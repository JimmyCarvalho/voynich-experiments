# Exp 71: o nivel da PALAVRA carrega informacao alem da memoria de 3 glifos? (Voynich vs latim vs portugues)
# treina cadeia ordem 3 nas letras (com espaco) de cada corpus e compara as estatisticas de PALAVRA do gerado com as do real
import re, random, math, statistics
from collections import Counter, defaultdict
from exp64 import voy_lines, to_lines, xw
from exp66 import gen_line
from exp69 import heaps, zipf_slope, top_cov
random.seed(9)
def train_lines(S,k=3):
    ctx=defaultdict(Counter)
    for s in S:
        s='^'*k+s+'$'
        for i in range(k,len(s)): ctx[s[i-k:i]][s[i]]+=1
    return ctx
N=34119
corp={'Voynich':[' '.join(ws) for ws in voy_lines()],
      'latim':[' '.join(ws) for ws in to_lines(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N])],
      'portugues':[' '.join(ws) for ws in to_lines(xw('Portuguese.xml')[:N])]}
print(f"{'corpus':10s} {'':8s} {'TTR':>6s} {'tipos@10k':>9s} {'tipos@34k':>9s} {'Zipf':>7s} {'top100':>7s} {'top1000':>8s} {'% palavras geradas que existem no real':>38s}")
for name,S in corp.items():
    real=[w for s in S for w in s.split()][:N]
    ctx=train_lines(S); gen=[]
    while len(gen)<N: gen+=[w for w in gen_line(ctx,3).split() if w]
    gen=gen[:N]; lex=set(real)
    for lab,ws in [('real',real),('cadeia 3',gen)]:
        h=heaps(ws); inlex=sum(1 for w in ws if w in lex)/len(ws)
        print(f"{name:10s} {lab:8s} {len(set(ws))/len(ws):6.3f} {h[10000]:9d} {h[34000]:9d} {zipf_slope(ws):7.3f} {top_cov(ws,100):7.3f} {top_cov(ws,1000):8.3f} {inlex*100:37.0f}%")
