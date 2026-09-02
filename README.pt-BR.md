# Oitenta experimentos no manuscrito Voynich

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22259446.svg)](https://doi.org/10.5281/zenodo.22259446)

**Site (PT):** https://jimmycarvalho.github.io/voynich-experiments/pt/ · **Site (EN):** https://jimmycarvalho.github.io/voynich-experiments/

Oitenta experimentos estatísticos no texto do manuscrito Voynich (Beinecke MS 408), cada um rodado primeiro em controles de língua natural (latim, português, alemão, hebraico, grego, turco, árabe, finlandês, húngaro, basco, náuatle) e em controles cifrados pelo método em teste, e só depois no manuscrito.

**Resultado em uma frase:** o texto é estatisticamente indistinguível de um processo com três regras, um hábito de dois glifos (cada glifo depende dos dois anteriores), 4% de cópia de uma palavra vizinha e um viés de preferências que muda de página para página; não há léxico acima desse hábito, nenhuma página tem vocabulário próprio, e as únicas palavras que se comportam como nomes são as etiquetas coladas aos desenhos. Uma cifra homofônica verbosa da classe Naibbe (Greshko, 2025) reproduz a entropia e a ausência de frases repetidas, mas não a cópia nem a ligação de fronteira; nossos solucionadores não quebraram o controle do próprio Greshko, então essa hipótese fica em aberto.

O argumento completo, as figuras e os números estão no site. Este repositório guarda o que é preciso para conferi-los.

## Estrutura

```
experiments/   um script por experimento (exp49.py ... exp80e.py) mais o código anterior de ataques e entropia
results/       os números que cada script produziu, em JSON
figures/       gráficos e scans anotados usados no site
docs/          o site bilíngue (o GitHub Pages serve esta pasta)
scripts/       fetch_data.sh baixa transliterações, corpora, o código Naibbe e os scans
paper/         o artigo longo anterior para o X (v1, 36 experimentos; superado pelo site)
data/          vazia até rodar scripts/fetch_data.sh (nada é redistribuído aqui)
```

## Reproduzir

```bash
git clone https://github.com/JimmyCarvalho/voynich-experiments
cd voynich-experiments
pip install -r requirements.txt
bash scripts/fetch_data.sh          # transliterações, corpora, código Naibbe, scans
cd experiments
python3 exp65.py                    # comprimento de memória do processo (~1 min)
python3 exp66.py                    # cadeia de glifos de ordem k contra a bateria
python3 exp71.py                    # nível da palavra vs hábito de 3 glifos, por corpus
```

Os scripts esperam rodar de dentro de `experiments/` com os arquivos de dados ao lado; o `fetch_data.sh` os coloca lá. A maioria termina em segundos ou poucos minutos. Os solucionadores em `exp80*.py` levam 5 a 15 minutos cada; rode em segundo plano.

Os experimentos 1 a 48 (ataques de substituição em sete línguas, polialfabética, abjad, abreviatura, grade de Cardano, glifos nulos, cifra verbosa, tabela silábica, anagrama, nomenclator, simulador de autocitação, escribas, etiquetas do zodíaco, comunidades de adjacência, deriva, línguas aglutinantes, controles de ladainha, lista ordenada, tabela numérica, taxonomia de Friedman, transposição, inversão, fusão de glifos, n-gramas repetidos, palavra como letra, espaços falsos, distribuição de tamanhos) foram rodados numa sessão anterior; seus números agregados estão em `results/numbers.json` e `results/boost.json`, e os gráficos em `figures/`. `experiments/EXPERIMENTS.md` mapeia cada número de experimento ao script e ao arquivo de resultado.

## Dados e créditos

- Transliterações: EVA de Zandbergen e Landini (`ZL3b-n.txt`) e v101 de Glen Claston (`GC2a-n.txt`), do [voynich.nu](http://voynich.nu/) de René Zandbergen. Usadas com atribuição; não redistribuídas aqui.
- Corpora de comparação: [christos-c/bible-corpus](https://github.com/christos-c/bible-corpus) (traduções em domínio público) e Projeto Gutenberg.
- Cifra Naibbe: Michael A. Greshko, *Cryptologia* 2025, [doi:10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408); código em [greshko/naibbe-cipher](https://github.com/greshko/naibbe-cipher), usado sob a licença dele, que exige citar o artigo.
- Scans: [Internet Archive](https://archive.org/details/TheVoynichManuscript), domínio público.
- Escribas e imageamento multiespectral: Lisa Fagin Davis (2020, 2024).

## Licença

Código: MIT (ver `LICENSE`). Texto e figuras em `docs/` e `figures/`: CC BY 4.0. Escrito por Jimmy com Claude (Anthropic) como copiloto.

## Citar

Se usar isto, cite assim: Carvalho, J. (2026). *Eighty experiments on the Voynich manuscript: code, results and bilingual site* (v1.0). Zenodo. https://doi.org/10.5281/zenodo.22259446 (esta versão: https://doi.org/10.5281/zenodo.22259447). Cite também as fontes acima, em particular Zandbergen pela transliteração e Greshko pela cifra Naibbe.
