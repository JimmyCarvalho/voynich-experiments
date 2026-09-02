# Exp 66: modelo nulo "Markov de ordem 2 nos glifos (com o espaco como simbolo)" reproduz o que da bateria?
import re, math, random
from collections import Counter, defaultdict
from exp64 import voy_lines
from exp57 import battery, show, ref, pages_of
random.seed(7)
lines=[' '.join(ws) for ws in voy_lines()]
def train(k):
    ctx=defaultdict(Counter)
    for s in lines:
        s='^'*k+s+'$'
        for i in range(k,len(s)): ctx[s[i-k:i]][s[i]]+=1
    return ctx
def gen_line(ctx,k,maxlen=120):
    s='^'*k
    while len(s)<maxlen+k:
        c=ctx.get(s[-k:])
        if not c: break
        syms=list(c); w=[c[x] for x in syms]
        x=random.choices(syms,w)[0]
        if x=='$': break
        s+=x
    return s[k:]
print(f"{'configuracao':42s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}")
show('Voynich (referencia)',ref)
for k in [1,2,3,4]:
    ctx=train(k); out=[]
    while sum(len(l) for l in out)<34119*1.02:
        ws=gen_line(ctx,k).split()
        ws=[w for w in ws if w]
        if ws: out.append(ws)
    show(f'Markov ordem {k} nos glifos',battery(pages_of(out)))
