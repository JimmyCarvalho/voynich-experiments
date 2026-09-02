# Exp 73: cadeia + copia de QUALQUER lugar da pagina (peso caindo com a distancia) reproduz a correlacao de longo alcance?
import random, math, sys
import numpy as np
from exp66 import train, gen_line
from exp57 import battery, show, ref, pages_of
from exp72 import dfa, series_rank, series_len, voy
random.seed(21)
def hybrid_page(pages, p, exact=0.35, decay=1.0):
    glyphs=[g for pg in pages for l in pg for w in l for g in w]
    out=[]
    for pg in pages:
        new=[]
        for li,line in enumerate(pg):
            nl=[]
            for k,w in enumerate(line):
                if random.random()<p and (li>0 or k>0):
                    # fonte: palavra anterior na pagina, peso ~ 1/(1+dist_linhas)^decay
                    cands=[]; wts=[]
                    for lj in range(li):
                        for u in new[lj]: cands.append(u); wts.append(1/(1+(li-lj))**decay)
                    for u in nl: cands.append(u); wts.append(1.0)
                    src=random.choices(cands,wts)[0]
                    if random.random()<exact: nl.append(src)
                    else:
                        s=list(src); op=random.random()
                        if op<0.5: s[random.randrange(len(s))]=random.choice(glyphs)
                        elif op<0.75: s.insert(random.randrange(len(s)+1),random.choice(glyphs))
                        elif len(s)>2: del s[random.randrange(len(s))]
                        nl.append(''.join(s))
                else: nl.append(w)
            new.append(nl)
        out.append(new)
    return out
ctx=train(3); out=[]
while sum(len(l) for l in out)<34119*1.15:
    ws=[w for w in gen_line(ctx,3).split() if w]
    if ws: out.append(ws)
# paginas com tamanho parecido com o real (~20 linhas)
base=pages_of(out,20)
print(f"{'configuracao':44s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}  alpha(rank) alpha(tam)")
def row(name,pages):
    b=battery(pages); ws=[w for pg in pages for l in pg for w in l][:34119]
    show(name,b); print(f"{'':44s} {'':66s} {dfa(series_rank(ws)):.3f}       {dfa(series_len(ws)):.3f}")
row('Voynich (referencia)',None) if False else None
show('Voynich (referencia)',ref); print(f"{'':44s} {'':66s} {dfa(series_rank(voy)):.3f}       {dfa(series_len(voy)):.3f}")
for p,dec in [(0.04,1.0),(0.08,1.0),(0.08,0.5),(0.12,0.5)]:
    random.seed(7); row(f'cadeia 3 + copia na pagina p={p:.2f}, decaimento {dec}',hybrid_page(base,p,exact=0.35,decay=dec)); sys.stdout.flush()
