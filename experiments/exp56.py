# Exp 56: a fronteira entre palavras. MI atraves do espaco, classes fim->inicio, previsibilidade do espaco
import re, math, random, statistics, json
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET
from exp51 import voy_words, seg
random.seed(3)

def xw(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^\w\s]','',txt.lower()).split()
def nai_words():
    out=[]
    for l in open('naibbe/encrypted/lat_output_ciphertext.txt'):
        out.extend(re.sub(r'[^a-z]','',w) for w in l.split() if re.sub(r'[^a-z]','',w))
    return out

N=34000
voy=voy_words()
CUR={'ch','sh','cth','ckh','cph','cfh','ee','eee','iin','in','iiin','ii','iii'}
voy_cur=[seg(w,CUR) for w in voy]
corp={'Voynich (EVA)':[list(w) for w in voy],
      'Voynich (glifos compostos)':voy_cur,
      'latim':[list(w) for w in re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N]],
      'portugues':[list(w) for w in xw('Portuguese.xml')[:N]],
      'alemao':[list(w) for w in xw('German.xml')[:N]],
      'hebraico':[list(w) for w in xw('Hebrew.xml')[:N]],
      'turco':[list(w) for w in xw('Turkish.xml')[:N]],
      'Naibbe (latim cifrado)':[list(w) for w in nai_words()[:N]]}
sh=list(corp['Voynich (EVA)']); random.shuffle(sh); corp['Voynich, palavras embaralhadas']=sh

def MI(pairs):
    j=Counter(pairs); a=Counter(x for x,_ in pairs); b=Counter(y for _,y in pairs); n=len(pairs)
    return sum(c/n*math.log2((c/n)/((a[x]/n)*(b[y]/n))) for (x,y),c in j.items())
def cross_pairs(ws,dist=1):
    return [(ws[i][-1],ws[i+dist][0]) for i in range(len(ws)-dist)]
def classes(ws):
    pos=defaultdict(list)
    for w in ws:
        n=len(w)
        if n<2: continue
        for i,g in enumerate(w): pos[g].append(i/(n-1))
    mean={g:sum(v)/len(v) for g,v in pos.items() if len(v)>=50}
    end={g for g,m in mean.items() if m>=0.7}; start={g for g,m in mean.items() if m<=0.3}
    return end,start
def end_start_rate(ws):
    end,start=classes(ws); n=0; k=0
    for a,b in zip(ws,ws[1:]):
        n+=1
        if a[-1] in end and b[0] in start: k+=1
    return k/n, len(end), len(start)
def space_predictability(ws):
    """H(fronteira | contexto) / H(fronteira): quanto do espaco e dedutivel dos glifos"""
    # sequencia de glifos com marcador de fronteira apos cada posicao
    seqA=[]; 
    for w in ws:
        for i,g in enumerate(w): seqA.append((g, i==len(w)-1))
    half=len(seqA)//2
    def feats(seq,i):
        g=seq[i][0]; p=seq[i-1][0] if i>0 else '#'; nx=seq[i+1][0] if i+1<len(seq) else '#'; nx2=seq[i+2][0] if i+2<len(seq) else '#'
        return [(p,g,nx,nx2),(p,g,nx),(g,nx),(g,)]
    tabs=[defaultdict(Counter) for _ in range(4)]
    for i in range(half):
        for k,f in enumerate(feats(seqA,i)): tabs[k][f][seqA[i][1]]+=1
    lp=0.0; n=0; pb=Counter(b for _,b in seqA[half:])
    for i in range(half,len(seqA)):
        b=seqA[i][1]; p=None
        for k,f in enumerate(feats(seqA,i)):
            c=tabs[k].get(f)
            if c and sum(c.values())>=5:
                p=(c[b]+0.5)/(sum(c.values())+1.0); break
        if p is None: p=(pb[b]+0.5)/(sum(pb.values())+1.0)
        lp-=math.log2(p); n+=1
    Hc=lp/n; tot=sum(pb.values()); Hb=-sum(c/tot*math.log2(c/tot) for c in pb.values())
    return Hc,Hb,1-Hc/Hb

print(f"{'corpus':34s} {'MI d=1':>7s} {'MI d=2':>7s} {'fim->ini':>8s} {'#fim':>4s} {'#ini':>4s} {'H(esp|ctx)':>10s} {'H(esp)':>7s} {'previs.':>7s}")
res={}
for name,ws in corp.items():
    ws=[w for w in ws if w]
    mi1=MI(cross_pairs(ws,1)); mi2=MI(cross_pairs(ws,2)); r,ne,ns=end_start_rate(ws); Hc,Hb,pr=space_predictability(ws)
    res[name]=dict(mi1=mi1,mi2=mi2,end_start=r,Hc=Hc,Hb=Hb,pred=pr)
    print(f"{name:34s} {mi1:7.3f} {mi2:7.3f} {r*100:7.1f}% {ne:4d} {ns:4d} {Hc:10.3f} {Hb:7.3f} {pr*100:6.1f}%")
json.dump(res,open('exp56.json','w'),indent=1)

# quais pares fim->inicio carregam a MI no Voynich?
ws=corp['Voynich (EVA)']; pairs=cross_pairs(ws); j=Counter(pairs); a=Counter(x for x,_ in pairs); b=Counter(y for _,y in pairs); n=len(pairs)
print("\nVoynich: pares (ultimo glifo . primeiro glifo da seguinte) com maior desvio do esperado")
rows=[]
for (x,y),c in j.items():
    e=a[x]*b[y]/n
    if e>=30: rows.append((c/e,x,y,c,int(e)))
rows.sort(reverse=True)
print("  sobre-representados:", ', '.join(f"{x}.{y} ({c} obs / {e} esp, x{l:.1f})" for l,x,y,c,e in rows[:8]))
print("  sub-representados:  ", ', '.join(f"{x}.{y} ({c} / {e}, x{l:.2f})" for l,x,y,c,e in rows[-8:]))
