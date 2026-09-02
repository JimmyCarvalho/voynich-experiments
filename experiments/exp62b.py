# Exp 62b: re-segmentar usando a hesitacao do proprio escriba como guia (juntas moles = pares com espaco incerto frequente)
import re, math, random
from collections import Counter
from exp56 import MI, cross_pairs, space_predictability
from exp51 import H2
random.seed(2)
lines=[]
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','',t)
    t=re.sub(r'[^a-z.,]','',t).strip('.,')
    if t: lines.append(t)
# razao incerto/certo por par
dot=Counter(); com=Counter()
for t in lines:
    for i,c in enumerate(t):
        if c in '.,' and 0<i<len(t)-1 and t[i-1].isalpha() and t[i+1].isalpha():
            (dot if c=='.' else com)[(t[i-1],t[i+1])]+=1
nd=sum(dot.values()); nc=sum(com.values())
ratio={p:(com[p]/nc)/((dot[p]+0.5)/nd) for p in set(dot)|set(com) if com[p]+dot[p]>=40}
soft=sorted(ratio,key=lambda p:-ratio[p])
def words_with(joined):
    ws=[]
    for t in lines:
        s=t.replace(',','.')
        # junta fronteiras nas juntas moles
        out=[]; parts=s.split('.')
        cur=parts[0]
        for nxt in parts[1:]:
            if cur and nxt and (cur[-1],nxt[0]) in joined: cur+=nxt
            else: out.append(cur); cur=nxt
        out.append(cur); ws.extend(w for w in out if w)
    return ws
def repeats(ws,n): return sum(1 for k,c in Counter(tuple(ws[i:i+n]) for i in range(len(ws)-n+1)).items() if c>1)
print(f"{'juntas moles fundidas':>22s} {'palavras':>8s} {'tam':>5s} {'MI fronteira':>12s} {'H2':>6s} {'TTR':>6s} {'rep4':>5s} {'previs.':>7s}   pares fundidos")
for k in [0,3,6,10,15]:
    J=set(soft[:k]); ws=words_with(J); L=[list(w) for w in ws]
    print(f"{k:22d} {len(ws):8d} {sum(map(len,ws))/len(ws):5.2f} {MI(cross_pairs(L)):12.3f} {H2(ws):6.3f} {len(set(ws))/len(ws):6.3f} {repeats(ws,4):5d} {space_predictability(L)[2]*100:6.1f}%   {' '.join(a+b for a,b in soft[:k])}")
# controle: fundir k pares ALEATORIOS (nao moles) com frequencia comparavel
random.seed(5)
allp=[p for p in ratio if p not in set(soft[:15])]
for k in [6,15]:
    J=set(random.sample(allp,k)); ws=words_with(J); L=[list(w) for w in ws]
    print(f"{'aleatorio '+str(k):>22s} {len(ws):8d} {sum(map(len,ws))/len(ws):5.2f} {MI(cross_pairs(L)):12.3f} {H2(ws):6.3f} {len(set(ws))/len(ws):6.3f} {repeats(ws,4):5d} {space_predictability(L)[2]*100:6.1f}%")
