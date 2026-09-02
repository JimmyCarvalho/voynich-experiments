# Exp 69: validacao fora da amostra do modelo de 2 ingredientes (Markov 3 + 4% copia local)
import re, math, random, statistics, json
from collections import Counter
from exp66 import train, gen_line
from exp57 import hybrid, pages_of
from exp51 import voy_words
import xml.etree.ElementTree as ET
random.seed(3)
voy=voy_words(); N=len(voy)
ctx=train(3); out=[]
while sum(len(l) for l in out)<N*1.15:
    ws=[w for w in gen_line(ctx,3).split() if w]
    if ws: out.append(ws)
random.seed(11); model=[w for pg in hybrid(pages_of(out),0.04,exact=0.4) for l in pg for w in l][:N]
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N]
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
por=xw('Portuguese.xml')[:N]
def lendist(ws):
    c=Counter(len(w) for w in ws); n=len(ws); return {k:c[k]/n for k in range(1,16)}
def kl(p,q): return sum(p[k]*math.log2(p[k]/max(q[k],1e-9)) for k in p if p[k]>0)
def vm(ws):
    L=[len(w) for w in ws]; return statistics.pvariance(L)/statistics.mean(L)
def heaps(ws):
    seen=set(); pts={}
    for i,w in enumerate(ws,1):
        seen.add(w)
        if i in (2000,5000,10000,20000,34000): pts[i]=len(seen)
    return pts
def zipf_slope(ws):
    c=Counter(ws).most_common(1000); xs=[math.log(r) for r in range(1,len(c)+1)]; ys=[math.log(f) for _,f in c]
    mx=statistics.mean(xs); my=statistics.mean(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
def burst(ws,top=150):
    pos={}
    for i,w in enumerate(ws): pos.setdefault(w,[]).append(i)
    common=[w for w,_ in Counter(ws).most_common(top)]
    cvs=[]
    for w in common:
        g=[b-a for a,b in zip(pos[w],pos[w][1:])]
        if len(g)>=10: cvs.append(statistics.pstdev(g)/statistics.mean(g))
    return statistics.mean(cvs)
def top_cov(ws,k): return sum(c for _,c in Counter(ws).most_common(k))/len(ws)
print(f"{'medida (fora do ajuste)':40s} {'Voynich':>9s} {'modelo':>9s} {'latim':>9s} {'portugues':>9s}")
rows=[('tamanho: variancia/media',vm),('tamanho: KL(real||x) em bits',None),('Heaps: tipos apos 10k palavras',lambda w:heaps(w)[10000]),
      ('Heaps: tipos apos 34k palavras',lambda w:heaps(w)[34000]),('Zipf: inclinacao (top 1000)',zipf_slope),
      ('cobertura das 100 mais comuns',lambda w:top_cov(w,100)),('cobertura das 1000 mais comuns',lambda w:top_cov(w,1000)),
      ('burstiness (CV dos intervalos, 150 top)',burst)]
LD=lendist(voy)
for name,f in rows:
    if f is None:
        vals=[0.0]+[kl(LD,lendist(x)) for x in (model,lat,por)]
    else: vals=[f(x) for x in (voy,model,lat,por)]
    print(f"{name:40s} "+' '.join(f"{v:9.3f}" for v in vals))
# distribuicao de tamanhos lado a lado
print("\ntamanho da palavra  real   modelo   latim")
for k in range(1,13):
    print(f"   {k:2d}            {LD[k]*100:5.1f}%  {lendist(model)[k]*100:5.1f}%  {lendist(lat)[k]*100:5.1f}%")
json.dump({'lendist_real':LD,'lendist_model':lendist(model)},open('exp69.json','w'))
