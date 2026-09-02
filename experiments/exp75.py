# Exp 75: o efeito de pagina esta concentrado em PALAVRAS especificas (conteudo) ou espalhado nos habitos?
# estatistica: palavras que aparecem >=3 vezes numa pagina e em NENHUMA outra (exclusivas), e palavras >=3x na pagina e raras fora
import random, re, math, statistics
from collections import Counter, defaultdict
from exp49 import parse, latin_like
from exp66 import train
from exp74 import gen_page, ctx
from exp57 import hybrid
import xml.etree.ElementTree as ET
random.seed(2)
def exclusive_stats(pages_words):
    tot=Counter(w for pg in pages_words for w in pg)
    excl=0; concentrated=0; npg=0
    for pg in pages_words:
        c=Counter(pg); npg+=1
        for w,k in c.items():
            if k>=3:
                if tot[w]==k: excl+=1
                if k/tot[w]>=0.5: concentrated+=1
    return excl/npg, concentrated/npg
voy=parse('ZL3b-n.txt'); voyP=[[w for l in lines for w in l] for lines in voy]
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
latP=[[w for l in lines for w in l] for lines in latin_like(voy,lat)]
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
porP=[[w for l in lines for w in l] for lines in latin_like(voy,xw('Portuguese.xml'))]
def model_pages(sigma,p=0.04):
    pages=[]
    for lines in voy:   # mesmo numero de linhas por pagina que o real
        pages.append(gen_page(ctx,len(lines),sigma))
    random.seed(11); pages=hybrid(pages,p,exact=0.4)
    return [[w for l in pg for w in l] for pg in pages]
print(f"{'texto':40s} {'exclusivas (>=3x, so nessa pagina)':>34s} {'concentradas (>=3x, >=50% na pagina)':>36s}   por pagina")
for name,P in [('Voynich',voyP),('modelo: cadeia 3 + copia 4%',model_pages(0.0)),('modelo: + vies por pagina 0.5',model_pages(0.5)),('modelo: + vies por pagina 0.7',model_pages(0.7)),('latim (mesmas paginas)',latP),('portugues (mesmas paginas)',porP)]:
    e,c=exclusive_stats(P); print(f"{name:40s} {e:34.2f} {c:36.2f}")
# exemplos reais
tot=Counter(w for pg in voyP for w in pg)
ex=[]
for pg,lines in zip(voyP,voy):
    c=Counter(pg)
    for w,k in c.items():
        if k>=3 and tot[w]==k: ex.append((k,w))
ex.sort(reverse=True)
print("\nexemplos de palavras exclusivas de uma pagina no Voynich (vezes, palavra):", ex[:12])
