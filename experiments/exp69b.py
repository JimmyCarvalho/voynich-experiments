# Exp 69b: a burstiness sobrevive DENTRO de uma secao com um so escriba? (topico vs dialeto)
import re, math, random, statistics
from collections import Counter, defaultdict
from exp69 import burst, xw
from exp66 import gen_line
random.seed(4)
pages={}; meta={}; order=[]; plines={}
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip()
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',r)
    if m:
        pg=m.group(1); t=re.sub(r'<[^>]*>','',m.group(5))
        t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
        if not ws: continue
        pages.setdefault(pg,[]).extend(ws); plines.setdefault(pg,[]).append(ws)
        if pg not in order: order.append(pg)
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))
def block(sec,hand):
    ws=[]; ls=[]
    for pg in order:
        md=meta.get(pg,{})
        if md.get('I')==sec and md.get('H')==hand: ws+=pages[pg]; ls+=plines[pg]
    return ws,ls
def train_lines(lines,k=3):
    ctx=defaultdict(Counter)
    for ws in lines:
        s='^'*k+' '.join(ws)+'$'
        for i in range(k,len(s)): ctx[s[i-k:i]][s[i]]+=1
    return ctx
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
por=xw('Portuguese.xml')
print(f"{'bloco (secao/escriba)':26s} {'palavras':>8s} {'burst real':>10s} {'cadeia ordem 3 (mesmo bloco)':>28s} {'latim mesmo n':>13s} {'portugues':>10s}")
for sec,hand,name in [('B','2','biologica / mao 2'),('S','3','estrelas / mao 3'),('H','1','herbario / mao 1'),('H','2','herbario / mao 2')]:
    ws,ls=block(sec,hand); n=len(ws)
    if n<2000: continue
    ctx=train_lines(ls); gen=[]
    while len(gen)<n: gen+=[w for w in gen_line(ctx,3).split() if w]
    top=min(150,max(30,n//60))
    b_real=burst(ws,top); b_gen=burst(gen[:n],top)
    b_lat=statistics.mean(burst(lat[i:i+n],top) for i in range(0,n*5,n)); b_por=statistics.mean(burst(por[i:i+n],top) for i in range(0,n*5,n))
    print(f"{name:26s} {n:8d} {b_real:10.3f} {b_gen:28.3f} {b_lat:13.3f} {b_por:10.3f}")
