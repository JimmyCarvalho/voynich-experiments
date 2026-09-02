# Exp 80: solucionador de cifra verbosa homofonica (classe Naibbe), sem a chave.
# simbolos = tipos de palavra cifrada (>= minc ocorrencias); cada simbolo -> 1 letra ou 1 bigrama do texto claro
# objetivo: log-prob de um modelo de 4-gramas de letras (sem espacos) da lingua alvo; busca por recozimento
import re, math, random, sys, time
from collections import Counter, defaultdict
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
MODE=sys.argv[1] if len(sys.argv)>1 else 'control'
ITERS=int(sys.argv[3]) if len(sys.argv)>3 else 300000
LANG=sys.argv[4] if len(sys.argv)>4 else 'latim'
ALPHA='abcdefghilmnopqrstuvxyz'
def clean(s): return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('k','c').replace('w','uu'))
# ---------- modelo de linguagem 4-gramas sem espacos, com backoff ----------
def build_lm(text):
    tabs=[defaultdict(Counter) for _ in range(4)]
    for i in range(len(text)):
        for k in range(4):
            if i>=k: tabs[k][text[i-k:i]][text[i]]+=1
    V=len(ALPHA)
    def logp(ctx,ch):
        for k in range(min(3,len(ctx)),-1,-1):
            c=tabs[k].get(ctx[len(ctx)-k:] if k else '')
            if c and sum(c.values())>=5: return math.log((c.get(ch,0)+0.2)/(sum(c.values())+0.2*V))
        return math.log(1/V)
    cache={}
    def lp(ctx,ch):
        key=(ctx,ch); v=cache.get(key)
        if v is None: v=logp(ctx,ch); cache[key]=v
        return v
    return lp
if LANG=='latim':
    vul=re.sub(r'[^a-z\s]','',open('vulgate.txt').read().lower()).split()
    lm_text=clean(''.join(vul[300000:700000]))   # longe do trecho cifrado (inicio do texto)
    bigr=Counter(lm_text[i:i+2] for i in range(len(lm_text)-1))
else:
    it=re.sub(r'[^a-z\s]','',open('naibbe/input/examples/divina_commedia.txt').read().lower()).split()
    lm_text=clean(''.join(it)); bigr=Counter(lm_text[i:i+2] for i in range(len(lm_text)-1))
LP=build_lm(lm_text)
OPTIONS=list(ALPHA)+[b for b,_ in bigr.most_common(220)]
uni_freq=Counter(lm_text); PRIOR=[uni_freq[o]/len(lm_text) if len(o)==1 else bigr[o]/len(lm_text) for o in OPTIONS]
# ---------- texto cifrado ----------
if MODE=='control':
    L1=[l.split() for l in open('naibbe/encrypted/lat_output_ciphertext.txt')]
    L2=[l.split() for l in open('naibbe/respaced_plaintext/lat_pre_encryption_respaced_plaintext.txt')]
    pairs=[(a,b) for a,b in zip(L1,L2) if a and b and len(a)==len(b)]
    lines=[a for a,b in pairs]; truth_lines=[b for a,b in pairs]
elif MODE=='voynich':
    from exp64 import voy_lines
    lines=voy_lines(); truth_lines=None
elif MODE=='chain':
    from exp66 import train, gen_line
    ctx=train(3); lines=[]
    while sum(len(l) for l in lines)<34119:
        ws=[w for w in gen_line(ctx,3).split() if w]
        if ws: lines.append(ws)
    truth_lines=None
lines=[l for l in lines if l]
cnt=Counter(w for l in lines for w in l)
MINC=3
syms=[w for w,c in cnt.items() if c>=MINC]
occ=defaultdict(list)
for li,l in enumerate(lines):
    for ti,w in enumerate(l):
        if cnt[w]>=MINC: occ[w].append((li,ti))
print(f"[{MODE}/{LANG}] linhas {len(lines)} tokens {sum(map(len,lines))} simbolos {len(syms)} cobrindo {sum(cnt[s] for s in syms)/sum(cnt.values())*100:.0f}%", flush=True)
# ---------- estado ----------
assign={s:random.choices(OPTIONS,PRIOR)[0] for s in syms}
def tok_str(w): return assign.get(w,'?')
def line_letters(l): return ''.join(tok_str(w) for w in l)
def line_score(letters):
    s=0.0
    for i,ch in enumerate(letters):
        if ch=='?': s+=math.log(1/len(ALPHA)); continue
        ctx=letters[max(0,i-3):i].replace('?','')
        s+=LP(ctx,ch)
    return s
def local_score(l, ti, s_old, s_new):
    """delta de trocar o token ti da linha l de s_old para s_new, rescorando so a janela afetada"""
    toks=[tok_str(w) for w in l]
    pre=''.join(toks[:ti]); post=''.join(toks[ti+1:])
    old=pre+s_old+post; new=pre+s_new+post
    a=len(pre); 
    def part(letters,start,end):
        s=0.0
        for i in range(start,min(end,len(letters))):
            ch=letters[i]
            if ch=='?': s+=math.log(1/len(ALPHA)); continue
            ctx=letters[max(0,i-3):i].replace('?','')
            s+=LP(ctx,ch)
        return s
    return part(new,a,a+len(s_new)+3)-part(old,a,a+len(s_old)+3)
LAMBDA=float(sys.argv[5]) if len(sys.argv)>5 else 2.0
P_LET={c:uni_freq[c]/len(lm_text) for c in ALPHA}
def letter_counts():
    c=Counter()
    for s in syms:
        for ch in assign[s]: c[ch]+=cnt[s]
    return c
def kl_pen(c):
    n=sum(c.values())
    return LAMBDA*n*sum((c[ch]/n)*math.log((c[ch]/n)/P_LET[ch]) for ch in ALPHA if c[ch]>0)
LC=letter_counts()
total=sum(line_score(line_letters(l)) for l in lines)-kl_pen(LC)
if truth_lines:
    majT=defaultdict(Counter)
    for a,b in zip(truth_lines,lines):
        for p,c in zip(a,b): majT[c][p]+=1
    saved=dict(assign)
    for s in syms: assign[s]=majT[s].most_common(1)[0][0]
    tl=sum(line_score(line_letters(l)) for l in lines); nl=sum(len(line_letters(l)) for l in lines)
    print(f"[control] score da CHAVE VERDADEIRA: {tl/nl:.3f} nats/letra (perplexidade {math.exp(-tl/nl):.1f})", flush=True)
    assign=saved
held=clean(''.join(vul[750000:800000])) if LANG=='latim' else lm_text[-30000:]
hs=sum(LP(held[max(0,i-3):i],held[i]) for i in range(len(held)))/len(held)
print(f"[{LANG}] LM em texto real nao visto: {hs:.3f} nats/letra (perplexidade {math.exp(-hs):.1f})", flush=True)
best=(total,dict(assign)); t0=time.time()
for it in range(ITERS):
    T=1.0*(1-it/ITERS)**2+0.05
    s=random.choice(syms); old=assign[s]
    new=random.choices(OPTIONS,PRIOR)[0] if random.random()<0.7 else random.choice(OPTIONS)
    if new==old: continue
    delta=0.0
    for li,ti in occ[s]: delta+=local_score(lines[li],ti,old,new)
    pen_old=kl_pen(LC)
    for ch in old: LC[ch]-=cnt[s]
    for ch in new: LC[ch]+=cnt[s]
    delta+=pen_old-kl_pen(LC)
    if delta>=0 or random.random()<math.exp(delta/T):
        assign[s]=new; total+=delta
        if total>best[0]: best=(total,dict(assign))
    else:
        for ch in new: LC[ch]-=cnt[s]
        for ch in old: LC[ch]+=cnt[s]
    if it%2000==0 and it>0:
        # troca global de duas letras (x<->y em todas as atribuicoes)
        x,y=random.sample(ALPHA,2); tr=str.maketrans(x+y,y+x)
        new_assign={s2:a.translate(tr) for s2,a in assign.items()}
        saved_assign=assign; assign=new_assign
        nt=sum(line_score(line_letters(l)) for l in lines)-kl_pen(letter_counts())
        if nt>=total or random.random()<math.exp((nt-total)/T): total=nt; LC=letter_counts()
        else: assign=saved_assign
        if total>best[0]: best=(total,dict(assign))
    if it%50000==0: print(f"  it {it} score/letra {total/sum(len(line_letters(l)) for l in lines):.3f}  ({time.time()-t0:.0f}s)", flush=True)
assign=best[1]
nlet=sum(len(line_letters(l)) for l in lines)
print(f"[{MODE}/{LANG}] melhor log-prob por letra: {best[0]/nlet:.3f} nats  (perplexidade {math.exp(-best[0]/nlet):.1f})")
# avaliacao
if truth_lines:
    maj=defaultdict(Counter)
    for a,b in zip(truth_lines,lines):
        if len(a)==len(b):
            for p,c in zip(a,b): maj[c][p]+=1
    hit=tot=0; lethit=letot=0
    for s in syms:
        tp=maj[s].most_common(1)[0][0]; n=cnt[s]; tot+=n
        if assign[s]==tp: hit+=n
        for x,y in zip(assign[s],tp): letot+=1; lethit+= x==y
    print(f"[{MODE}] acuracia por token (simbolos atribuidos): {hit/tot*100:.1f}%   por letra: {lethit/letot*100:.1f}%")
print("decodificacao das 3 primeiras linhas:")
for l in lines[:3]: print("   ", ' '.join(tok_str(w) for w in l))
import json; json.dump({'mode':MODE,'lang':LANG,'score_per_letter':best[0]/nlet,'assign':assign},open(f'exp80_{MODE}_{LANG}.json','w'))
