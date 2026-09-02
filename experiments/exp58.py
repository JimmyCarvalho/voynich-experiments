# Exp 58: as trocas de MAO (Davis 2020) coincidem com saltos no comportamento do texto, controlando a SECAO?
import re, math, random, statistics, json
from collections import Counter, defaultdict
random.seed(8)
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
# vetor de caracteristicas por pagina: bigramas de glifo com '#' de borda (robusto para paginas pequenas)
def feat(ws):
    c=Counter()
    for w in ws:
        s='#'+w+'#'
        for i in range(len(s)-1): c[s[i:i+2]]+=1
    n=sum(c.values()); return {k:v/n for k,v in c.items()}
def js(p,q):
    keys=set(p)|set(q); m={k:(p.get(k,0)+q.get(k,0))/2 for k in keys}
    def kl(a,b): return sum(a[k]*math.log2(a[k]/b[k]) for k in a if a[k]>0)
    return 0.5*kl(p,m)+0.5*kl(q,m)
good=[pg for pg in order if len(pages[pg])>=60 and 'H' in meta.get(pg,{}) and 'I' in meta.get(pg,{})]
F={pg:feat(pages[pg]) for pg in good}
same_hand=[]; diff_hand=[]
for a,b in zip(good,good[1:]):
    if meta[a]['I']!=meta[b]['I']: continue          # so pares na MESMA secao
    d=js(F[a],F[b])
    (same_hand if meta[a]['H']==meta[b]['H'] else diff_hand).append((d,a,b,meta[a]['H'],meta[b]['H']))
print(f"paginas consecutivas na MESMA secao:")
print(f"  mesma mao:      n={len(same_hand):3d}  JS mediana={statistics.median(x[0] for x in same_hand):.4f}  media={statistics.mean(x[0] for x in same_hand):.4f}")
print(f"  mao diferente:  n={len(diff_hand):3d}  JS mediana={statistics.median(x[0] for x in diff_hand):.4f}  media={statistics.mean(x[0] for x in diff_hand):.4f}")
# permutacao: embaralha os rotulos de mao dentro da secao
obs=statistics.mean(x[0] for x in diff_hand)-statistics.mean(x[0] for x in same_hand)
pairs=same_hand+diff_hand; cnt=0; B=3000
labels=[x[3]==x[4] for x in pairs]
# permutacao das maos por pagina (nao dos pares) dentro de cada secao
from itertools import groupby
def perm_stat():
    lab={}
    for sec in set(meta[p]['I'] for p in good):
        pg=[p for p in good if meta[p]['I']==sec]; hs=[meta[p]['H'] for p in pg]; random.shuffle(hs)
        for p,h in zip(pg,hs): lab[p]=h
    s=[];d=[]
    for a,b in zip(good,good[1:]):
        if meta[a]['I']!=meta[b]['I']: continue
        (s if lab[a]==lab[b] else d).append(js(F[a],F[b]))
    return statistics.mean(d)-statistics.mean(s) if s and d else 0
for _ in range(B):
    if perm_stat()>=obs: cnt+=1
print(f"  diferenca observada {obs:+.4f}, p(permutacao)={cnt/B:.4f}")
print("\ndetalhe das trocas de mao dentro da mesma secao (JS entre as duas paginas):")
for d,a,b,h1,h2 in sorted(diff_hand,reverse=True)[:12]: print(f"    {a:6s}(mao {h1}) -> {b:6s}(mao {h2})  JS={d:.4f}")
# classificacao: o texto sozinho recupera o rotulo de mao de Davis? (herbario, centroide, leave-one-out)
herb=[p for p in good if meta[p]['I']=='H']
hands=Counter(meta[p]['H'] for p in herb); print(f"\nherbario: paginas por mao {dict(hands)}")
def centroid(pgs):
    c=Counter()
    for p in pgs:
        for k,v in F[p].items(): c[k]+=v
    n=len(pgs); return {k:v/n for k,v in c.items()}
hit=0; conf=Counter()
for p in herb:
    cents={h:centroid([q for q in herb if q!=p and meta[q]['H']==h]) for h in hands if hands[h]>1}
    pred=min(cents,key=lambda h: js(F[p],cents[h])); conf[(meta[p]['H'],pred)]+=1
    hit+= pred==meta[p]['H']
print(f"acerto leave-one-out: {hit}/{len(herb)} = {hit/len(herb)*100:.0f}%  (chance = {max(hands.values())/len(herb)*100:.0f}% se chutasse sempre a mao majoritaria)")
print("confusao (real -> previsto):", dict(conf))

print("\ntrocas de mao que NAO envolvem a mao 1 (B -> B), na mesma secao:")
bb=[x for x in diff_hand if '1' not in (x[3],x[4])]
for d,a,b,h1,h2 in sorted(bb,reverse=True): print(f"    {a:6s}(mao {h1}) -> {b:6s}(mao {h2})  JS={d:.4f}")
if bb: print(f"  media B->B: {statistics.mean(x[0] for x in bb):.4f}   vs mesma mao {statistics.mean(x[0] for x in same_hand):.4f}   vs trocas com a mao 1: {statistics.mean(x[0] for x in diff_hand if '1' in (x[3],x[4])):.4f}")
# mesma mao, mas paginas por mao 2/3/5 apenas (baseline B)
sb=[x[0] for x in same_hand if x[3]!='1']
print(f"  baseline mesma mao, so maos 2/3/5: media {statistics.mean(sb):.4f} (n={len(sb)})")
