import re, random
from exp49 import parse, latin_like
from exp56 import MI
random.seed(1)
voy=parse('ZL3b-n.txt')
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()
for name,data in [('latim no esqueleto de linhas do Voynich',latin_like(voy,lat))]:
    within=[]; across=[]
    for lines in data:
        for i,line in enumerate(lines):
            for a,b in zip(line,line[1:]): within.append((a[-1],b[0]))
            if i+1<len(lines) and line and lines[i+1]: across.append((line[-1][-1], lines[i+1][0][0]))
    sub=random.sample(within,len(across))
    print(f"{name}: dentro da linha MI={MI(within):.3f} (amostra n={len(across)}: {MI(sub):.3f}) | atraves da quebra MI={MI(across):.3f}")
