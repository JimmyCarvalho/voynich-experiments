# Exp 64: descoberta de unidades pela ENTROPIA DE RAMIFICACAO (Harris 1955 / Tanaka-Ishii 2006), sem usar os espacos
# fronteira = ponto onde a incerteza sobre o proximo glifo (para frente) e sobre o anterior (para tras) sobe
import re, math, random
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET
random.seed(1)
def voy_lines():
    out=[]
    for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','',t)
        t=re.sub(r'[^a-z.,]','',t).strip('.,').replace(',','.')
        ws=[w for w in t.split('.') if w]
        if ws: out.append(ws)
    return out
def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
def to_lines(words,per=9):
    return [words[i:i+per] for i in range(0,len(words),per)]
def nai_lines():
    out=[]
    for l in open('naibbe/encrypted/lat_output_ciphertext.txt'):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]; ws=[w for w in ws if w]
        if ws: out.append(ws)
    return out

def branching(lines,k=2):
    """retorna, por linha, o fluxo de glifos, as posicoes de espaco reais, e o escore de fronteira por posicao"""
    fwd=defaultdict(Counter); bwd=defaultdict(Counter)
    streams=[]
    for ws in lines:
        s=''.join(ws); streams.append(s)
        for i in range(len(s)):
            if i>=k: fwd[s[i-k:i]][s[i]]+=1
            if i+k<len(s): bwd[s[i+1:i+1+k]][s[i]]+=1
    def H(c):
        n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
    Hf={ctx:H(c) for ctx,c in fwd.items()}; Hb={ctx:H(c) for ctx,c in bwd.items()}
    scores=[]; truth=[]
    for ws,s in zip(lines,streams):
        # posicoes de fronteira reais (apos o glifo i)
        cuts=set(); p=0
        for w in ws[:-1]: p+=len(w); cuts.add(p-1)
        sc=[]
        for i in range(len(s)-1):
            f=Hf.get(s[max(0,i-k+1):i+1],None) if i>=k-1 else None   # incerteza sobre s[i+1] dado os k anteriores
            b=Hb.get(s[i+1:i+1+k],None) if i+1+k<=len(s) else None     # incerteza sobre s[i] dado os k seguintes
            v=(f if f is not None else 0)+(b if b is not None else 0)
            sc.append(v)
        scores.append(sc); truth.append(cuts)
    return streams,scores,truth
def evaluate(lines,k=2,name=''):
    streams,scores,truth=branching(lines,k)
    allsc=sorted([v for sc in scores for v in sc],reverse=True)
    ncut=sum(len(t) for t in truth)
    thr=allsc[ncut-1]   # mesmo numero de fronteiras previstas que reais
    tp=fp=fn=0; inside=Counter()
    for s,sc,t in zip(streams,scores,truth):
        pred=set(i for i,v in enumerate(sc) if v>=thr)
        tp+=len(pred&t); fp+=len(pred-t); fn+=len(t-pred)
        for i in pred-t:   # fronteira prevista dentro de uma palavra: registra a junta
            inside[(s[i],s[i+1])]+=1
    P=tp/(tp+fp); R=tp/(tp+fn); F=2*P*R/(P+R)
    print(f"{name:26s} k={k}  precisao {P*100:5.1f}%  cobertura {R*100:5.1f}%  F={F*100:5.1f}%   cortes previstos dentro de palavras mais comuns: {', '.join(a+'|'+b+' '+str(n) for (a,b),n in inside.most_common(8))}")
    return F
voy=voy_lines()
N=34119
lat=to_lines(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N])
por=to_lines(xw('Portuguese.xml')[:N]); ale=to_lines(xw('German.xml')[:N])
nai=nai_lines()
for k in [2,3]:
    for name,data in [('Voynich',voy),('latim',lat),('portugues',por),('alemao',ale),('Naibbe (latim cifrado)',nai)]:
        evaluate(data,k,name)
    print()
