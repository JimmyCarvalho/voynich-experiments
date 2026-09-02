# Exp 72b: a correlacao e livre de escala (fractal) ou tem uma escala preferida (pagina)? inclinacoes locais do DFA
import numpy as np, math, random, re
from collections import Counter
from exp72 import voy, blockS, lat, por, gen, series_len, series_rank
random.seed(1)
def dfa_curve(x):
    x=np.asarray(x,float); x=x-x.mean(); y=np.cumsum(x); n=len(y)
    scales=np.unique(np.logspace(np.log10(8),np.log10(n//6),22).astype(int)); F=[]
    for s in scales:
        m=n//s; segs=y[:m*s].reshape(m,s); t=np.arange(s)
        F.append(np.sqrt(np.mean([np.mean((seg-np.polyval(np.polyfit(t,seg,1),t))**2) for seg in segs])))
    return scales,np.array(F)
def local_slopes(x,bands=((8,40),(40,200),(200,1000),(1000,10000))):
    s,F=dfa_curve(x); out=[]
    for lo,hi in bands:
        m=(s>=lo)&(s<=hi)
        out.append(np.polyfit(np.log(s[m]),np.log(F[m]),1)[0] if m.sum()>=3 else float('nan'))
    return out
print("inclinacao local do DFA (serie log-rank), por faixa de escala em palavras:")
print(f"{'texto':26s} {'8-40':>8s} {'40-200':>8s} {'200-1000':>9s} {'1000+':>8s}")
for name,ws in [('Voynich',voy),('Voynich, estrelas/mao 3',blockS),('cadeia ordem 3',gen),('latim',lat),('portugues',por)]:
    sl=local_slopes(series_rank(ws)); print(f"{name:26s} "+' '.join(f'{v:8.3f}' for v in sl))
print("\nmesma coisa, serie tamanho da palavra:")
for name,ws in [('Voynich',voy),('Voynich, estrelas/mao 3',blockS),('cadeia ordem 3',gen),('latim',lat),('portugues',por)]:
    sl=local_slopes(series_len(ws)); print(f"{name:26s} "+' '.join(f'{v:8.3f}' for v in sl))
# controle: embaralhar as LINHAS dentro de cada pagina (mata a estrutura dentro da pagina, mantem a pagina)
from exp49 import parse
pg=parse('ZL3b-n.txt')
def flat(pages): return [w for lines in pages for l in lines for w in l]
def shuffle_lines(pages):
    out=[]
    for lines in pages:
        l=list(lines); random.shuffle(l); out.append(l)
    return out
def shuffle_pages(pages):
    p=list(pages); random.shuffle(p); return p
def shuffle_words_in_page(pages):
    out=[]
    for lines in pages:
        ws=[w for l in lines for w in l]; random.shuffle(ws); out.append([ws])
    return out
print("\ncontroles de escala (serie log-rank, expoente global):")
from exp72 import dfa
for name,data in [('Voynich original',pg),('palavras embaralhadas dentro da pagina',shuffle_words_in_page(pg)),('linhas embaralhadas dentro da pagina',shuffle_lines(pg)),('paginas embaralhadas (ordem das paginas)',shuffle_pages(pg))]:
    print(f"  {name:42s} alpha={dfa(series_rank(flat(data))):.3f}")
