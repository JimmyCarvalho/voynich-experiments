# Exp 77: um mecanismo que RODA deixaria periodicidade. Autocorrelacao das escolhas por posicao (lag 1..80) e regularidade dos intervalos
import re, math, random, statistics
import numpy as np
from collections import Counter
from exp51 import voy_words
from exp66 import train, gen_line
random.seed(3)
ws=voy_words()
OPEN=['qok','qot','qo','ok','ot','ch','sh','che','she','d','s','o','y','l','r','k','t','p','f','a','e','c']
def opener(w):
    for o in sorted(OPEN,key=len,reverse=True):
        if w.startswith(o): return o
    return w[0]
CLOSE=['aiin','ain','eedy','edy','ody','eey','ey','chy','dy','y','ar','or','al','ol','am','an','in','n','m','r','l','s','d','o']
def closer(w):
    for c in sorted(CLOSE,key=len,reverse=True):
        if w.endswith(c): return c
    return w[-1]
def autocorr_spectrum(series, maxlag=80):
    # serie categorica -> indicadores das 8 classes mais comuns; media da autocorrelacao
    cats=[c for c,_ in Counter(series).most_common(8)]
    out=np.zeros(maxlag+1)
    for c in cats:
        x=np.array([1.0 if s==c else 0.0 for s in series]); x=x-x.mean(); v=np.dot(x,x)
        for lag in range(1,maxlag+1): out[lag]+=np.dot(x[:-lag],x[lag:])/v
    return out/len(cats)
def report(name,words):
    for lab,f in [('abertura',opener),('fechamento',closer),('tamanho',len)]:
        s=[f(w) for w in words]; ac=autocorr_spectrum(s)
        base=ac[10:80]; peaks=[(lag,ac[lag]) for lag in range(2,81) if ac[lag]>base.mean()+4*base.std() and ac[lag]>0.02]
        print(f"  {name:22s} {lab:11s} lag1 {ac[1]:+.3f}  lag2 {ac[2]:+.3f}  lag3 {ac[3]:+.3f}  media lags 10-80 {base.mean():+.4f} (dp {base.std():.4f})  picos: {[(l,round(v,3)) for l,v in peaks] or 'nenhum'}")
print("autocorrelacao das classes de abertura/fechamento/tamanho por posicao da palavra (um mecanismo girando com N posicoes daria pico no lag N):")
report('Voynich',ws)
ctx=train(3); gen=[]
while len(gen)<len(ws): gen+=[w for w in gen_line(ctx,3).split() if w]
report('cadeia ordem 3',gen[:len(ws)])
# regularidade dos intervalos entre usos do mesmo bloco de abertura (mecanico = regular, CV baixo; aleatorio = CV~1)
print("\nintervalos entre usos consecutivos da mesma abertura (CV = desvio/media; passo mecanico fixo daria CV perto de 0):")
for name,words in [('Voynich',ws),('cadeia ordem 3',gen[:len(ws)])]:
    ops=[opener(w) for w in words]; row=[]
    for o,_ in Counter(ops).most_common(6):
        pos=[i for i,x in enumerate(ops) if x==o]; gaps=np.diff(pos)
        row.append(f"{o} CV={gaps.std()/gaps.mean():.2f}")
    print(f"  {name:16s} "+'  '.join(row))
