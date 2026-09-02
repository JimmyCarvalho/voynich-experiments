# Exp 63a: descobrir a unidade. Cortar o fluxo de glifos (sem espacos) nas juntas com P(espaco | a,b) >= theta
import re, math, random, statistics, json
from collections import Counter, defaultdict
from exp56 import MI
from exp51 import H2
random.seed(4)
lines=[]   # cada linha: lista de (glifo, tem_espaco_depois)
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','',t)
    t=re.sub(r'[^a-z.,]','',t).strip('.,')
    if not t: continue
    seq=[]
    for i,c in enumerate(t):
        if c.isalpha():
            nxt=t[i+1] if i+1<len(t) else ''
            seq.append((c, nxt in '.,'))
    lines.append(seq)
# P(espaco | a,b) por junta
tot=Counter(); sp=Counter()
for seq in lines:
    for (a,sa),(b,sb) in zip(seq,seq[1:]):
        tot[(a,b)]+=1
        if sa: sp[(a,b)]+=1
P={k:sp[k]/tot[k] for k in tot if tot[k]>=20}
def segment(theta):
    units=[]; cuts=0; hits=0; eva_sp=0
    for seq in lines:
        cur=''
        for i,(g,s) in enumerate(seq):
            cur+=g
            if i+1<len(seq):
                b=seq[i+1][0]; cut=P.get((g,b),0)>=theta
                if cut: units.append(cur); cur=''; cuts+=1
                if cut and s: hits+=1
                if s: eva_sp+=1
        if cur: units.append(cur)
    return units, cuts, hits, eva_sp
def repeats(ws,n): return sum(1 for k,c in Counter(tuple(ws[i:i+n]) for i in range(len(ws)-n+1)).items() if c>1)
print(f"{'theta':>6s} {'unidades':>8s} {'tam':>5s} {'MI entre unidades':>17s} {'H2':>6s} {'TTR':>6s} {'rep4':>5s} {'precisao':>8s} {'cobertura':>9s}")
rows=[]
for theta in [0.98,0.95,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]:
    U,cuts,hits,eva_sp=segment(theta)
    if len(U)<500: continue
    L=[list(u) for u in U]
    pairs=[(U[i][-1],U[i+1][0]) for i in range(len(U)-1)]
    mi=MI(pairs); sh=[y for _,y in pairs]; random.shuffle(sh); mi0=MI(list(zip([x for x,_ in pairs],sh)))
    rows.append(dict(theta=theta,n=len(U),len=sum(map(len,U))/len(U),mi=mi,mi0=mi0,H2=H2(U),ttr=len(set(U))/len(U),rep4=repeats(U,4),prec=hits/cuts if cuts else 0,rec=hits/eva_sp))
    print(f"{theta:6.2f} {len(U):8d} {sum(map(len,U))/len(U):5.2f} {mi:8.3f} (piso {mi0:.3f}) {H2(U):6.3f} {len(set(U))/len(U):6.3f} {repeats(U,4):5d} {hits/cuts*100:7.0f}% {hits/eva_sp*100:8.0f}%")
json.dump(rows,open('exp63a.json','w'),indent=1)
# as juntas mais "duras" (P alto) e as mais "moles" com frequencia
print("\njuntas com P(espaco) mais alto (n>=200):", ', '.join(f"{a}{b} {P[(a,b)]*100:.0f}%" for (a,b) in sorted([k for k in P if tot[k]>=200],key=lambda k:-P[k])[:12]))
print("juntas frequentes com P(espaco) intermediario (20-80%):", ', '.join(f"{a}{b} {P[(a,b)]*100:.0f}% (n={tot[(a,b)]})" for (a,b) in sorted([k for k in P if tot[k]>=150 and 0.2<=P[k]<=0.8],key=lambda k:-tot[k])[:14]))
