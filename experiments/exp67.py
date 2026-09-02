# Exp 67: modelo completo de 2 ingredientes: Markov ordem 3 nos glifos + fracao p de copia local (com edicao)
import random, sys
from exp66 import train, gen_line
from exp57 import battery, show, ref, pages_of, hybrid
print(f"{'configuracao':42s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}")
show('Voynich (referencia)',ref)
random.seed(3); ctx=train(3); out=[]
while sum(len(l) for l in out)<34119*1.15:
    ws=[w for w in gen_line(ctx,3).split() if w]
    if ws: out.append(ws)
base=pages_of(out)
for p,ex in [(0.04,0.4),(0.06,0.4),(0.08,0.4),(0.06,0.6)]:
    random.seed(11)
    show(f'Markov 3 + copia local p={p:.2f} (exata {int(ex*100)}%)',battery(hybrid(base,p,exact=ex))); sys.stdout.flush()
