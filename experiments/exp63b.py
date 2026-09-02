# Exp 63b: sem espacos, existem trechos longos repetidos? (a "ausencia de frases repetidas" depende dos espacos?)
import re, random
from collections import Counter
from exp51 import voy_words
import xml.etree.ElementTree as ET
def stream_lines_voy():
    out=[]
    for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','',t)
        s=re.sub(r'[^a-z]','',t)
        if s: out.append(s)
    return out
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
voyL=stream_lines_voy(); voyS=''.join(voyL)
N=len(voyS); print('glifos',N)
lat=''.join(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split())[:N]
por=''.join(xw('Portuguese.xml'))[:N]
nai=''.join(re.sub(r'[^a-z]','',l) for l in open('naibbe/encrypted/lat_output_ciphertext.txt'))[:N]
def rep_substrings(s,k):
    c=Counter(s[i:i+k] for i in range(len(s)-k+1))
    r=[(x,n) for x,n in c.items() if n>1]
    return len(r), max(r,key=lambda x:x[1]) if r else None
print(f"{'texto':22s} "+' '.join(f'{k:>8d}' for k in [10,12,15,18,20,25,30]))
for name,s in [('Voynich (sem espacos)',voyS),('latim (sem espacos)',lat),('portugues (sem esp.)',por),('Naibbe (sem espacos)',nai)]:
    print(f"{name:22s} "+' '.join(f'{rep_substrings(s,k)[0]:8d}' for k in [10,12,15,18,20,25,30]))
# os trechos mais longos repetidos do Voynich e onde a EVA os corta
for k in [20,16,14]:
    n,best=rep_substrings(voyS,k)
    if best: print(f"\ntrecho de {k} glifos mais repetido: '{best[0]}' x{best[1]}")
# como a EVA segmenta as ocorrencias do trecho mais repetido de 14 glifos?
n,best=rep_substrings(voyS,14); tgt=best[0]
segs=Counter()
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','',t)
    t=re.sub(r'[^a-z.,]','',t)
    s=t.replace('.','').replace(',','')
    i=s.find(tgt)
    while i>=0:
        # reconstruir a segmentacao EVA desse trecho
        j=0; out=''; cnt=0
        for c in t:
            if c.isalpha():
                if cnt>=i and cnt<i+len(tgt): out+=c
                cnt+=1
            elif cnt>i and cnt<i+len(tgt): out+='|'
        segs[out]+=1; i=s.find(tgt,i+1)
print(f"segmentacoes EVA das ocorrencias de '{tgt}':", dict(segs))
