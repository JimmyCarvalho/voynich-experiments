# Exp 51: "e se os caracteres sao diferentes?" -> re-segmentar os glifos
import re, math, json
from collections import Counter
import xml.etree.ElementTree as ET

def voy_words(path='ZL3b-n.txt'):
    out=[]
    for raw in open(path,encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
        t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        out.extend(re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w))
    return out

def H2(seqs):
    """conditional entropy of unit given previous unit, over '#'+w+'#'"""
    bi=Counter(); uni=Counter()
    for s in seqs:
        u=['#']+list(s)+['#']
        for a,b in zip(u,u[1:]): bi[(a,b)]+=1; uni[a]+=1
    tot=sum(bi.values()); h=0.0
    for (a,b),c in bi.items():
        p=c/tot; h-= p*math.log2(c/uni[a])
    return h
def H1(seqs):
    uni=Counter(x for s in seqs for x in s); tot=sum(uni.values())
    return -sum(c/tot*math.log2(c/tot) for c in uni.values())

def seg(word, units):
    """greedy longest-match segmentation"""
    out=[]; i=0; n=len(word)
    while i<n:
        for L in (3,2,1):
            if i+L<=n and word[i:i+L] in units:
                out.append(word[i:i+L]); i+=L; break
        else:
            out.append(word[i]); i+=1
    return out

voy=voy_words()
print(f"palavras={len(voy)} glifos EVA={sum(map(len,voy))} alfabeto={len(set(''.join(voy)))}")

SEGS={
 'EVA (1 letra = 1 glifo)': set(),
 'ligaduras basicas (ch sh)': {'ch','sh'},
 'ch sh + benches com gallows (cth ckh cph cfh)': {'ch','sh','cth','ckh','cph','cfh'},
 'Currier-like (ch sh cth ckh cph cfh ee eee iin in iiin)': {'ch','sh','cth','ckh','cph','cfh','ee','eee','iin','iin','in','iiin','ii','iii'},
 'maximo (tudo que parece 1 traco)': {'ch','sh','cth','ckh','cph','cfh','ee','eee','ii','iii','iin','iiin','in','ain','aiin','aiiin','dy','ol','or','al','ar','qo','ey','edy'},
}
rows=[]
for name,units in SEGS.items():
    ss=[seg(w,units) for w in voy] if units else [list(w) for w in voy]
    alpha=len(set(x for s in ss for x in s)); L=sum(map(len,ss))/len(ss)
    rows.append((name,alpha,L,H1(ss),H2(ss)))
    print(f"{name:58s} alfabeto={alpha:3d} unid/palavra={L:4.2f} H1={H1(ss):5.3f} H2={H2(ss):5.3f}")

# controles: mesma "má segmentação" aplicada a linguas reais
def words_from_xml(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:34000]
por=words_from_xml('Portuguese.xml')[:34000]
ale=words_from_xml('German.xml')[:34000]
print()
print("controles: e se ESSAS linguas fossem escritas com glifos compostos?")
LATSEG={'qu','ch','th','ph','sc','st','pr','tr','er','re','in','on','um','us','is','es','ae','ii','nt','it','ur','tu','di','de','au','ss','ll','ti'}
for nome,ws in [('latim',lat),('portugues',por),('alemao',ale)]:
    base=[list(w) for w in ws]
    comp=[seg(w,LATSEG) for w in ws]
    print(f"{nome:12s} letra a letra: alfabeto={len(set(''.join(ws))):2d} H2={H2(base):5.3f}   |  com 28 digrafos: alfabeto={len(set(x for s in comp for x in s)):3d} unid/pal={sum(map(len,comp))/len(comp):4.2f} H2={H2(comp):5.3f}")
