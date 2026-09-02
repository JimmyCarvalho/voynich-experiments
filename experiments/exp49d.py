import re, random, statistics
from exp49 import ed1, shuffle_lines
random.seed(3)
# parse with page metadata
pages={}; order=[]; meta={}
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    r=raw.strip()
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',r)
    if m:
        pg=m.group(1); t=m.group(5)
        t=re.sub(r'<[^>]*>','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t)
        t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
        ws=[re.sub(r'[^a-z]','',w) for w in t.split('.')]; ws=[w for w in ws if w]
        if not ws: continue
        if pg not in pages: pages[pg]=[]; order.append(pg)
        if m.group(3)=='&' and pages[pg]: pages[pg][-1].extend(ws)
        else: pages[pg].append(ws)
        continue
    mh=re.match(r'^<(f[^>]+)>\s*<!(.*)>', r)
    if mh: meta[mh.group(1)]=dict(re.findall(r'\$(\w)=(\w+)', mh.group(2)))
def P(pagelines,maxd=4):
    hit=[0]*(maxd+1); tot=[0]*(maxd+1)
    for lines in pagelines:
        for i,line in enumerate(lines):
            for w in line:
                for d in range(1,maxd+1):
                    if i-d<0: break
                    tot[d]+=1
                    if any(ed1(w,u) for u in lines[i-d]): hit[d]+=1
    return [hit[d]/tot[d] if tot[d] else float('nan') for d in range(1,maxd+1)], tot[1]
groups={}
for pg in order:
    key=(meta.get(pg,{}).get('I','?'), meta.get(pg,{}).get('L','?'))
    groups.setdefault(key,[]).append(pages[pg])
print('secao lang  n_pal  P1    P2    P3    P4   | embaralhado P1..P4      | excesso P1 (real - emb.)')
for key in sorted(groups, key=lambda k:-sum(len(l) for pg in groups[k] for l in pg)):
    data=groups[key]; p,n=P(data); q,_=P(shuffle_lines(data))
    if n<800: continue
    print(f"{key[0]:5s} {key[1]:4s} {n:6d}  {' '.join(f'{x:.3f}' for x in p)} | {' '.join(f'{x:.3f}' for x in q)} | {p[0]-q[0]:+.3f}  (d=2: {p[1]-q[1]:+.3f}, d=4: {p[3]-q[3]:+.3f})")
