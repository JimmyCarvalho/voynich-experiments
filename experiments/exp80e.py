# Exp 80e: decifracao como HMM (Knight et al.): estados = letras da lingua (transicoes FIXAS pelos bigramas da lingua), emissoes = simbolos (aprendidas por EM)
import re, math, random, sys, json, time
import numpy as np
from collections import Counter, defaultdict
from exp80b import learn_segmentation
MODE=sys.argv[1]; LANG=sys.argv[2]; SEED=int(sys.argv[3]) if len(sys.argv)>3 else 1; NIT=int(sys.argv[4]) if len(sys.argv)>4 else 40
random.seed(SEED); np.random.seed(SEED)
ALPHA='abcdefghilmnopqrstuvxyz'; A2I={c:i for i,c in enumerate(ALPHA)}
def clean(s): return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('k','c').replace('w','uu'))
if LANG=='latim':
    vul=re.sub(r'[^a-z\s]','',open('vulgate.txt').read().lower()).split(); lm_text=clean(''.join(vul[300000:700000]))
else:
    it=re.sub(r'[^a-z\s]','',open('naibbe/input/examples/divina_commedia.txt').read().lower()).split(); lm_text=clean(''.join(it))
lm_text=''.join(c for c in lm_text if c in A2I)
n=len(ALPHA); T=np.ones((n,n))*0.5
for a,b in zip(lm_text,lm_text[1:]): T[A2I[a],A2I[b]]+=1
T=T/T.sum(axis=1,keepdims=True); pi=np.array([lm_text.count(c) for c in ALPHA],float); pi/=pi.sum()
truth_lines=None
if MODE=='control':
    L1=[l.split() for l in open('naibbe/encrypted/lat_output_ciphertext.txt')]
    L2=[l.split() for l in open('naibbe/respaced_plaintext/lat_pre_encryption_respaced_plaintext.txt')]
    pairs=[(a,b) for a,b in zip(L1,L2) if a and b and len(a)==len(b)]
    lines=[a for a,b in pairs]; truth_lines=[b for a,b in pairs]
elif MODE=='voynich':
    from exp64 import voy_lines; lines=voy_lines()
elif MODE=='chain':
    from exp66 import train, gen_line
    ctx=train(3); lines=[]
    while sum(len(l) for l in lines)<34119:
        ws=[w for w in gen_line(ctx,3).split() if w]
        if ws: lines.append(ws)
cnt=Counter(w for l in lines for w in l)
U,split,f,g=learn_segmentation(cnt,n_uni=170)
PRE=set(x for x,_ in f.most_common(160)); SUF=set(x for x,_ in g.most_common(160))
def symbols_of(w):
    if w in U: return [('U',w)]
    if w in split:
        p,s=split[w]
        if p in PRE and s in SUF: return [('P',p),('S',s)]
    return None
flows=[]
for l in lines:
    fl=[]
    for w in l:
        t=symbols_of(w); fl.extend(t if t else [None])
    flows.append(fl)
syms=sorted(set(s for fl in flows for s in fl if s)); idx={s:i for i,s in enumerate(syms)}; m=len(syms)
segs=[]
for fl in flows:
    cur=[]
    for s in fl:
        if s: cur.append(idx[s])
        else:
            if len(cur)>=2: segs.append(np.array(cur))
            cur=[]
    if len(cur)>=2: segs.append(np.array(cur))
ntok=sum(len(s) for s in segs)
print(f"[{MODE}/{LANG}] simbolos {m}, segmentos {len(segs)}, tokens {ntok}", flush=True)
def forward_backward(B):
    Bc=np.zeros((n,m)); ll=0.0
    for seq in segs:
        L=len(seq); alpha=np.zeros((L,n)); beta=np.zeros((L,n)); c=np.zeros(L)
        alpha[0]=pi*B[:,seq[0]]; c[0]=alpha[0].sum(); alpha[0]/=c[0]
        for t in range(1,L):
            alpha[t]=(alpha[t-1]@T)*B[:,seq[t]]; c[t]=alpha[t].sum(); alpha[t]/=c[t]
        beta[L-1]=1.0
        for t in range(L-2,-1,-1):
            beta[t]=(T@(B[:,seq[t+1]]*beta[t+1]))/c[t+1]
        gamma=alpha*beta; gamma/=gamma.sum(axis=1,keepdims=True)
        np.add.at(Bc.T,seq,gamma)
        ll+=np.log(c).sum()
    return Bc,ll
t0=time.time(); best=None
for restart in range(int(sys.argv[5]) if len(sys.argv)>5 else 3):
    B=np.random.dirichlet(np.ones(m)*1.0,size=n); prev=-1e18
    for it in range(NIT):
        Bc,ll=forward_backward(B)
        B=(Bc+0.01)**1.3; B=B/B.sum(axis=1,keepdims=True)   # esparsificacao: empurra cada simbolo para uma letra so
        if it%10==0: print(f"  reinicio {restart} it {it} log-verossimilhanca/token {ll/ntok:.4f} ({time.time()-t0:.0f}s)", flush=True)
        if it>15 and ll-prev<1e-4*abs(ll): break
        prev=ll
    if best is None or ll>best[0]: best=(ll,B.copy())
ll,B=best
sym_letter=defaultdict(Counter); lT=np.log(T)
def viterbi(seq):
    L=len(seq); d=np.log(pi+1e-12)+np.log(B[:,seq[0]]+1e-12); bp=np.zeros((L,n),int)
    for t in range(1,L):
        cand=d[:,None]+lT; bp[t]=cand.argmax(axis=0); d=cand.max(axis=0)+np.log(B[:,seq[t]]+1e-12)
    path=[int(d.argmax())]
    for t in range(L-1,0,-1): path.append(int(bp[t][path[-1]]))
    return path[::-1]
for seq in segs:
    for s,st in zip(seq,viterbi(seq)): sym_letter[s][st]+=1
assign={syms[i]:ALPHA[sym_letter[i].most_common(1)[0][0]] for i in range(m) if sym_letter[i]}
print(f"[{MODE}/{LANG}] log-verossimilhanca por token: {ll/ntok:.4f}", flush=True)
if truth_lines:
    tr=defaultdict(Counter)
    for a,tl in zip(lines,truth_lines):
        for w,p in zip(a,tl):
            t=symbols_of(w)
            if not t: continue
            if len(t)==1: tr[t[0]][p[0]]+=1
            elif len(p)==2: tr[t[0]][p[0]]+=1; tr[t[1]][p[1]]+=1
    scnt=Counter(s for fl in flows for s in fl if s)
    truth={s:tr[s].most_common(1)[0][0] for s in syms if tr[s]}
    hit=sum(scnt[s] for s in syms if s in truth and assign.get(s)==truth[s]); tot=sum(scnt[s] for s in syms if s in truth)
    print(f"[control] acuracia por letra: {hit/tot*100:.1f}%", flush=True)
print("primeiras linhas decodificadas (Viterbi):")
for fl in flows[:4]:
    seq=[idx[s] for s in fl if s]; out=''
    if len(seq)>=2: out=''.join(ALPHA[p] for p in viterbi(np.array(seq)))
    print("   ",out)
json.dump({'mode':MODE,'lang':LANG,'ll_per_token':ll/ntok,'assign':{f'{k[0]}:{k[1]}':v for k,v in assign.items()}},open(f'exp80e_{MODE}_{LANG}.json','w'))
