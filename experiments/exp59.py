# Exp 59: cifra Naibbe com ESCALA DE TABELAS dependente do ultimo glifo (regra de mao) -> recupera a MI atraves do espaco?
import re, json, sys
from exp57 import battery, pages_of, hybrid, show, ref
def lines_of(path):
    L=[]
    for l in open(path):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]; ws=[w for w in ws if w]
        if ws: L.append(ws)
    return L
sched=pages_of(lines_of('naibbe/encrypted/lat_sched.txt'))
print(f"{'configuracao':42s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}")
show('Voynich (referencia)',ref)
out={}
b=battery(sched); out['sched']=b; show('Naibbe com escala por ultimo glifo',b); sys.stdout.flush()
import random; random.seed(21)
for p in [0.05,0.08]:
    b=battery(hybrid(sched,p,exact=0.15)); out[f'sched+p{p}']=b; show(f'  + enchimento p={p:.2f} (copia exata 15%)',b); sys.stdout.flush()
json.dump(out,open('exp59.json','w'),indent=1)
