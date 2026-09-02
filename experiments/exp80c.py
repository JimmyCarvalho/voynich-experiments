# Exp 80c, passo B: solucionador homofonico no nivel dos SIMBOLOS (unigramas + prefixos + sufixos aprendidos), 1 letra por simbolo
import re, math, random, sys, time, json
from collections import Counter, defaultdict
from exp80b import learn_segmentation
MODE=sys.argv[1]; SEED=int(sys.argv[2]); ITERS=int(sys.argv[3]); LANG=sys.argv[4]; LAMBDA=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
random.seed(SEED)
ALPHA='abcdefghilmnopqrstuvxyz'
def clean(s): return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('k','c').replace('w','uu'))
def build_lm(text,order=4):
    tabs=[defaultdict(Counter) for _ in range(order)]
    for i in range(len(text)):
        for k in range(order):
            if i>=k: tabs[k][text[i-k:i]][text[i]]+=1
    V=len(ALPHA); cache={}
    def lp(ctx,ch):
        key=(ctx,ch); v=cache.get(key)
        if v is not None: return v
        v=None
        for k in range(min(order-1,len(ctx)),-1,-1):
            c=tabs[k].get(ctx[len(ctx)-k:] if k else '')
            if c and sum(c.values())>=5: v=math.log((c.get(ch,0)+0.2)/(sum(c.values())+0.2*V)); break
        if v is None: v=math.log(1/V)
        cache[key]=v; return v
    return lp
if LANG=='latim':
    vul=re.sub(r'[^a-z\s]','',open('vulgate.txt').read().lower()).split()
    lm_text=clean(''.join(vul[300000:700000])); held=clean(''.join(vul[750000:800000]))
else:
    it=re.sub(r'[^a-z\s]','',open('naibbe/input/examples/divina_commedia.txt').read().lower()).split()
    full=clean(''.join(it)); lm_text=full[:-30000]; held=full[-30000:]
LP=build_lm(lm_text); P_LET={c:lm_text.count(c)/len(lm_text) for c in ALPHA}
hs=sum(LP(held[max(0,i-3):i],held[i]) for i in range(len(held)))/len(held)
# ---------- texto ----------
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
N_UNI=int(sys.argv[6]) if len(sys.argv)>6 else 170
U,split,f,g=learn_segmentation(cnt,n_uni=N_UNI)
PRE=set(x for x,_ in f.most_common(160)); SUF=set(x for x,_ in g.most_common(160))
def symbols_of(w):
    if w in U: return [('U',w)]
    if w in split:
        p,s=split[w]
        if p in PRE and s in SUF: return [('P',p),('S',s)]
    return None
tok_syms=[[symbols_of(w) for w in l] for l in lines]
syms=sorted(set(s for l in tok_syms for t in l if t for s in t))
scnt=Counter(s for l in tok_syms for t in l if t for s in t)
covered=sum(1 for l in tok_syms for t in l if t)/sum(len(l) for l in lines)
print(f"[{MODE}/{LANG}] tokens {sum(len(l) for l in lines)}, simbolos {len(syms)} ({len(U)} unigramas, {len(PRE)} prefixos, {len(SUF)} sufixos), tokens cobertos {covered*100:.0f}%; LM em texto real: {hs:.3f} nats/letra", flush=True)
# ---------- estado ----------
assign={s:random.choices(ALPHA,[P_LET[c] for c in ALPHA])[0] for s in syms}
occ=defaultdict(list)
for li,l in enumerate(tok_syms):
    for ti,t in enumerate(l):
        if t:
            for s in t: occ[s].append((li,ti))
def tok_str(t): return ''.join(assign[s] for s in t) if t else '?'
def score_span(letters,start,end):
    sc=0.0
    for i in range(start,min(end,len(letters))):
        ch=letters[i]
        if ch=='?': sc+=math.log(1/len(ALPHA)); continue
        sc+=LP(letters[max(0,i-3):i].replace('?',''),ch)
    return sc
def line_score(l): 
    s=''.join(tok_str(t) for t in l); return score_span(s,0,len(s))
def delta_line(l,ti,old_tok,new_tok):
    pre=''.join(tok_str(t) for t in l[:ti]); post=''.join(tok_str(t) for t in l[ti+1:])
    a=len(pre); old=pre+old_tok+post; new=pre+new_tok+post
    return score_span(new,a,a+len(new_tok)+3)-score_span(old,a,a+len(old_tok)+3)
LC=Counter()
for s in syms: LC[assign[s]]+=scnt[s]
def kl_pen(c):
    n=sum(c.values()); return LAMBDA*n*sum((c[ch]/n)*math.log((c[ch]/n)/P_LET[ch]) for ch in ALPHA if c[ch]>0)
total=sum(line_score(l) for l in tok_syms)-kl_pen(LC)
if truth_lines:
    # letra verdadeira de cada simbolo (majoritaria)
    tr=defaultdict(Counter)
    for a,b,tl in zip(lines,tok_syms,truth_lines):
        for w,t,p in zip(a,b,tl):
            if not t: continue
            if len(t)==1: tr[t[0]][p[0] if len(p)==1 else p]+=1
            elif len(p)==2: tr[t[0]][p[0]]+=1; tr[t[1]][p[1]]+=1
    truth={s:tr[s].most_common(1)[0][0] for s in syms if tr[s]}
    saved=dict(assign)
    for s in syms: assign[s]=truth.get(s,'e')[0]
    tl=sum(line_score(l) for l in tok_syms); nl=sum(len(''.join(tok_str(t) for t in l)) for l in tok_syms)
    print(f"[control] chave verdadeira: {tl/nl:.3f} nats/letra", flush=True); assign=saved
best=(total,dict(assign)); t0=time.time()
for it in range(ITERS):
    T=1.5*(1-it/ITERS)**2+0.05
    s=random.choice(syms); old=assign[s]; new=random.choice(ALPHA)
    if new==old: continue
    d=0.0
    O=occ[s]; CAP=300
    if len(O)>CAP: O=random.sample(O,CAP)
    scale=len(occ[s])/len(O)
    for li,ti in O:
        t=tok_syms[li][ti]; old_tok=tok_str(t); assign[s]=new; new_tok=tok_str(t); assign[s]=old
        d+=delta_line(tok_syms[li],ti,old_tok,new_tok)
    d*=scale
    pen_old=kl_pen(LC); LC[old]-=scnt[s]; LC[new]+=scnt[s]; d+=pen_old-kl_pen(LC)
    if d>=0 or random.random()<math.exp(d/T):
        assign[s]=new; total+=d
        if total>best[0]: best=(total,dict(assign))
    else: LC[new]-=scnt[s]; LC[old]+=scnt[s]
    if it%100000==0: print(f"  it {it} total/letra {total/sum(len(''.join(tok_str(t) for t in l)) for l in tok_syms):.3f} ({time.time()-t0:.0f}s)", flush=True)
assign=best[1]
nl=sum(len(''.join(tok_str(t) for t in l)) for l in tok_syms)
lm_only=sum(line_score(l) for l in tok_syms)/nl
print(f"[{MODE}/{LANG}] resultado: LM {lm_only:.3f} nats/letra (perplexidade {math.exp(-lm_only):.1f}; texto real {math.exp(-hs):.1f})", flush=True)
if truth_lines:
    hit=sum(scnt[s] for s in syms if s in truth and assign[s]==truth[s][0]); tot=sum(scnt[s] for s in syms if s in truth)
    print(f"[control] acuracia por letra: {hit/tot*100:.1f}%")
print("primeiras linhas decodificadas:")
for l in tok_syms[:4]: print("   ",''.join(tok_str(t) for t in l))
json.dump({'mode':MODE,'lang':LANG,'lm':lm_only,'assign':{f'{k[0]}:{k[1]}':v for k,v in assign.items()}},open(f'exp80c_{MODE}_{LANG}_{SEED}.json','w'))
