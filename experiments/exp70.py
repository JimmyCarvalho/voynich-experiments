# Exp 70: o tamanho da receita. quantas regras geram o livro?
import re, math
from collections import Counter, defaultdict
from exp64 import voy_lines, to_lines, xw
def stream(lines): return [' '.join(ws) for ws in lines]
def table(S,k):
    ctx=defaultdict(Counter)
    for s in S:
        s='^'*k+s+'$'
        for i in range(k,len(s)): ctx[s[i-k:i]][s[i]]+=1
    return ctx
def rules_needed(ctx,cover=0.95,min_ctx=5):
    n_ctx=0; n_rules=0; mass_total=sum(sum(c.values()) for c in ctx.values()); covered=0
    for c,succ in ctx.items():
        tot=sum(succ.values())
        if tot<min_ctx: continue
        n_ctx+=1; acc=0
        for sym,cnt in succ.most_common():
            n_rules+=1; acc+=cnt
            if acc>=cover*tot: break
        covered+=acc
    return n_ctx,n_rules,covered/mass_total
N=34119
corp={'Voynich':stream(voy_lines()),
      'latim':stream(to_lines(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N])),
      'portugues':stream(to_lines(xw('Portuguese.xml')[:N])),'alemao':stream(to_lines(xw('German.xml')[:N]))}
print(f"{'corpus':12s} {'ordem':>5s} {'contextos usados':>16s} {'regras (95% de cada contexto)':>30s} {'massa coberta':>13s}")
for name,S in corp.items():
    for k in [1,2,3]:
        nc,nr,cov=rules_needed(table(S,k)); print(f"{name:12s} {k:5d} {nc:16d} {nr:30d} {cov*100:12.1f}%")
# inventario de "silabas": fusoes gulosas (BPE) e quantas unidades cobrem 95% do fluxo
def bpe_units(words,merges=60):
    seqs=[list(w) for w in words]
    for _ in range(merges):
        bi=Counter()
        for s in seqs:
            for a,b in zip(s,s[1:]): bi[(a,b)]+=1
        if not bi: break
        (a,b),_=bi.most_common(1)[0]
        new=[]
        for s in seqs:
            o=[];i=0
            while i<len(s):
                if i+1<len(s) and s[i]==a and s[i+1]==b: o.append(a+b); i+=2
                else: o.append(s[i]); i+=1
            new.append(o)
        seqs=new
    c=Counter(u for s in seqs for u in s); tot=sum(c.values()); acc=0; n=0
    for u,cnt in c.most_common():
        n+=1; acc+=cnt
        if acc>=0.95*tot: break
    return n, len(c), sum(len(s) for s in seqs)/len(seqs), [u for u,_ in c.most_common(30)]
from exp51 import voy_words
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N]
print()
for name,ws in [('Voynich',voy_words()),('latim',lat)]:
    n95,ntot,L,top=bpe_units(ws,60)
    print(f"{name}: apos 60 fusoes, {ntot} unidades no total; {n95} cobrem 95% do texto; {L:.2f} unidades por palavra")
    print("   as 30 mais comuns:",' '.join(top))
