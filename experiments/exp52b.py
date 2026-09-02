import re
from exp51 import voy_words, H2
from exp52 import merge_pass
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:34119]
ls=[list(w) for w in lat]
print("latim, empurrando ate a mesma compressao do Voynich (3.3 unid/palavra):")
for step in range(1,36):
    r=merge_pass(ls)
    if r is None: break
    hl,pair,ls=r
    L=sum(map(len,ls))/len(ls); A=len(set(x for s in ls for x in s))
    if step%5==0 or L<3.4: print(f"  {step:2d} fusoes: alfabeto={A:3d} unid/pal={L:4.2f} H2={hl:.3f}")
    if L<3.35: break
