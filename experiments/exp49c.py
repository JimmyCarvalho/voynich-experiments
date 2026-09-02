import re, random, statistics, json
from exp49 import ed1, xml_words
random.seed(5)
def parse_par(path):
    """pages -> list of paragraphs -> list of lines (words)"""
    pages={}; order=[]; cur=None
    for raw in open(path,encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        pg=m.group(1); t=m.group(5)
        newpar='<%>' in t; endpar='<$>' in t
        t=re.sub(r'<[^>]*>','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
        t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.')]; ws=[w for w in ws if w]
        if not ws: continue
        if pg not in pages: pages[pg]=[]; order.append(pg); cur=None
        if m.group(3)=='&' and cur is not None and cur:
            cur[-1].extend(ws); continue
        if newpar or cur is None:
            cur=[]; pages[pg].append(cur)
        cur.append(ws)
        if endpar: cur=None
    return [pages[p] for p in order]

def P_within(pars, sim, maxd=4):
    hit=[0]*(maxd+1); tot=[0]*(maxd+1)
    for page in pars:
        for lines in page:
            for i,line in enumerate(lines):
                for w in line:
                    for d in range(1,maxd+1):
                        if i-d<0: break
                        tot[d]+=1
                        if any(sim(w,u) for u in lines[i-d]): hit[d]+=1
    return [hit[d]/tot[d] for d in range(1,maxd+1)], tot[1:]

def refill(pars, words):
    out=[]; p=0
    for page in pars:
        np_=[]
        for lines in page:
            nl=[]
            for l in lines: nl.append(words[p:p+len(l)]); p+=len(l)
            np_.append(nl)
        out.append(np_)
    return out
def shuffle_lines_in_par(pars):
    out=[]
    for page in pars:
        np_=[]
        for lines in page:
            l=list(lines); random.shuffle(l); np_.append(l)
        out.append(np_)
    return out

voy=parse_par('ZL3b-n.txt')
npar=sum(len(p) for p in voy); nl=sum(len(l) for p in voy for l in p)
print('paragrafos',npar,'linhas',nl,'linhas por paragrafo',nl/npar)
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
por=xml_words('Portuguese.xml')
for name,data in [('voynich',voy),('voy_linhas_embaralhadas_no_paragrafo',shuffle_lines_in_par(voy)),('latim',refill(voy,lat)),('portugues',refill(voy,por))]:
    for simname,sim in [('ed1',ed1),('exact',lambda a,b:a==b)]:
        P,T=P_within(data,sim)
        print(f"{name:38s} {simname:5s} P(d=1..4 mesmo paragrafo)={' '.join(f'{x:.3f}' for x in P)}  P1-P2={P[0]-P[1]:+.4f}  n={T}")
