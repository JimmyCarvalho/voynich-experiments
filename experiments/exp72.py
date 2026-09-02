# Exp 72: (a) previsibilidade da proxima palavra; (b) fractal? correlacao de longo alcance (DFA / expoente alpha)
import re, math, random, statistics
import numpy as np
from collections import Counter, defaultdict
from exp64 import voy_lines, to_lines, xw
from exp66 import train, gen_line
random.seed(5); np.random.seed(5)
N=34119
voy=[w for ws in voy_lines() for w in ws]
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N]
por=xw('Portuguese.xml')[:N]
ctx=train(3); gen=[]
while len(gen)<N: gen+=[w for w in gen_line(ctx,3).split() if w]
gen=gen[:N]
shuf=voy[:]; random.shuffle(shuf)
# bloco de um so escriba/secao (estrelas, mao 3) para controlar dialeto
pages={}; meta={}; order=[]
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip(); m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',r)
    if m:
        pg=m.group(1); t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
        pages.setdefault(pg,[]).extend(ws)
        if pg not in order: order.append(pg)
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))
blockS=[w for pg in order if meta.get(pg,{}).get('I')=='S' and meta.get(pg,{}).get('H')=='3' for w in pages[pg]]

# (a) previsibilidade
def word_pred(ws):
    half=len(ws)//2; tr,te=ws[:half],ws[half:]
    uni=Counter(tr); bi=defaultdict(Counter)
    for a,b in zip(tr,tr[1:]): bi[a][b]+=1
    V=len(uni)+1; tot=sum(uni.values())
    lp0=lp1=0; hit0=hit1=0; n=0
    best0=uni.most_common(1)[0][0]
    for a,b in zip(te,te[1:]):
        n+=1
        p0=(uni[b]+0.5)/(tot+0.5*V); lp0-=math.log2(p0); hit0+= b==best0
        c=bi.get(a)
        if c and sum(c.values())>=3:
            p1=(c[b]+0.5)/(sum(c.values())+0.5*V); hit1+= b==c.most_common(1)[0][0]
        else: p1=p0; hit1+= b==best0
        lp1-=math.log2(p1)
    return lp0/n, lp1/n, hit0/n, hit1/n
print(f"{'texto':22s} {'H(palavra)':>10s} {'H(pal|anterior)':>15s} {'ganho':>6s} {'acerto sem contexto':>19s} {'acerto com a anterior':>21s}")
for name,ws in [('Voynich',voy),('Voynich, so estrelas/mao 3',blockS),('latim',lat),('portugues',por),('cadeia ordem 3',gen)]:
    h0,h1,a0,a1=word_pred(ws)
    print(f"{name:22s} {h0:10.2f} {h1:15.2f} {h0-h1:6.2f} {a0*100:18.1f}% {a1*100:20.1f}%")

# (b) DFA
def dfa(x, scales=None):
    x=np.asarray(x,float); x=x-x.mean(); y=np.cumsum(x); n=len(y)
    if scales is None: scales=np.unique(np.logspace(np.log10(8),np.log10(n//8),18).astype(int))
    F=[]
    for s in scales:
        m=n//s; segs=y[:m*s].reshape(m,s); t=np.arange(s)
        res=[]
        for seg in segs:
            c=np.polyfit(t,seg,1); res.append(np.mean((seg-np.polyval(c,t))**2))
        F.append(np.sqrt(np.mean(res)))
    a=np.polyfit(np.log(scales),np.log(F),1)[0]
    return a
def series_len(ws): return [len(w) for w in ws]
def series_rank(ws):
    r={w:i+1 for i,(w,_) in enumerate(Counter(ws).most_common())}
    return [math.log(r[w]) for w in ws]
def series_gallows(ws): return [1 if any(g in w for g in 'ktpf') else 0 for w in ws]
print(f"\nexpoente DFA (0,50 = sem memoria longa; >0,5 = correlacao de longo alcance, 'fractal')")
print(f"{'texto':26s} {'tamanho da palavra':>18s} {'log-rank (frequencia)':>22s} {'tem gallows':>12s}")
for name,ws in [('Voynich',voy),('Voynich, so estrelas/mao 3',blockS),('Voynich embaralhado',shuf),('cadeia ordem 3',gen),('latim',lat),('portugues',por)]:
    print(f"{name:26s} {dfa(series_len(ws)):18.3f} {dfa(series_rank(ws)):22.3f} {dfa(series_gallows(ws)):12.3f}")
