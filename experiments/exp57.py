# Exp 57: hibrido = cifra Naibbe + fracao p de palavras "de enchimento" copiadas da vizinhanca (com 1 edicao)
import re, math, random, statistics, json, sys
from collections import Counter
from exp49 import ed1, parse
from exp51 import H2
from exp56 import MI, cross_pairs, space_predictability
random.seed(11)

def nai_lines():
    L=[]
    for l in open('naibbe/encrypted/lat_output_ciphertext.txt'):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]; ws=[w for w in ws if w]
        if ws: L.append(ws)
    return L
def pages_of(lines,per=20): return [lines[i:i+per] for i in range(0,len(lines),per)]

def hybrid(pages, p, exact=0.35, seed_first_line=False):
    glyphs=[g for pg in pages for l in pg for w in l for g in w]
    out=[]
    for pg in pages:
        new=[]
        for li,line in enumerate(pg):
            nl=[]
            for k,w in enumerate(line):
                use_filler = random.random()<p
                if seed_first_line and li==0: use_filler=False
                if use_filler:
                    src=None
                    r=random.random()
                    if r<0.5 and k>0: src=nl[k-1]
                    elif li>0:
                        up=new[li-1]; j=min(len(up)-1,max(0,k+random.choice([-1,0,0,1])))
                        src=up[j]
                    elif k>0: src=nl[k-1]
                    if src is None: nl.append(w); continue
                    if random.random()<exact: nl.append(src)
                    else:
                        s=list(src); op=random.random()
                        if op<0.5 and len(s)>0: s[random.randrange(len(s))]=random.choice(glyphs)
                        elif op<0.75: s.insert(random.randrange(len(s)+1),random.choice(glyphs))
                        elif len(s)>2: del s[random.randrange(len(s))]
                        nl.append(''.join(s))
                else: nl.append(w)
            new.append(nl)
        out.append(new)
    return out

def line_memory(pagelines,maxd=5):
    hit=[0]*(maxd+1); tot=[0]*(maxd+1)
    for lines in pagelines:
        for i,line in enumerate(lines):
            for w in line:
                for d in range(1,maxd+1):
                    if i-d<0: break
                    tot[d]+=1
                    if any(ed1(w,u) for u in lines[i-d]): hit[d]+=1
    P=[hit[d]/tot[d] for d in range(1,maxd+1)]
    return P[0]-statistics.mean(P[1:])
def adj_ed1(pagelines):
    n=s=0
    for lines in pagelines:
        for l in lines:
            for a,b in zip(l,l[1:]):
                n+=1; s+=ed1(a,b)
    return s/n
def repeats(ws,n): return sum(1 for k,c in Counter(tuple(ws[i:i+n]) for i in range(len(ws)-n+1)).items() if c>1)
def battery(pagelines, N=34119):
    ws=[w for pg in pagelines for l in pg for w in l][:N]
    # recorta paginas ate N palavras
    cut=[]; c=0
    for pg in pagelines:
        if c>=N: break
        cut.append(pg); c+=sum(len(l) for l in pg)
    return dict(H2=H2(ws), TTR=len(set(ws))/len(ws), top20=sum(x for _,x in Counter(ws).most_common(20))/len(ws),
                rep4=repeats(ws,4), rep5=repeats(ws,5), imm=sum(1 for a,b in zip(ws,ws[1:]) if a==b),
                adj=adj_ed1(cut), mem=line_memory(cut), mi=MI(cross_pairs([list(w) for w in ws])),
                pred=space_predictability([list(w) for w in ws])[2])

voy=parse('ZL3b-n.txt')
ref=battery(voy)
base=pages_of(nai_lines())
configs=[('Voynich (referencia)',None)]+[(f'Naibbe + enchimento p={p:.2f}',p) for p in [0.0,0.10,0.20,0.30,0.40]]+[('so procedimento (p=1, semente=1a linha)',1.0)]
print(f"{'configuracao':42s} {'H2':>5s} {'TTR':>5s} {'top20':>6s} {'rep4':>5s} {'rep5':>5s} {'w=w-1':>5s} {'viz1':>6s} {'memLinha':>8s} {'MI':>6s} {'previs':>6s}")
out={}
def show(name,b):
    print(f"{name:42s} {b['H2']:5.2f} {b['TTR']:5.3f} {b['top20']*100:5.1f}% {b['rep4']:5d} {b['rep5']:5d} {b['imm']:5d} {b['adj']*100:5.1f}% {b['mem']:+8.4f} {b['mi']:6.3f} {b['pred']*100:5.1f}%")
show('Voynich (referencia)',ref); out['voynich']=ref
for name,p in configs[1:]:
    data=hybrid(base,p,seed_first_line=(p==1.0)) if p>0 else base
    b=battery(data); out[name]=b; show(name,b); sys.stdout.flush()
json.dump(out,open('exp57.json','w'),indent=1)
