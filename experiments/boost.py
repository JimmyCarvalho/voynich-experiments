import re, math, random, pickle, json
from collections import Counter
random.seed(777)
models = pickle.load(open('models.pkl','rb'))
voy=[]
for raw in open('ZL3b-n.txt', encoding='utf-8', errors='replace'):
    m = re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)$', raw.strip())
    if not m: continue
    t = re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
    t = re.sub(r'\{[^}]*\}','',t).replace(',','.')
    voy.extend(re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w))
vtext=' '.join(voy)[:3500]
class Attack:
    def __init__(s,tri,bi):
        s.logp={t:math.log((c+0.1)/(bi.get(t[:2],0)+0.1*31)) for t,c in tri.items()}; s.floor=math.log(0.1/(0.1*31))
    def ws_(s,dec,wins):
        lp=s.logp; fl=s.floor
        return sum(lp.get(''.join(dec[w:w+3]),fl) for w in wins)
    def solve(s,cipher,targets,iters=40000,restarts=5):
        syms=sorted(set(cipher)-{' '}); n=len(cipher)
        pos={x:[i for i,c in enumerate(cipher) if c==x] for x in syms}
        wof={}
        for x in syms:
            st=set()
            for p in pos[x]:
                for w in (p-2,p-1,p):
                    if 0<=w<=n-3: st.add(w)
            wof[x]=sorted(st)
        best=None
        for r in range(restarts):
            mp={x:random.choice(targets) for x in syms}
            dec=[mp.get(c,' ') if c!=' ' else ' ' for c in cipher]
            for it in range(iters):
                T=0.10*(1-it/iters)*(n-2)*0.01
                if random.random()<0.5:
                    s1=random.choice(syms); old=mp[s1]; nt=random.choice(targets)
                    if nt==old: continue
                    wn=wof[s1]; b0=s.ws_(dec,wn)
                    for p in pos[s1]: dec[p]=nt
                    d=s.ws_(dec,wn)-b0
                    if d>=0 or random.random()<math.exp(d/max(T,1e-9)): mp[s1]=nt
                    else:
                        for p in pos[s1]: dec[p]=old
                else:
                    s1,s2=random.sample(syms,2)
                    wn=sorted(set(wof[s1])|set(wof[s2])); b0=s.ws_(dec,wn)
                    a,b=mp[s1],mp[s2]
                    for p in pos[s1]: dec[p]=b
                    for p in pos[s2]: dec[p]=a
                    d=s.ws_(dec,wn)-b0
                    if d>=0 or random.random()<math.exp(d/max(T,1e-9)): mp[s1],mp[s2]=b,a
                    else:
                        for p in pos[s1]: dec[p]=a
                        for p in pos[s2]: dec[p]=b
            sc=s.ws_(dec,range(n-2))
            if best is None or sc>best[0]: best=(sc,dict(mp))
        return best[0]/(n-2),best[1]
res={}
for key,label in [('turco','Turco'),('alemão','Alemão')]:
    tri,bi,letters,sample=models[key]
    atk=Attack(tri,bi)
    ref=atk.ws_(list(sample[:20000]),range(19998))/19998
    plain=sample[1000:4500]
    kk={c:t for c,t in zip(letters,random.sample(letters,len(letters)))}
    ciph=''.join(kk.get(c,c) if c!=' ' else ' ' for c in plain)
    cs,cm=atk.solve(ciph,letters)
    dec=''.join(cm.get(c,c) if c!=' ' else ' ' for c in ciph)
    rec=sum(1 for a,b in zip(dec,plain) if a==b)/len(plain)*100
    vs,_=atk.solve(vtext,letters)
    res[label]=dict(ref=round(ref,3),controle=round(ref-cs,3),voynich=round(ref-vs,3),recuperacao=round(rec))
    print(label,res[label])
json.dump(res,open('boost.json','w'),ensure_ascii=False)
