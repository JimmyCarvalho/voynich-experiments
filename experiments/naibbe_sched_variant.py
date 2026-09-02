# Variante da cifra Naibbe: a tabela do INICIO de cada palavra e escolhida pelo ULTIMO glifo da palavra anterior
# (regra de mao, sem dado). O resto (sufixo dos bigramas) continua sorteado pelo baralho.
import random, sys
MIX=float(sys.argv[1]) if len(sys.argv)>1 else 0.0
sys.argv=['x']
import naibbe as N
random.seed(5)
TABLES=N.TABLES
def make_schedule(seed=1):
    r=random.Random(seed)
    finals=list('abcdefghijklmnopqrstuvwxyz')
    return {g:r.choice(TABLES) for g in finals}
def encrypt_sched(plaintext, sched, mix=0.0):
    ngrams=N.respace_plaintext(plaintext)
    deck=N.create_card_deck(False); di=0; out=[]; prev_last='#'
    def draw():
        nonlocal deck,di
        if di>=len(deck): deck=N.create_card_deck(False); di=0
        t=deck[di]; di+=1; return t
    for tok in ngrams:
        first_table = sched.get(prev_last, 'alpha') if (prev_last!='#' and random.random()>=mix) else draw()
        if len(tok)==1:
            code=N.naibbe_tables[first_table][('unigram',tok)]
            g=N.placeholder_to_glyph.get(code,code)
        else:
            while True:
                cp=N.naibbe_tables[first_table][('prefix',tok[0])]; gp=N.placeholder_to_glyph.get(cp,cp)
                cs=N.naibbe_tables[draw()][('suffix',tok[1])]; gs=N.placeholder_to_glyph.get(cs,cs)
                g=gp+gs
                if g not in N.unigram_glyphs: break
                first_table=draw()
        out.append(g); prev_last=g[-1]
    return out
if __name__=='__main__':
    mix=MIX
    sched=make_schedule(1)
    with open('input/examples/vulgate3k.txt') as fin, open('encrypted/lat_sched.txt','w') as fout:
        for line in fin:
            c=N.clean_line(line)
            if c: fout.write(' '.join(encrypt_sched(c,sched,mix))+'\n')
    print('ok', sched)
