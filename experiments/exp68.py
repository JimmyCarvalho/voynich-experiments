# Exp 68: as etiquetas do zodiaco. posicao, marcador de signo, prefixos
import re, random, statistics, math
from collections import Counter, defaultdict
from exp49 import ed1
random.seed(1)
SIGN={'f70v2':'Peixes','f70v1':'Aries-escuro','f71r':'Aries-claro','f71v':'Touro-claro','f72r1':'Touro-escuro','f72r2':'Gemeos',
      'f72r3':'Cancer','f72v3':'Leao','f72v2':'Virgem','f72v1':'Libra','f73r':'Escorpiao','f73v':'Sagitario'}
labels=defaultdict(list)   # page -> list of (ring, clock, word)
ring={}
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f7[0-3][rv][0-9]?)\.(\d+),([@+=&])(Lz)>\s*(?:<!(\d+):(\d+)>)?\s*(.*)',raw.strip())
    if not m: continue
    pg=m.group(1)
    if m.group(3)=='@': ring[pg]=ring.get(pg,-1)+1
    t=re.sub(r'<[^>]*>','',m.group(7)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
    ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
    if not ws: continue
    clock=(int(m.group(5))%12)+int(m.group(6))/60 if m.group(5) else None
    labels[pg].append((ring.get(pg,0),clock,ws[0],ws))
for pg in SIGN:
    L=labels[pg]; print(f"{pg:6s} {SIGN[pg]:14s} {len(L):2d} etiquetas, {len(set(r for r,_,_,_ in L))} aneis, ex.: {' '.join(w for _,_,w,_ in L[:6])}")
allw=[w for pg in labels for _,_,w,_ in labels[pg]]
print(f"\ntotal {len(allw)} etiquetas, {len(set(allw))} distintas")

# (c) prefixo: com que comecam as etiquetas?
def prefix_profile(ws,n=2):
    c=Counter(w[:n] for w in ws); N=len(ws)
    return {k:v/N for k,v in c.most_common(8)}
from exp51 import voy_words
text=voy_words()
print("\ninicio das etiquetas do zodiaco (2 glifos):", {k:f"{v*100:.0f}%" for k,v in prefix_profile(allw).items()})
print("inicio das palavras do texto corrido:    ", {k:f"{v*100:.0f}%" for k,v in prefix_profile(text).items()})
ot=sum(1 for w in allw if w[:2] in ('ot','ok','op','of'))/len(allw); ot_t=sum(1 for w in text if w[:2] in ('ot','ok','op','of'))/len(text)
print(f"etiquetas comecando com o+gallows: {ot*100:.0f}%   texto corrido: {ot_t*100:.0f}%")

# (b) marcador de signo: pares de etiquetas com mesmo prefixo de 3 glifos, dentro do signo vs entre signos
def share(a,b,n): return a[:n]==b[:n]
def pair_rate(same,n,suffix=False):
    hit=tot=0
    pages=list(labels)
    for i,p in enumerate(pages):
        for j,q in enumerate(pages):
            if (p==q)!=same or (not same and j<=i): continue
            for _,_,a,_ in labels[p]:
                for _,_,b,_ in labels[q]:
                    if p==q and a is b: continue
                    tot+=1; hit+= (a[-n:]==b[-n:]) if suffix else (a[:n]==b[:n])
    return hit/tot
for n in [2,3,4]:
    print(f"prefixo de {n} glifos igual: dentro do signo {pair_rate(True,n)*100:.1f}%  entre signos {pair_rate(False,n)*100:.1f}%   | sufixo de {n}: dentro {pair_rate(True,n,True)*100:.1f}%  entre {pair_rate(False,n,True)*100:.1f}%")

# (a) posicao: etiquetas na mesma posicao (mesmo anel, ordem angular) em signos diferentes sao mais parecidas?
def ordered(pg):
    L=sorted(labels[pg],key=lambda x:(x[0],x[1] if x[1] is not None else 99))
    return [w for _,_,w,_ in L]
def nedit(a,b):
    # distancia de edicao normalizada
    import functools
    la,lb=len(a),len(b); d=list(range(lb+1))
    for i in range(1,la+1):
        prev=d[:]; d[0]=i
        for j in range(1,lb+1): d[j]=min(prev[j]+1,d[j-1]+1,prev[j-1]+(a[i-1]!=b[j-1]))
    return d[lb]/max(la,lb)
full=[pg for pg in SIGN if len(labels[pg])>=26]
pos_d=[]; rnd_d=[]
for i,p in enumerate(full):
    for q in full[i+1:]:
        A,B=ordered(p),ordered(q); n=min(len(A),len(B))
        pos_d+= [nedit(A[k],B[k]) for k in range(n)]
        Bs=B[:]; random.shuffle(Bs); rnd_d+=[nedit(A[k],Bs[k]) for k in range(n)]
print(f"\nmesma posicao em signos diferentes: distancia media {statistics.mean(pos_d):.3f} (n={len(pos_d)})   posicao aleatoria: {statistics.mean(rnd_d):.3f}")
same_pos_exact=sum(1 for i,p in enumerate(full) for q in full[i+1:] for k in range(min(len(ordered(p)),len(ordered(q)))) if ordered(p)[k]==ordered(q)[k])
print(f"etiquetas identicas na mesma posicao: {same_pos_exact} de {len(pos_d)} pares")
# etiquetas repetidas entre signos (qualquer posicao)
byw=defaultdict(set)
for pg in labels:
    for _,_,w,_ in labels[pg]: byw[w].add(pg)
multi={w:p for w,p in byw.items() if len(p)>1}
print(f"etiquetas que aparecem em mais de um signo: {len(multi)} ({', '.join(f'{w}:{len(p)}' for w,p in sorted(multi.items(),key=lambda x:-len(x[1]))[:10])})")
