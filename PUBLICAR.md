# Como publicar (passo a passo)

## 1. Repositório no GitHub (5 minutos)

1. Em github.com, crie um repositório público chamado `voynich-experiments` (sem README, sem licença: já estão aqui).
2. No seu computador, dentro desta pasta:

```bash
git init
git add .
git commit -m "Eighty experiments on the Voynich manuscript: code, results, site"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/voynich-experiments.git
git push -u origin main
```

3. Troque `USER` pelo seu usuário do GitHub nos quatro lugares onde ele aparece como marcador: `README.md`, `README.pt-BR.md`, `docs/index.html` e `docs/pt/index.html` (procure por `USER`). Faça um novo commit e push.

## 2. GitHub Pages (2 minutos)

Settings → Pages → Build and deployment → Source: "Deploy from a branch" → Branch: `main`, pasta `/docs` → Save.
Em um ou dois minutos o site fica no ar em `https://SEU_USUARIO.github.io/voynich-experiments/` (inglês) e `.../voynich-experiments/pt/` (português). O arquivo `docs/.nojekyll` já está lá para o GitHub servir os arquivos como estão.

## 3. Um DOI para ser citável (10 minutos, opcional mas recomendado)

1. Em zenodo.org, entre com a conta do GitHub e, em "GitHub", ative o repositório `voynich-experiments`.
2. No GitHub, crie um release: Releases → Draft a new release → tag `v1.0` → título "v1.0: 80 experiments" → Publish.
3. O Zenodo gera um DOI automaticamente. Cole o DOI no README (seção "Cite") e no rodapé do site.

## 4. Divulgação, na ordem que recomendo

1. **X**: uma thread curta (o texto em `paper/thread-promo.md` serve de base, mas precisa ser atualizado para os 80 experimentos e para a retratação sobre a cifra Naibbe) apontando para o site. Não use a palavra "decifrado" em lugar nenhum. A frase que vende sem enganar: "80 testes com controle; o texto se comporta como hábito, não como língua; a única exceção são as etiquetas; a cifra de Greshko continua em aberto".
2. **voynich.ninja**: é o fórum onde estão as pessoas que vão realmente checar os números (Zandbergen, Timm, Greshko e Parisel passam por lá). Poste um resumo de dez linhas com o link do repositório e peça revisão. Espere crítica dura e responda com os scripts. É ali que o trabalho ganha ou perde credibilidade.
3. **Greshko**: mande uma mensagem direta ou abra uma issue no repositório dele avisando que você rodou a cifra dele na bateria e que os solucionadores não quebraram o controle. É cortesia e é interesse dele.
4. **Lisa Fagin Davis e Claire Bowern**: e-mail curto com o link e os dois resultados que dialogam com o trabalho delas (o Exp 58 confirma os saltos nas trocas de mão; o Exp 71 responde ao argumento MATTR). Sem pedir nada.

## 5. O que não fazer

- Não redistribua as transliterações nem o PDF dos scans dentro do repositório; o script `scripts/fetch_data.sh` baixa tudo da fonte. As transliterações são do voynich.nu e pedem atribuição.
- Não remova a menção à licença do código Naibbe: ela exige citar o artigo de Greshko em qualquer uso.
- Não apresente o modelo de três regras como "solução". A conclusão defensável é a que está no site: indistinguível estatisticamente de um processo de três regras, com a cifra Naibbe em aberto e as etiquetas como exceção.

## 6. Manutenção

Se alguém achar um erro num experimento, corrija o script, rode de novo, atualize o JSON em `results/` e o número no site, e registre a mudança no release seguinte. A credibilidade vem de os números serem regeneráveis, não de estarem certos na primeira vez.
