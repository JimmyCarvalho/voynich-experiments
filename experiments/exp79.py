# Exp 79: as etiquetas sao nomes latinos/italianos em substituicao simples? busca da chave que maximiza acertos no lexico, com controle
import re, math, random, sys
from collections import Counter, defaultdict
random.seed(7)
def lexicon(path,minc=2):
    ws=re.sub(r'[^a-z\s]','',open(path).read().lower()).split(); c=Counter(ws)
    return {w for w,n in c.items() if n>=minc and len(w)>=3}, ws
LAT,latws=lexicon('latin_words.txt',2); ITA,itws=lexicon('naibbe/input/examples/divina_commedia.txt',1)
# etiquetas
labels=[]
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.(\d+),([@+=&])(L[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t).replace(',','.')
    ws=[re.sub(r'[^a-z]','',w) for w in t.split('.') if re.sub(r'[^a-z]','',w)]
    if ws: labels.append(ws[0])
labels=sorted(set(w for w in labels if len(w)>=3))
UNITS=['ch','sh','cth','ckh','cph','cfh','ee','ii','iin','ain','aiin','qo']
def seg(w):
    out=[];i=0
    while i<len(w):
        for L in (4,3,2):
            if w[i:i+L] in UNITS: out.append(w[i:i+L]); i+=L; break
        else: out.append(w[i]); i+=1
    return out
def solve(words, lex, letters='abcdefghilmnopqrstuvxyz', iters=60000, restarts=3, composite=False):
    seqs=[seg(w) if composite else list(w) for w in words]
    syms=sorted(set(s for q in seqs for s in q))
    best_global=(0,None)
    for r in range(restarts):
        key={s:random.choice(letters) for s in syms}
        def score(key): return sum(1 for q in seqs if ''.join(key[s] for s in q) in lex)
        cur=score(key); best=(cur,dict(key))
        idx=defaultdict(list)
        for i,q in enumerate(seqs):
            for s in set(q): idx[s].append(i)
        hits=[''.join(key[s] for s in q) in lex for q in seqs]
        for it in range(iters):
            T=0.6*(1-it/iters)+0.02
            s=random.choice(syms); old=key[s]; new=random.choice(letters)
            if new==old: continue
            key[s]=new; delta=0; changed=[]
            for i in idx[s]:
                h=''.join(key[x] for x in seqs[i]) in lex
                if h!=hits[i]: delta+= 1 if h else -1; changed.append((i,h))
            if delta>=0 or random.random()<math.exp(delta/T):
                cur+=delta
                for i,h in changed: hits[i]=h
                if cur>best[0]: best=(cur,dict(key))
            else: key[s]=old
        if best[0]>best_global[0]: best_global=best
    return best_global
def show(name,words,lex,composite=False):
    sc,key=solve(words,lex,composite=composite)
    seqs=[seg(w) if composite else list(w) for w in words]
    ex=[(w,''.join(key[s] for s in q)) for w,q in zip(words,seqs) if ''.join(key[s] for s in q) in lex][:10]
    print(f"{name:52s} acertos {sc:4d} de {len(words)} ({sc/len(words)*100:4.1f}%)   ex.: {', '.join(f'{a}->{b}' for a,b in ex)}"); sys.stdout.flush()
    return sc
# controles: 1) palavras latinas reais cifradas por substituicao (o solver deveria recupera-las); 2) palavras da CADEIA (sem sentido, mesmo tamanho): nivel de acaso
lat_types=[w for w in Counter(latws).most_common() if len(w[0])>=3]
random.seed(3); ctrl=random.sample([w for w,_ in lat_types[:8000]],len(labels))
alpha='abcdefghijklmnopqrstuvwxyz'; perm=list(alpha); random.shuffle(perm); sub=dict(zip(alpha,perm))
ctrl_enc=[''.join(sub[c] for c in w) for w in ctrl]
from exp66 import train, gen_line
ctx=train(3); gen=[]
while len(gen)<3000: gen+=[w for w in gen_line(ctx,3).split() if w]
chance=sorted(set(w for w in gen if len(w)>=3))[:len(labels)]
print(f"etiquetas distintas testadas: {len(labels)}  | lexico latino {len(LAT)} palavras, italiano {len(ITA)}\n")
show('controle: latim real cifrado, lexico latino',ctrl_enc,LAT)
show('nivel do acaso: palavras da cadeia, lexico latino',chance,LAT)
show('etiquetas, glifo a glifo, lexico latino',labels,LAT)
show('etiquetas, glifos compostos (ch sh aiin...), latino',labels,LAT,composite=True)
show('etiquetas, glifo a glifo, lexico italiano',labels,ITA)
show('nivel do acaso: cadeia, lexico italiano',chance,ITA)
strip=[w[2:] for w in labels if w[:2] in ('ot','ok','op','of') and len(w)>=5]
show('etiquetas sem o marcador o+gallows, latino',strip,LAT)
show('nivel do acaso para o mesmo caso',[w[2:] for w in chance if len(w)>=5][:len(strip)],LAT)
