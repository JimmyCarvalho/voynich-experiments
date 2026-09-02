# Exp 52: busca gulosa pela MELHOR segmentacao possivel do Voynich (a favor da hipotese)
import re, math, json
from collections import Counter
from exp51 import voy_words, H2, H1
import xml.etree.ElementTree as ET

def h2_of(seqs):
    return H2(seqs)

def merge_pass(seqs, banned=set()):
    """acha o par adjacente cuja fusao mais aumenta H2"""
    # candidatos: bigramas frequentes
    bi=Counter()
    for s in seqs:
        for a,b in zip(s,s[1:]): bi[(a,b)]+=1
    best=None
    for pair,c in bi.most_common(40):
        if pair in banned: continue
        new=[]
        for s in seqs:
            o=[];i=0
            while i<len(s):
                if i+1<len(s) and (s[i],s[i+1])==pair: o.append(s[i]+s[i+1]); i+=2
                else: o.append(s[i]); i+=1
            new.append(o)
        h=h2_of(new)
        if best is None or h>best[0]: best=(h,pair,new)
    return best

voy=voy_words()
seqs=[list(w) for w in voy]
h=h2_of(seqs)
print(f"partida EVA: alfabeto={len(set(''.join(voy)))} unid/pal={sum(map(len,seqs))/len(seqs):.2f} H2={h:.3f}")
hist=[]
for step in range(1,13):
    r=merge_pass(seqs)
    if r is None: break
    h,pair,seqs=r
    alpha=len(set(x for s in seqs for x in s)); L=sum(map(len,seqs))/len(seqs)
    hist.append((step,''.join(pair),alpha,L,h))
    print(f"  fusao {step:2d}: '{pair[0]}'+'{pair[1]}' -> '{''.join(pair)}'   alfabeto={alpha:3d} unid/pal={L:4.2f} H2={h:.3f}")

# mesmo procedimento aplicado ao latim (controle): quanto uma lingua real "ganha" com o mesmo truque?
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:34119]
ls=[list(w) for w in lat]
print(f"\ncontrole latim: H2 inicial={h2_of(ls):.3f}")
for step in range(1,13):
    r=merge_pass(ls)
    if r is None: break
    hl,pair,ls=r
    print(f"  fusao {step:2d}: '{''.join(pair)}'  alfabeto={len(set(x for s in ls for x in s)):3d} unid/pal={sum(map(len,ls))/len(ls):4.2f} H2={hl:.3f}")
json.dump({'voynich':hist},open('exp52.json','w'))
