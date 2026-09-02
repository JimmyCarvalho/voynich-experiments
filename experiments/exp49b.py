import re, random, statistics, json
from exp49 import parse, ed1, shuffle_lines, shuffle_words_in_page, latin_like, xml_words
random.seed(11)

def per_page_stats(pagelines, sim, maxd=5):
    """returns per-page arrays for bootstrap + fair alignment baseline"""
    rows=[]  # per page: hits[d], tots[d], align_sum, alignrand_sum, n_align
    for lines in pagelines:
        hit=[0]*(maxd+1); tot=[0]*(maxd+1); al=alr=0.0; na=0
        for i,line in enumerate(lines):
            n=len(line)
            for k,w in enumerate(line):
                for d in range(1,maxd+1):
                    if i-d<0: break
                    up=lines[i-d]; tot[d]+=1
                    idx=[j for j,u in enumerate(up) if sim(w,u)]
                    if idx:
                        hit[d]+=1
                        if d==1 and n>1 and len(up)>1:
                            rp=k/(n-1); m=len(up)-1
                            al+=min(abs(rp-j/m) for j in idx)
                            rj=random.sample(range(len(up)),len(idx))
                            alr+=min(abs(rp-j/m) for j in rj)
                            na+=1
        rows.append((hit,tot,al,alr,na))
    return rows

def summarize(rows,maxd=5):
    H=[sum(r[0][d] for r in rows) for d in range(maxd+1)]
    T=[sum(r[1][d] for r in rows) for d in range(maxd+1)]
    P=[H[d]/T[d] for d in range(1,maxd+1)]
    al=sum(r[2] for r in rows)/sum(r[4] for r in rows); alr=sum(r[3] for r in rows)/sum(r[4] for r in rows)
    return P,al,alr

def excess(rows):
    P,_,_=summarize(rows); return P[0]-statistics.mean(P[1:])

def boot(rows,B=400):
    vals=[]
    for _ in range(B):
        s=[random.choice(rows) for _ in rows]; vals.append(excess(s))
    vals.sort(); return vals[int(0.025*B)],vals[int(0.975*B)]

voy=parse('ZL3b-n.txt')
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
por=xml_words('Portuguese.xml')
out={}
for name,data in [('voynich',voy),('voy_lines_shuffled',shuffle_lines(voy)),
                  ('latim',latin_like(voy,lat)),('portugues',latin_like(voy,por))]:
    for simname,sim in [('ed1',ed1),('exact',lambda a,b:a==b)]:
        rows=per_page_stats(data,sim); P,al,alr=summarize(rows); lo,hi=boot(rows)
        out[f'{name}|{simname}']=dict(P=P,excess=P[0]-statistics.mean(P[1:]),ci=[lo,hi],align=al,align_rand=alr)
        print(f"{name:20s} {simname:5s} P1={P[0]:.3f} mean(P2..P5)={statistics.mean(P[1:]):.3f} "
              f"excesso={P[0]-statistics.mean(P[1:]):+.4f} IC95=[{lo:+.4f},{hi:+.4f}] "
              f"alinh={al:.3f} vs base justa {alr:.3f} ({(alr-al)/alr*100:+.0f}%)")
json.dump(out,open('exp49b.json','w'),indent=1)
