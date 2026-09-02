# Builds the Naibbe control used by exp55, exp57, exp59, exp63b, exp64, exp65, exp76, exp80*:
# enciphers the first 3000 lines of the Vulgate (Latin) with Michael Greshko's Naibbe cipher.
# Requires: naibbe/ (cloned by scripts/fetch_data.sh) and vulgate.txt beside this script.
import os, sys, re
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'vulgate.txt')).read()
os.makedirs(os.path.join(here,'naibbe','input','examples'),exist_ok=True)
open(os.path.join(here,'naibbe','input','examples','vulgate3k.txt'),'w').write('\n'.join(src[i:i+70] for i in range(0,220000,70)))
os.chdir(os.path.join(here,'naibbe')); sys.path.insert(0,'.')
import naibbe as N
os.makedirs('encrypted',exist_ok=True); os.makedirs('respaced_plaintext',exist_ok=True)
with open('input/examples/vulgate3k.txt') as fin, open('encrypted/lat_output_ciphertext.txt','w') as fout, \
     open('respaced_plaintext/lat_pre_encryption_respaced_plaintext.txt','w') as fplain:
    for line in fin:
        c=N.clean_line(line)
        if c:
            toks=N.encrypt_naibbe(c,N.naibbe_tables,N.placeholder_to_glyph,use_78=N.USE_78_CARD_DECK,pre_plaintext_file=fplain)
            fout.write(' '.join(toks)+'\n')
        else: fout.write('\n'); fplain.write('\n')
print('Naibbe control written to naibbe/encrypted/lat_output_ciphertext.txt')
