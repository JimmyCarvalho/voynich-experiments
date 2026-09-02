import re, math
from collections import Counter, defaultdict
cls=defaultdict(list)   # class -> words
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=m.group(5).replace('<->','.GAP.')
    t=re.sub(r'<[^>]*>','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
    t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
    toks=[re.sub(r'[^A-Za-z]','',w) for w in t.split('.')]; toks=[w for w in toks if w]
    if m.group(3)=='&': continue   # skip continuation lines for position classes
    words=[w for w in toks if w!='GAP']
    if len(words)<3: continue
    for i,w in enumerate(toks):
        if w=='GAP': continue
        pre = i+1<len(toks) and toks[i+1]=='GAP'
        post= i>0 and toks[i-1]=='GAP'
        first = (i==0); last=(i==len(toks)-1)
        if first: c='inicio_linha'
        elif last: c='fim_linha'
        elif pre: c='antes_desenho'
        elif post: c='depois_desenho'
        else: c='meio'
        cls[c].append(w)
def prof(ws):
    n=len(ws)
    return dict(n=n, len=sum(map(len,ws))/n,
                fim_m=sum(w.endswith('m') for w in ws)/n, fim_y=sum(w.endswith('y') for w in ws)/n,
                fim_n=sum(w.endswith('n') for w in ws)/n,
                ini_q=sum(w.startswith('q') for w in ws)/n, ini_gallows=sum(w[0] in 'ktpf' for w in ws)/n,
                ini_d=sum(w.startswith('d') for w in ws)/n, ini_s=sum(w.startswith('s') for w in ws)/n)
print(f"{'classe':15s} {'n':>6s} {'tam':>5s} {'-m':>6s} {'-y':>6s} {'-n':>6s} {'q-':>6s} {'ktpf-':>6s} {'d-':>6s} {'s-':>6s}")
for c in ['meio','fim_linha','antes_desenho','depois_desenho','inicio_linha']:
    p=prof(cls[c])
    print(f"{c:15s} {p['n']:6d} {p['len']:5.2f} {p['fim_m']*100:5.1f}% {p['fim_y']*100:5.1f}% {p['fim_n']*100:5.1f}% {p['ini_q']*100:5.1f}% {p['ini_gallows']*100:5.1f}% {p['ini_d']*100:5.1f}% {p['ini_s']*100:5.1f}%")
# significance of -m before drawing vs mid
import random
random.seed(1)
mid=cls['meio']; pre=cls['antes_desenho']
obs=sum(w.endswith('m') for w in pre)/len(pre)
pool=mid+pre; k=len(pre); cnt=0; B=5000
for _ in range(B):
    s=random.sample(pool,k); v=sum(w.endswith('m') for w in s)/k
    if v>=obs: cnt+=1
print(f"\n-m antes de desenho: {obs*100:.1f}% ; p(permutacao vs meio) = {cnt/B:.4f}")
obs=sum(w.startswith('q') for w in cls['depois_desenho'])/len(cls['depois_desenho'])
pool=mid+cls['depois_desenho']; k=len(cls['depois_desenho']); cnt=0
for _ in range(B):
    s=random.sample(pool,k); v=sum(w.startswith('q') for w in s)/k
    if v<=obs: cnt+=1
print(f"q- depois de desenho: {obs*100:.1f}% ; p(permutacao vs meio, menor) = {cnt/B:.4f}")
