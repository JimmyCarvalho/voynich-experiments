# Exp 55b: a memoria da linha de cima existe na cifra Naibbe?
import re, random, statistics
from collections import Counter
from exp49 import ed1, parse
random.seed(6)
def lines_of(path):
    L=[]
    for l in open(path):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]
        ws=[w for w in ws if w]
        if ws: L.append(ws)
    return L
def pages_of(lines,per=20):
    return [lines[i:i+per] for i in range(0,len(lines),per)]
def P(pagelines,sim=ed1,maxd=5):
    hit=[0]*(maxd+1); tot=[0]*(maxd+1)
    for lines in pagelines:
        for i,line in enumerate(lines):
            for w in line:
                for d in range(1,maxd+1):
                    if i-d<0: break
                    tot[d]+=1
                    if any(sim(w,u) for u in lines[i-d]): hit[d]+=1
    return [hit[d]/tot[d] if tot[d] else float('nan') for d in range(1,maxd+1)]
def shuf(pagelines):
    out=[]
    for l in pagelines:
        x=list(l); random.shuffle(x); out.append(x)
    return out

voy=parse('ZL3b-n.txt')
nai=pages_of(lines_of('naibbe/encrypted/lat_output_ciphertext.txt'))
print(f"{'texto':28s} {'P1':>6s} {'P2':>6s} {'P3':>6s} {'P4':>6s} {'P5':>6s}   excesso P1 vs media(P2..P5)")
for name,data in [('Voynich',voy),('Voynich embaralhado',shuf(voy)),('Naibbe (latim cifrado)',nai),('Naibbe embaralhado',shuf(nai))]:
    p=P(data); e=p[0]-statistics.mean(p[1:])
    print(f"{name:28s} {' '.join(f'{x:.3f}' for x in p)}   {e:+.4f}")
# repeticao imediata dentro da linha
def imm(pagelines):
    n=s=0
    for lines in pagelines:
        for l in lines:
            for a,b in zip(l,l[1:]):
                n+=1
                if ed1(a,b): s+=1
    return s/n
print(f"\npalavras vizinhas quase iguais (mesma linha): Voynich {imm(voy)*100:.1f}%  Naibbe {imm(nai)*100:.1f}%")
