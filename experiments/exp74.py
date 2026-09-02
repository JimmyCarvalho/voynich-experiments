# Exp 74: terceiro ingrediente: cada pagina tem seu proprio "vies" nos habitos (reponderacao aleatoria da cadeia por pagina)
import random, math, sys
import numpy as np
from collections import Counter, defaultdict
from exp66 import train
from exp57 import battery, show, ref, hybrid
from exp72 import dfa, series_rank, series_len, voy
random.seed(3)
ctx=train(3)
syms=sorted(set(s for c in ctx.values() for s in c))
def gen_page(ctx, nlines, sigma, k=3):
    bias={s:math.exp(sigma*random.gauss(0,1)) for s in syms}   # vies da pagina, constante na pagina
    lines=[]
    for _ in range(nlines):
        s='^'*k
        while len(s)<120+k:
            c=ctx.get(s[-k:])
            if not c: break
            opts=list(c); w=[c[x]*bias.get(x,1.0) for x in opts]
            x=random.choices(opts,w)[0]
            if x=='$': break
            s+=x
        ws=[w for w in s[k:].split() if w]
        if ws: lines.append(ws)
    return lines
def build(sigma,p_copy=0.04):
    pages=[]
    while sum(len(l) for pg in pages for l in pg)<34119*1.15:
        pages.append(gen_page(ctx,20,sigma))
    random.seed(11); return hybrid(pages,p_copy,exact=0.4)
print(f"{'configuracao':40s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}   alpha(rank) alpha(tam)")
show('Voynich (referencia)',ref); print(f"{'':40s} {'':66s} {dfa(series_rank(voy)):.3f}       {dfa(series_len(voy)):.3f}")
for sigma in [0.0,0.3,0.5,0.7]:
    random.seed(5); pages=build(sigma); b=battery(pages); ws=[w for pg in pages for l in pg for w in l][:34119]
    show(f'cadeia 3 + vies por pagina sigma={sigma} + copia 4%',b); print(f"{'':40s} {'':66s} {dfa(series_rank(ws)):.3f}       {dfa(series_len(ws)):.3f}"); sys.stdout.flush()
