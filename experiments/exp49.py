import re, random, statistics, json
from collections import defaultdict
random.seed(7)

def parse(path):
    pages=defaultdict(list)   # page -> list of lines (list of words)
    order=[]
    for raw in open(path,encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        pg=m.group(1); t=m.group(5)
        t=re.sub(r'<[^>]*>','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
        t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.')]
        ws=[w for w in ws if w]
        if not ws: continue
        if m.group(3)=='&' and pages[pg]:   # continuation of previous locus line
            pages[pg][-1].extend(ws)
        else:
            if pg not in order: order.append(pg)
            pages[pg].append(ws)
    return [pages[p] for p in order]

def ed1(a,b):
    if a==b: return True
    la,lb=len(a),len(b)
    if abs(la-lb)>1: return False
    if la==lb:
        d=0
        for x,y in zip(a,b):
            if x!=y:
                d+=1
                if d>1: return False
        return True
    if la>lb: a,b,la,lb=b,a,lb,la
    i=j=0; skipped=False
    while i<la and j<lb:
        if a[i]==b[j]: i+=1; j+=1
        else:
            if skipped: return False
            skipped=True; j+=1
    return True

def stats(pagelines, sim, maxd=5):
    hit=[0]*(maxd+1); tot=[0]*(maxd+1)
    same_hit=same_tot=0
    align=[]; align_rand=[]
    for lines in pagelines:
        for i,line in enumerate(lines):
            n=len(line)
            for k,w in enumerate(line):
                # same line, earlier words
                if k>0:
                    same_tot+=1
                    if any(sim(w,u) for u in line[:k]): same_hit+=1
                for d in range(1,maxd+1):
                    if i-d<0: break
                    up=lines[i-d]
                    tot[d]+=1
                    idx=[j for j,u in enumerate(up) if sim(w,u)]
                    if idx:
                        hit[d]+=1
                        if d==1 and n>1 and len(up)>1:
                            rp=k/(n-1)
                            best=min(abs(rp-j/(len(up)-1)) for j in idx)
                            align.append(best)
                            j=random.randrange(len(up))
                            align_rand.append(abs(rp-j/(len(up)-1)))
    P=[hit[d]/tot[d] if tot[d] else float('nan') for d in range(maxd+1)]
    return dict(same=same_hit/same_tot, P=P[1:], ratio14=P[1]/P[4] if P[4] else float('nan'),
                align=statistics.mean(align) if align else float('nan'),
                align_rand=statistics.mean(align_rand) if align_rand else float('nan'),
                n_align=len(align))

def shuffle_lines(pagelines):
    out=[]
    for lines in pagelines:
        l=list(lines); random.shuffle(l); out.append(l)
    return out

def shuffle_words_in_page(pagelines):
    out=[]
    for lines in pagelines:
        ws=[w for l in lines for w in l]; random.shuffle(ws)
        new=[]; p=0
        for l in lines:
            new.append(ws[p:p+len(l)]); p+=len(l)
        out.append(new)
    return out

def latin_like(pagelines, words):
    """format a running Latin text into the same page/line skeleton"""
    out=[]; p=0
    for lines in pagelines:
        new=[]
        for l in lines:
            new.append(words[p:p+len(l)]); p+=len(l)
        out.append(new)
    return out

voy=parse('ZL3b-n.txt')
nw=sum(len(l) for pg in voy for l in pg)
print('pages',len(voy),'lines',sum(len(pg) for pg in voy),'words',nw)

lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
print('latin words',len(lat))
# second natural-language control: Portuguese bible xml
import xml.etree.ElementTree as ET
def xml_words(fn):
    txt=' '.join(e.text or '' for e in ET.parse(fn).iter('seg'))
    return re.sub(r'[^a-z\s]','',txt.lower()).split()
por=xml_words('Portuguese.xml'); print('pt words',len(por))

exact=lambda a,b:a==b
res={}
for name,data in [('voynich',voy),('voy_lines_shuffled',shuffle_lines(voy)),('voy_words_shuffled',shuffle_words_in_page(voy)),
                  ('latim',latin_like(voy,lat)),('latim_lines_shuffled',shuffle_lines(latin_like(voy,lat))),
                  ('portugues',latin_like(voy,por))]:
    for simname,sim in [('ed1',ed1),('exact',exact)]:
        r=stats(data,sim); res[(name,simname)]=r
        print(f"{name:22s} {simname:5s} sameline={r['same']:.3f} P(d=1..5)={' '.join(f'{x:.3f}' for x in r['P'])} "
              f"P1/P4={r['ratio14']:.2f} align={r['align']:.3f} vs rand {r['align_rand']:.3f} (n={r['n_align']})")
json.dump({f'{k[0]}|{k[1]}':v for k,v in res.items()},open('exp49.json','w'),indent=1)
