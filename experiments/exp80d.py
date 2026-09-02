# Exp 80d: passo C: agrupar os simbolos homofonos pelo CONTEXTO (homofonos da mesma letra tem vizinhos parecidos), depois resolver como substituicao simples
import re, math, random, sys, json
import numpy as np
from collections import Counter, defaultdict
from exp80b import learn_segmentation
from scipy.cluster.hierarchy import linkage, fcluster
MODE=sys.argv[1]; LANG=sys.argv[2] if len(sys.argv)>2 else 'latim'; K=int(sys.argv[3]) if len(sys.argv)>3 else 23; SEED=int(sys.argv[4]) if len(sys.argv)>4 else 1
random.seed(SEED); np.random.seed(SEED)
ALPHA='abcdefghilmnopqrstuvxyz'
def clean(s): return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('k','c').replace('w','uu'))
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
# fluxo de simbolos por linha (None = desconhecido)
flows=[]
for l in lines:
    fl=[]
    for w in l:
        t=symbols_of(w); fl.extend(t if t else [None])
    flows.append(fl)
syms=sorted(set(s for fl in flows for s in fl if s)); idx={s:i for i,s in enumerate(syms)}; n=len(syms)
scnt=Counter(s for fl in flows for s in fl if s)
# vetores de contexto: distribuicao dos simbolos vizinhos (esquerda e direita), suavizada
L=np.zeros((n,n)); R=np.zeros((n,n))
for fl in flows:
    for i,s in enumerate(fl):
        if not s: continue
        if i>0 and fl[i-1]: L[idx[s],idx[fl[i-1]]]+=1
        if i+1<len(fl) and fl[i+1]: R[idx[s],idx[fl[i+1]]]+=1
X=np.hstack([L,R])+0.5; X=X/X.sum(axis=1,keepdims=True); X=np.sqrt(X)   # Hellinger
Z=linkage(X,method='average',metric='cosine'); cl=fcluster(Z,K,criterion='maxclust')
clusters=defaultdict(list)
for s,c in zip(syms,cl): clusters[c].append(s)
print(f"[{MODE}] simbolos {n}, agrupados em {len(clusters)} grupos; tamanhos: {sorted([sum(scnt[s] for s in v) for v in clusters.values()],reverse=True)[:12]}...", flush=True)
if truth_lines:
    tr=defaultdict(Counter)
    for a,tl in zip(lines,truth_lines):
        for w,p in zip(a,tl):
            t=symbols_of(w)
            if not t: continue
            if len(t)==1: tr[t[0]][p[0]]+=1
            elif len(p)==2: tr[t[0]][p[0]]+=1; tr[t[1]][p[1]]+=1
    truth={s:tr[s].most_common(1)[0][0] for s in syms if tr[s]}
    pure=0; tot=0
    for c,v in clusters.items():
        lc=Counter()
        for s in v: lc[truth.get(s,'?')]+=scnt[s]
        pure+=lc.most_common(1)[0][1]; tot+=sum(lc.values())
    print(f"[control] pureza dos grupos (fracao de tokens na letra majoritaria do grupo): {pure/tot*100:.1f}%", flush=True)
    # quantas letras distintas dominam grupos
    dom=Counter()
    for c,v in clusters.items():
        lc=Counter()
        for s in v: lc[truth.get(s,'?')]+=scnt[s]
        dom[lc.most_common(1)[0][0]]+=1
    print(f"[control] letras distintas representadas como majoritarias: {len(dom)} de {K} grupos", flush=True)
# ---------- substituicao simples: grupo -> letra, com LM 4-gramas ----------
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
LP=build_lm(lm_text); hs=sum(LP(held[max(0,i-3):i],held[i]) for i in range(len(held)))/len(held)
P_LET={c:lm_text.count(c)/len(lm_text) for c in ALPHA}
group_of={s:c for c,v in clusters.items() for s in v}
gflows=[[group_of[s] if s else None for s in fl] for fl in flows]
gcnt=Counter(g for fl in gflows for g in fl if g)
gids=sorted(clusters)
# contagem de 4-tuplas de grupos (contexto de 3 + alvo), None = desconhecido
tup=Counter()
for fl in gflows:
    for i in range(len(fl)):
        tup[tuple(fl[max(0,i-3):i+1])]+=1
by_g=defaultdict(list)
for t in tup:
    for g in set(x for x in t if x): by_g[g].append(t)
def lp_tuple(t,assign):
    ch=assign[t[-1]] if t[-1] else None
    if ch is None: return math.log(1/len(ALPHA))
    ctx=''.join(assign[x] for x in t[:-1] if x)
    return LP(ctx,ch)
def full_score(assign): return sum(c*lp_tuple(t,assign) for t,c in tup.items())
LAMBDA=0.5
def kl(assign):
    c=Counter()
    for g in gids: c[assign[g]]+=gcnt[g]
    nn=sum(c.values()); return LAMBDA*nn*sum((c[ch]/nn)*math.log((c[ch]/nn)/P_LET[ch]) for ch in ALPHA if c[ch]>0)
def partial(assign,gs):
    ts=set()
    for g in gs: ts.update(by_g[g])
    return sum(tup[t]*lp_tuple(t,assign) for t in ts)
nl=sum(len(fl) for fl in gflows)
best=None
for restart in range(4):
    order_g=sorted(gids,key=lambda g:-gcnt[g]); order_l=sorted(ALPHA,key=lambda c:-P_LET[c])
    assign={g:order_l[i%len(order_l)] for i,g in enumerate(order_g)}
    if restart>0:
        for g in gids:
            if random.random()<0.5: assign[g]=random.choice(ALPHA)
    cur=full_score(assign)-kl(assign); loc=(cur,dict(assign))
    for it in range(2500):
        T=1500*(1-it/2500)**2+15
        if random.random()<0.5:
            g=random.choice(gids); old=assign[g]; new=random.choice(ALPHA)
            if new==old: continue
            before=partial(assign,[g])-kl(assign); assign[g]=new; after=partial(assign,[g])-kl(assign)
            d=after-before
            if d>=0 or random.random()<math.exp(d/T): cur+=d
            else: assign[g]=old
        else:
            g,g2=random.sample(gids,2)
            before=partial(assign,[g,g2])-kl(assign); assign[g],assign[g2]=assign[g2],assign[g]; after=partial(assign,[g,g2])-kl(assign)
            d=after-before
            if d>=0 or random.random()<math.exp(d/T): cur+=d
            else: assign[g],assign[g2]=assign[g2],assign[g]
        if cur>loc[0]: loc=(cur,dict(assign))
    if best is None or loc[0]>best[0]: best=loc
assign=best[1]; lm_only=full_score(assign)/nl
def decode(fl,assign): return ''.join(assign[g] if g else '?' for g in fl)
print(f"[{MODE}/{LANG}] substituicao sobre os grupos: LM {lm_only:.3f} nats/letra (perplexidade {math.exp(-lm_only):.1f}; texto real {math.exp(-hs):.1f})", flush=True)
if truth_lines:
    hit=sum(scnt[s] for s in syms if s in truth and assign[group_of[s]]==truth[s]); tot=sum(scnt[s] for s in syms if s in truth)
    print(f"[control] acuracia por letra: {hit/tot*100:.1f}%")
print("primeiras linhas decodificadas:")
for fl in gflows[:4]: print("   ",decode(fl,assign))
json.dump({'mode':MODE,'lang':LANG,'lm':lm_only},open(f'exp80d_{MODE}_{LANG}.json','w'))
