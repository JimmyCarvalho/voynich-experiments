# Exp 53c: separar MAO de SECAO -- comparar escribas dentro da MESMA secao (herbario)
import re, math, statistics
from collections import Counter, defaultdict
from exp53b import model, xent
pages={}; meta={}; order=[]
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip()
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',r)
    if m:
        pg=m.group(1); t=re.sub(r'<[^>]*>','',m.group(5))
        t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
        pages.setdefault(pg,[]).extend(ws)
        if pg not in order: order.append(pg)
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))
cell=defaultdict(list)
for pg in order:
    md=meta.get(pg,{})
    if 'H' in md and 'I' in md: cell[(md['I'],md['H'])].extend(pages[pg])
print("celulas secao x escriba com >400 palavras:")
big={k:v for k,v in cell.items() if len(v)>400}
for k in sorted(big): print(f"  secao {k[0]}, escriba {k[1]}: {len(big[k])} palavras")
M={k:model(v) for k,v in big.items()}
print("\npenalidade cruzada (bits/glifo), por tipo de par:")
same_sec=[]; same_scr=[]; both_diff=[]
for a in big:
    for b in big:
        if a==b: continue
        p=xent(big[b],M[a])-xent(big[b],M[b])
        if a[0]==b[0]: same_sec.append((p,a,b))
        elif a[1]==b[1]: same_scr.append((p,a,b))
        else: both_diff.append((p,a,b))
def rep(name,L):
    if L: print(f"  {name:38s} n={len(L):2d}  media +{statistics.mean(x[0] for x in L):.3f} bits")
rep('MESMA secao, escriba DIFERENTE',same_sec)
rep('MESMO escriba, secao DIFERENTE',same_scr)
rep('secao e escriba diferentes',both_diff)
print("\ndetalhe, mesma secao / maos diferentes:")
for p,a,b in sorted(same_sec): print(f"    modelo {a} -> texto {b}: +{p:.3f}")
