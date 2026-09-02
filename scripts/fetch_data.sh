#!/usr/bin/env bash
# Downloads the data the experiments need into experiments/ (nothing is redistributed in this repo).
set -euo pipefail
cd "$(dirname "$0")/../experiments"

echo "== transliterations (voynich.nu, Rene Zandbergen; used with attribution)"
curl -sSL -o ZL3b-n.txt https://www.voynich.nu/data/ZL3b-n.txt
curl -sSL -o GC2a-n.txt https://www.voynich.nu/data/GC2a-n.txt

echo "== comparison corpora (christos-c/bible-corpus, public-domain translations)"
BC=https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles
for f in Latin Portuguese German Hebrew Greek Turkish Arabic Finnish Hungarian Basque-NT Nahuatl-NT; do
  out="${f%-NT}.xml"; curl -sSL -o "$out" "$BC/$f.xml" || echo "   (could not fetch $f)"
done
# a plain-text Latin corpus (Vulgate) used by several scripts as latin_words.txt / vulgate.txt
python3 - <<'PY'
import re, xml.etree.ElementTree as ET
try:
    t=' '.join(e.text or '' for e in ET.parse('Latin.xml').iter('seg'))
    open('vulgate.txt','w').write(t)
    open('latin_words.txt','w').write(re.sub(r'[^a-z\s]','',t.lower()))
    import shutil; shutil.copy('Latin.xml','latin.xml')
    print('   vulgate.txt / latin_words.txt written')
except Exception as e: print('   Latin corpus not available:', e)
PY

echo "== Naibbe cipher (Michael A. Greshko, MIT with citation requirement)"
rm -rf naibbe && git clone --depth 1 -q https://github.com/greshko/naibbe-cipher naibbe

echo "== Naibbe control (enciphers 3000 lines of the Vulgate)"
python3 make_naibbe_control.py

echo "== scans (Internet Archive, public domain, 56 MB) -> img/vms.pdf"
mkdir -p img && curl -sSL -o img/vms.pdf "https://archive.org/download/TheVoynichManuscript/Voynich_Manuscript.pdf"
echo "done. Run the experiments from this directory, e.g.: python3 exp65.py"
