# Exp 76: "tecnica compartilhada, seguida de forma desleixada do comeco ao fim"?
# (a) deriva ao longo do livro (por escriba), (b) taxa de violacao das regras mais fortes, (c) habito (distribuicoes enviesadas) vs tabela+dado (planas)
import re, math, random, statistics
from collections import Counter, defaultdict
from scipy.stats import spearmanr
from exp49 import ed1
random.seed(1)
pages={}; meta={}; order=[]; plines={}
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip(); m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',r)
    if m:
        pg=m.group(1); t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
        if not ws: continue
        pages.setdefault(pg,[]).extend(ws); plines.setdefault(pg,[]).append(ws)
        if pg not in order: order.append(pg)
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))
def folio_num(pg):
    m=re.match(r'f(\d+)',pg); return int(m.group(1))
def page_metrics(pg):
    ws=pages[pg]; ls=plines[pg]
    if len(ws)<80: return None
    adj=sum(ed1(a,b) for l in ls for a,b in zip(l,l[1:]))/max(1,sum(len(l)-1 for l in ls))
    og=sum(1 for w in ws if w[:2] in ('ot','ok','op','of'))/len(ws)
    qo=sum(1 for w in ws if w.startswith('qo'))/len(ws)
    L=sum(map(len,ws))/len(ws)
    # memoria da linha de cima
    hit=tot=0
    for i in range(1,len(ls)):
        for w in ls[i]:
            tot+=1; hit+=any(ed1(w,u) for u in ls[i-1])
    mem=hit/tot if tot else float('nan')
    ttr=len(set(ws[:80]))/80
    return dict(n=len(ws),tam=L,viz1=adj,mem=mem,og=og,qo=qo,ttr=ttr)
print("(a) deriva ao longo do livro: correlacao de Spearman entre a posicao no codice e cada medida, por escriba")
for hand in ['1','2','3']:
    pgs=[pg for pg in order if meta.get(pg,{}).get('H')==hand and page_metrics(pg)]
    if len(pgs)<10: continue
    xs=[folio_num(pg) for pg in pgs]; M=[page_metrics(pg) for pg in pgs]
    out=[]
    for key in ['tam','viz1','mem','og','qo','ttr']:
        ys=[m[key] for m in M]; rho,p=spearmanr(xs,ys); out.append(f"{key} {rho:+.2f} (p={p:.2f})")
    print(f"  escriba {hand}: {len(pgs)} paginas, folios {min(xs)}-{max(xs)}:  "+'  '.join(out))
    # primeiro terco vs ultimo terco
    k=len(pgs)//3
    a=[page_metrics(pg) for pg in pgs[:k]]; b=[page_metrics(pg) for pg in pgs[-k:]]
    print(f"     inicio vs fim: tamanho {statistics.mean(m['tam'] for m in a):.2f}->{statistics.mean(m['tam'] for m in b):.2f}  vizinhas {statistics.mean(m['viz1'] for m in a)*100:.1f}%->{statistics.mean(m['viz1'] for m in b)*100:.1f}%  memoria linha {statistics.mean(m['mem'] for m in a)*100:.1f}%->{statistics.mean(m['mem'] for m in b)*100:.1f}%  qo- {statistics.mean(m['qo'] for m in a)*100:.1f}%->{statistics.mean(m['qo'] for m in b)*100:.1f}%")

# (b) violacoes das regras mais fortes (nivel do glifo, com espaco)
S=' '.join(' '.join(pages[pg]) for pg in order)
bi=Counter(zip(S,S[1:])); uni=Counter(S)
print("\n(b) as regras mais rigidas e quantas vezes foram quebradas:")
rules=[]
for a in uni:
    if uni[a]<300 or a==' ': continue
    b,c=max(((b,c) for (x,b),c in bi.items() if x==a),key=lambda t:t[1])
    tot=sum(c for (x,_),c in bi.items() if x==a)
    rules.append((c/tot,a,b,tot-c,tot))
for p,a,b,viol,tot in sorted(rules,reverse=True)[:8]:
    bb='espaco' if b==' ' else b
    print(f"   depois de '{a}' vem '{bb}': {p*100:5.1f}%  (quebrada {viol} vezes em {tot})")
# regras de posicao
words=[w for pg in order for w in pages[pg]]
print(f"   'q' e seguido de 'o': {sum(1 for w in words for i,c in enumerate(w[:-1]) if c=='q' and w[i+1]=='o')/max(1,sum(w.count('q') for w in words))*100:.1f}%")
print(f"   'q' e inicial de palavra: {sum(1 for w in words if w[0]=='q')/max(1,sum(1 for w in words if 'q' in w))*100:.1f}%")
print(f"   'm' e final de palavra: {sum(1 for w in words if w[-1]=='m')/max(1,sum(1 for w in words if 'm' in w))*100:.1f}%")
print(f"   'n' e final de palavra: {sum(1 for w in words if w[-1]=='n')/max(1,sum(1 for w in words if 'n' in w))*100:.1f}%")

# (c) habito ou tabela? forma das distribuicoes de sucessores (contexto de 2 glifos)
ctx=defaultdict(Counter)
for i in range(2,len(S)): ctx[S[i-2:i]][S[i]]+=1
def shape(ctxs):
    ratios=[]; tops=[]
    for c,succ in ctxs.items():
        n=sum(succ.values())
        if n<200: continue
        k=len([s for s,v in succ.items() if v>=0.01*n])
        H=-sum(v/n*math.log2(v/n) for v in succ.values())
        ratios.append(H/math.log2(k) if k>1 else 1.0); tops.append(max(succ.values())/n)
    return statistics.mean(ratios), statistics.mean(tops), len(ratios)
r,t,n=shape(ctx)
print(f"\n(c) forma das escolhas (contextos com >=200 ocorrencias, n={n}): entropia relativa media {r:.2f} (1,0 = opcoes igualmente provaveis, como dado; menor = habito enviesado); a opcao favorita leva em media {t*100:.0f}%")
# comparacao: mesma medida no latim e no texto Naibbe (tabela + baralho)
lat=' '.join(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:34119])
nai=' '.join(re.sub(r'[^a-z]','',w) for l in open('naibbe/encrypted/lat_output_ciphertext.txt') for w in l.split())[:len(S)]
for name,T in [('latim',lat),('Naibbe (tabela + baralho)',nai)]:
    c2=defaultdict(Counter)
    for i in range(2,len(T)): c2[T[i-2:i]][T[i]]+=1
    r,t,n=shape(c2); print(f"    {name:26s}: entropia relativa {r:.2f}; favorita {t*100:.0f}%")
