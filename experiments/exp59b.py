import re, json, sys, random
from exp57 import battery, pages_of, hybrid, show, ref
def lines_of(path):
    L=[]
    for l in open(path):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]; ws=[w for w in ws if w]
        if ws: L.append(ws)
    return L
print(f"{'configuracao':42s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}")
show('Voynich (referencia)',ref); out={}
for m in ['0.5','0.7']:
    d=pages_of(lines_of(f'naibbe/encrypted/lat_sched_{m}.txt'))
    b=battery(d); out[m]=b; show(f'escala por glifo, {int((1-float(m))*100)}% regra / {int(float(m)*100)}% dado',b); sys.stdout.flush()
    random.seed(3); b=battery(hybrid(d,0.06,exact=0.15)); out[m+'+p']=b; show(f'  + enchimento p=0.06',b); sys.stdout.flush()
json.dump(out,open('exp59b.json','w'),indent=1)
