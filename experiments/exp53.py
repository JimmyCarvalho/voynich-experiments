# Exp 53: os 5 escribas compartilham a mesma "gramatica"?
import re, math, json, random
from collections import Counter, defaultdict
random.seed(9)

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

scribe=defaultdict(list); sec=defaultdict(Counter); quire=defaultdict(Counter)
for pg in order:
    h=meta.get(pg,{}).get('H'); 
    if not h: continue
    scribe[h].extend(pages[pg])
    sec[h][meta[pg].get('I','?')]+=len(pages[pg]); quire[h][meta[pg].get('Q','?')]+=1
print("escriba  palavras  tipos   TTR    secoes                          cadernos")
for h in sorted(scribe):
    w=scribe[h]; print(f"  {h}     {len(w):6d}  {len(set(w)):5d}  {len(set(w))/len(w):.3f}  {dict(sec[h].most_common(4))}  {''.join(sorted(quire[h]))}")

# ---- 1. gramatica de posicao: um glifo pode ocupar que fatia da palavra?
def slot_profile(words):
    """distribuicao de posicao relativa de cada glifo"""
    pos=defaultdict(list)
    for w in words:
        n=len(w)
        if n<2: continue
        for i,c in enumerate(w): pos[c].append(i/(n-1))
    return {c:sum(v)/len(v) for c,v in pos.items() if len(v)>=80}

profs={h:slot_profile(scribe[h]) for h in sorted(scribe)}
common=set.intersection(*[set(p) for p in profs.values()])
print(f"\nglifos comuns aos 5 escribas: {len(common)}")
import statistics
print("glifo  posicao media relativa por escriba (0=inicio, 1=fim)      desvio")
rows=[]
for c in sorted(common, key=lambda c: statistics.mean(profs[h][c] for h in profs)):
    vals=[profs[h][c] for h in sorted(profs)]
    rows.append((c,vals,statistics.pstdev(vals)))
    print(f"  {c}    {'  '.join(f'{v:.2f}' for v in vals)}    {statistics.pstdev(vals):.3f}")
print(f"\ndesvio medio entre escribas (mesmo glifo): {statistics.mean(r[2] for r in rows):.3f}")

# controle: desvio se dividissemos o texto em 5 blocos aleatorios de linguas DIFERENTES
import xml.etree.ElementTree as ET
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
langs={'portugues':xw('Portuguese.xml'),'hungaro':xw('Hungarian.xml'),'alemao':xw('German.xml'),
       'finlandes':xw('Finnish.xml'),'turco':xw('Turkish.xml')}
lp={k:slot_profile(v[:8000]) for k,v in langs.items()}
cl=set.intersection(*[set(p) for p in lp.values()])
d_lang=statistics.mean(statistics.pstdev([lp[k][c] for k in lp]) for c in cl)
print(f"controle, 5 LINGUAS diferentes (mesmo alfabeto latino, {len(cl)} letras comuns): desvio medio = {d_lang:.3f}")
# controle: 5 blocos do MESMO idioma
pt=langs['portugues']; blocks=[pt[i*8000:(i+1)*8000] for i in range(5)]
bp=[slot_profile(b) for b in blocks]; cb=set.intersection(*[set(p) for p in bp])
d_same=statistics.mean(statistics.pstdev([p[c] for p in bp]) for c in cb)
print(f"controle, 5 blocos do MESMO idioma (portugues): desvio medio = {d_same:.3f}")
json.dump({'desvio_escribas':statistics.mean(r[2] for r in rows),'desvio_5_linguas':d_lang,'desvio_mesmo_idioma':d_same},open('exp53a.json','w'))
