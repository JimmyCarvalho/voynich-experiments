# Exp 53b: a gramatica de um escriba prediz as palavras dos outros?
import re, math, statistics, json
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET
from exp53 import scribe   # reaproveita o parse

def model(words,n=3):
    ctx=Counter(); ng=Counter()
    for w in words:
        s='#'*(n-1)+w+'#'
        for i in range(len(s)-n+1):
            ng[s[i:i+n]]+=1; ctx[s[i:i+n-1]]+=1
    V=len(set(''.join(words)))+1
    return ng,ctx,V
def xent(words,M,n=3):
    ng,ctx,V=M; tot=0; lp=0.0
    for w in words:
        s='#'*(n-1)+w+'#'
        for i in range(len(s)-n+1):
            c=ng.get(s[i:i+n],0); d=ctx.get(s[i:i+n-1],0)
            lp+=math.log2((c+0.5)/(d+0.5*V)); tot+=1
    return -lp/tot

S=sorted(scribe)
big=[h for h in S if len(scribe[h])>2000]
print("entropia cruzada (bits/glifo): modelo do escriba LINHA aplicado ao texto do escriba COLUNA")
print("        "+"  ".join(f"esc{h}" for h in big))
M={h:model(scribe[h]) for h in big}
cross=[]
for a in big:
    row=[]
    for b in big:
        v=xent(scribe[b],M[a]); row.append(v)
        if a!=b: cross.append(v-xent(scribe[b],M[b]))
    print(f"  esc{a}  "+"  ".join(f"{v:.2f}" for v in row))
print(f"\npenalidade media ao usar o modelo do OUTRO escriba: +{statistics.mean(cross):.3f} bits")

# vocabulario compartilhado
for a in big:
    for b in big:
        if a<b:
            A,B=set(scribe[a]),set(scribe[b])
            print(f"  vocabulario esc{a} x esc{b}: sobreposicao Jaccard {len(A&B)/len(A|B)*100:.1f}%")

# controles
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
langs={'pt':xw('Portuguese.xml')[:11000],'de':xw('German.xml')[:11000],'fi':xw('Finnish.xml')[:11000],'tr':xw('Turkish.xml')[:11000]}
ML={k:model(v) for k,v in langs.items()}
pen=[xent(langs[b],ML[a])-xent(langs[b],ML[b]) for a in langs for b in langs if a!=b]
print(f"\ncontrole, LINGUAS diferentes: penalidade media +{statistics.mean(pen):.3f} bits")
pt=xw('Portuguese.xml'); blocks={i:pt[i*11000:(i+1)*11000] for i in range(4)}
MB={k:model(v) for k,v in blocks.items()}
pen2=[xent(blocks[b],MB[a])-xent(blocks[b],MB[b]) for a in blocks for b in blocks if a!=b]
jac=[]
for a in blocks:
    for b in blocks:
        if a<b:
            A,B=set(blocks[a]),set(blocks[b]); jac.append(len(A&B)/len(A|B))
print(f"controle, 4 blocos do MESMO texto (portugues): penalidade media +{statistics.mean(pen2):.3f} bits, Jaccard medio {statistics.mean(jac)*100:.1f}%")
json.dump({'penalidade_escribas':statistics.mean(cross),'penalidade_linguas':statistics.mean(pen),'penalidade_mesmo_texto':statistics.mean(pen2)},open('exp53b.json','w'))
