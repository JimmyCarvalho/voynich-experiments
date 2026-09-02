# Exp 54: os ROTULOS (nos potes, nas plantas, nas estrelas) se comportam como NOMES?
import re, math, statistics, random
from collections import Counter, defaultdict
random.seed(4)
loci=defaultdict(list); meta={}; pagemeta=defaultdict(list)
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip()
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])([A-Za-z][a-z0-9]*)>\s*(.*)',r)
    if m:
        pg,typ=m.group(1),m.group(4)
        t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
        t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
        base=re.sub(r'[0-9]','',typ)
        loci[base].append((pg,ws))
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))

LAB={'L':'rotulo solto','Lz':'rotulo do zodiaco','Lf':'rotulo de planta (farmacia)','Ls':'rotulo de estrela','Ln':'rotulo de ninfa','Lc':'rotulo circular','Lt':'rotulo de texto'}
par=[w for pg,ws in loci['P'] for w in ws]
print(f"texto corrido: {len(par)} palavras, {len(set(par))} tipos, TTR={len(set(par))/len(par):.3f}")
print()
print(f"{'tipo':30s} {'itens':>6s} {'palavras':>8s} {'pal/item':>8s} {'tipos':>6s} {'TTR':>6s} {'hapax':>6s} {'tam':>5s}")
alllab=[]
for k,name in LAB.items():
    if k not in loci: continue
    items=loci[k]; ws=[w for pg,l in items for w in l]
    if len(ws)<40: continue
    alllab+=ws
    hap=sum(1 for w,c in Counter(ws).items() if c==1)/len(set(ws))
    print(f"{name:30s} {len(items):6d} {len(ws):8d} {len(ws)/len(items):8.2f} {len(set(ws)):6d} {len(set(ws))/len(ws):6.3f} {hap*100:5.0f}% {sum(map(len,ws))/len(ws):5.2f}")
hp=sum(1 for w,c in Counter(par).items() if c==1)/len(set(par))
print(f"{'TEXTO CORRIDO (comparacao)':30s} {len(loci['P']):6d} {len(par):8d} {len(par)/len(loci['P']):8.2f} {len(set(par)):6d} {len(set(par))/len(par):6.3f} {hp*100:5.0f}% {sum(map(len,par))/len(par):5.2f}")

# controle justo: amostras do texto corrido do MESMO tamanho que o conjunto de rotulos
n=len(alllab)
sub=[]
for _ in range(200):
    s=random.sample(par,n); sub.append((len(set(s))/n, sum(1 for w,c in Counter(s).items() if c==1)/len(set(s))))
ttr_lab=len(set(alllab))/n; hap_lab=sum(1 for w,c in Counter(alllab).items() if c==1)/len(set(alllab))
m_t=statistics.mean(x[0] for x in sub); s_t=statistics.pstdev(x[0] for x in sub)
m_h=statistics.mean(x[1] for x in sub); s_h=statistics.pstdev(x[1] for x in sub)
print(f"\nTODOS os rotulos juntos: {n} palavras, TTR={ttr_lab:.3f}, hapax={hap_lab*100:.0f}%")
print(f"amostra do texto corrido do mesmo tamanho: TTR={m_t:.3f} (dp {s_t:.3f})  ->  z={(ttr_lab-m_t)/s_t:+.1f}")
print(f"                                           hapax={m_h*100:.0f}% (dp {s_h*100:.1f}) ->  z={(hap_lab-m_h)/s_h:+.1f}")

# os rotulos usam o mesmo "idioma"? entropia cruzada rotulos <-> texto corrido
def model(words,n=3):
    ctx=Counter(); ng=Counter()
    for w in words:
        s='#'*(n-1)+w+'#'
        for i in range(len(s)-n+1): ng[s[i:i+n]]+=1; ctx[s[i:i+n-1]]+=1
    return ng,ctx,len(set(''.join(words)))+1
def xent(words,M,n=3):
    ng,ctx,V=M; tot=0; lp=0.0
    for w in words:
        s='#'*(n-1)+w+'#'
        for i in range(len(s)-n+1):
            lp+=math.log2((ng.get(s[i:i+n],0)+0.5)/(ctx.get(s[i:i+n-1],0)+0.5*V)); tot+=1
    return -lp/tot
Mp=model(par); Ml=model(alllab)
print(f"\nmodelo do texto corrido aplicado aos rotulos: {xent(alllab,Mp):.3f} bits (proprio: {xent(alllab,Ml):.3f}) -> penalidade +{xent(alllab,Mp)-xent(alllab,Ml):.3f}")
print(f"modelo dos rotulos aplicado ao texto corrido: {xent(par,Ml):.3f} bits (proprio: {xent(par,Mp):.3f}) -> penalidade +{xent(par,Ml)-xent(par,Mp):.3f}")

# quantos rotulos aparecem tambem no texto corrido da MESMA pagina?
hit=tot=0
for k in LAB:
    for pg,ws in loci.get(k,[]):
        page_par=set(w for p2,l in loci['P'] if p2==pg for w in l)
        for w in ws:
            tot+=1
            if w in page_par: hit+=1
print(f"\nrotulos que reaparecem no texto da MESMA pagina: {hit}/{tot} = {hit/tot*100:.1f}%")
allpar=set(par)
h2=sum(1 for k in LAB for pg,ws in loci.get(k,[]) for w in ws if w in allpar)
print(f"rotulos que aparecem em QUALQUER lugar do texto corrido: {h2}/{tot} = {h2/tot*100:.1f}%")
