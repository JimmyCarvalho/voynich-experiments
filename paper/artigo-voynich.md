# Ataquei o manuscrito Voynich com 36 experimentos. Todos os esconderijos estavam vazios.

## Um livro de 600 anos que ninguém leu

Em 1912, o livreiro polonês Wilfrid Voynich comprou um lote de manuscritos antigos guardados na Villa Mondragone, perto de Roma. Um deles não fazia sentido.

São cerca de 240 páginas de pergaminho, escritas à mão em um alfabeto que não aparece em nenhum outro documento conhecido do planeta. Cerca de 38 mil palavras. Ao redor do texto, as ilustrações: plantas que nenhum botânico consegue identificar, diagramas astronômicos, dezenas de mulheres nuas em banheiras ligadas por tubulações verdes.

A datação por carbono-14 do pergaminho, feita na Universidade do Arizona em 2009, deu 1404 a 1438. O objeto é autêntico e é do começo do século XV. Hoje ele está na Biblioteca Beinecke, em Yale, catalogado como MS 408.

Em seiscentos anos, ninguém leu uma linha.

Quem tentou não era amador. William Friedman, o maior criptoanalista americano do século XX, o homem por trás da quebra dos códigos japoneses na Segunda Guerra, atacou o manuscrito em três períodos da vida: anos 1920, 1940 e 1960. Morreu sem decifrar uma palavra. Em 1959 ele escondeu sua conclusão dentro de um anagrama lacrado, aberto só depois da sua morte: *"O MS Voynich foi uma tentativa inicial de construir uma língua artificial ou universal do tipo a priori."*

Traduzindo: o maior especialista do mundo abandonou a ideia de que havia um texto cifrado ali.

Resolvi testar isso do zero, com computador, e com uma regra que quase ninguém aplica nesse assunto.

## A regra: nada vale sem controle

O campo do Voynich é um cemitério de decifrações anunciadas. Hebraico, latim abreviado, proto-romance, turco antigo, náuatle. Todas caem pelo mesmo motivo: funcionam em meia dúzia de palavras escolhidas a dedo e desmoronam no resto.

O erro é sempre o mesmo, e é de método. A pessoa aplica uma técnica ao Voynich, obtém algo que parece promissor, e publica. Nunca testa a técnica contra um caso onde a resposta é conhecida.

Então minha regra foi: todo ataque roda duas vezes. Primeiro contra um texto real que eu mesmo cifrei, onde sei a resposta. Se o ataque não recupera o texto conhecido, o ataque é fraco e o resultado no Voynich não significa nada. Só depois de passar no controle é que o mesmo ataque, com os mesmos parâmetros, vai para o manuscrito.

Baixei a transliteração completa do texto (o padrão ZL, mantido pelo pesquisador René Zandbergen), montei modelos estatísticos de sete idiomas a partir de corpora reais de centenas de milhares de palavras, e comecei.

## O que o texto é

Antes de atacar, medir.

As 38 mil palavras se dividem em cerca de 8.300 formas distintas. As mais comuns, na notação padrão que converte cada glifo em uma letra latina, são *daiin*, *ol*, *chedy*, *shedy*, *qokeedy*. A estrutura interna é rígida a ponto de ser suspeita: quase tudo começa com *ch-*, *qo-*, *sh-*, *ok-*, *ot-*, e termina em *-dy*, *-in*, *-ey*, *-ol*, *-ar*.

Montei uma "gramática de encaixes" com apenas 2.112 combinações possíveis de prefixo, núcleo e sufixo. Ela cobre 53% de todas as ocorrências do manuscrito. As palavras são montadas, não fluem.

E existem 301 casos de palavras idênticas repetidas em sequência. Trechos reais do fólio 75r: *qokedy qokedy qokedy qokain olshedy*. Isso praticamente não acontece em língua nenhuma.

A medida que resume tudo é a entropia condicional: quanto uma letra permite prever a seguinte. Português, latim, grego, alemão, turco, hebraico e árabe ficam entre 2,9 e 3,5 bits. O Voynich fica em 2,12.

**[GRÁFICO 1]**

Nem latim com as vogais removidas, imitando o hebraico e o árabe escritos sem vogais, chega perto. O texto é repetitivo demais para ser língua.

## O ataque

Construí um quebrador automático de cifras de substituição, o tipo de código que qualquer escriba do século XV conseguiria operar. Ele testa milhões de mapeamentos possíveis e converge para o que produz o texto mais parecido com o idioma alvo.

Validei a ferramenta primeiro. Peguei latim da Vulgata, cifrei com uma chave aleatória, e soltei o ataque. Ele quebrou sozinho e recuperou 100% do texto: *"...ni gratiam in oculis tuis accipe munusculum de manibus meis..."*. Repeti para os outros seis idiomas. Em cinco deles o controle recuperou entre 92% e 100% do texto original.

Aí apliquei o mesmo ataque ao Voynich.

**[GRÁFICO 2]**

Barras verdes: a cifra real sendo quebrada, distância zero. Barras laranjas: o Voynich sob ataque idêntico, parando muito longe de qualquer língua. A "melhor decifração possível" contra latim sai assim: *"saquiq inam am atanni quam quami qtumlq i nam quammi qami qnuam"*. Pseudo-latim vazio, o otimizador forçando trigramas frequentes sem nada por baixo.

Isso fecha a porta, com demonstração reproduzível, para cifra de substituição simples nesses sete idiomas.

## A miragem árabe

O árabe merece parágrafo próprio, porque ele quase me enganou, e explica por que decifrações via línguas semíticas continuam sendo anunciadas até hoje.

No placar, o árabe passa. Défice negativo, dentro da faixa de língua real. Se eu parasse ali, teria uma manchete.

Rodei os controles negativos. Embaralhei as letras do Voynich, destruindo qualquer estrutura, e ataquei de novo: o modelo árabe rejeitou (défice +0,47). Bom sinal, o teste discrimina. Então fui ao teste que importa: das palavras "decifradas", quantas existem de fato em árabe?

Vinte por cento. Uma decifração verdadeira daria entre 60% e 90%. Para efeito de comparação, strings aleatórias do mesmo tamanho acertam 2%.

O motivo é estrutural. O árabe constrói palavras por gabaritos, encaixando raízes de três consoantes em padrões fixos. Isso produz uma assinatura estatística parecida com os encaixes do Voynich, o suficiente para enganar um modelo de trigramas. Não é decifração. É colisão de forma.

## A hipótese da máscara física

A ideia mais elegante que me sugeriram durante o trabalho foi mecânica, não matemática: e se o escriba usasse uma placa recortada, apoiada sobre a página, e a mensagem fosse só o que aparece nas janelas? O resto seria enchimento deliberado.

Isso tem nome e é tecnologia da época: grade de Cardan, descrita por Girolamo Cardano no século XVI. Papel e tesoura. Perfeitamente viável em 1420.

E é testável. Se existe uma máscara física, existe uma geometria, e ela se repete página após página. Varri 55 geometrias periódicas: palavra sim palavra não em todos os períodos de 2 a 6, linhas alternadas, glifos alternados dentro da linha, glifos alternados dentro da palavra, só a primeira palavra de cada linha, janelas de duas palavras a cada quatro. Testei também a variante do "miolo", em que os prefixos e sufixos rígidos seriam a encheção e o núcleo variável seria a mensagem.

Cada extração foi atacada com o quebrador já validado, contra latim e português.

Nenhuma revela língua. E o miolo saiu pior que o texto completo. Os núcleos são fragmentos como *ch ch kok kdch l che o kosh k k l t e*. A informação que existe no texto mora justamente nos afixos rígidos, não no recheio.

O argumento mais forte, porém, é outro. Medi a distribuição de glifos posição por posição da linha, da primeira palavra até a oitava. Todas são estatisticamente indistinguíveis entre si. Para a máscara funcionar, um humano teria que escrever à mão, ao longo de milhares de linhas, dois tipos de texto (um com significado e outro de enchimento) sem deixar nenhuma costura estatística em nenhuma posição. E ainda assim as janelas extraídas não viram língua em geometria alguma. A hipótese exige duas perfeições simultâneas.

## O que sobrou em pé

Depois de eliminar substituição em sete línguas, cifra polialfabética (o índice de coincidência do Voynich é 0,084, maior que o do latim, e cifras polialfabéticas achatam esse número), escrita sem vogais, latim abreviado por escriba, esteganografia em seis canais diferentes, glifos nulos, anagramas, tabela silábica e cifra verbosa com segmentação livre, sobrou uma explicação que os dados sustentam bem.

O texto foi gerado por um procedimento, não escrito a partir de uma mensagem.

A hipótese, formalizada por Torsten Timm e Andreas Schinner em 2019, é de autocitação: o escriba produz texto novo copiando palavras já escritas na página e alterando um pedaço. Escrevi um gerador de brinquedo com essa regra, umas poucas dezenas de linhas de código. Ele reproduz a entropia condicional (2,20 contra 2,12 reais), a taxa de repetição e o comprimento médio das palavras. Não reproduz tudo, e sou honesto quanto a isso: a concentração de frequências escapou do meu modelo simples. Reproduzir as quinze estatísticas ao mesmo tempo exigiu dos autores originais um modelo bem mais afinado.

Três achados independentes apontam para o mesmo lugar.

Primeiro, não há sintaxe. Agrupei as palavras por terminação, criando classes gramaticais aproximadas, e medi se classes vizinhas se condicionam. No latim, o excesso de informação mútua é 0,106 bits. No Voynich, 0,028. Quase nada. A rede de palavras adjacentes também não se organiza por função, como faria uma língua, e sim por semelhança de forma: *aiiin, aiin, ain, air, al, am, ar*.

Segundo, o sistema deriva. A palavra *daiin* cai de 4,6% para 1,1% ao longo do livro enquanto o prefixo *qo-* triplica. E, o mais revelador: a paleógrafa Lisa Fagin Davis identificou em 2020 cinco mãos diferentes escrevendo o manuscrito. Cruzei essa marcação com minhas estatísticas. Cada escriba escreve uma versão própria do sistema. Mesmo entre mãos que escrevem a mesma "língua interna", a sobreposição de vocabulário é de apenas 9% a 21%. Não existe um idioma fora das pessoas. Existem cinco pessoas executando um método de fabricar palavras, cada uma com seus cacoetes.

Terceiro, e talvez o mais bonito: o texto tem estrutura estética.

**[GRÁFICO 3]**

Medi quantas palavras vizinhas terminam com os mesmos dois glifos. No latim, 4,2%. No Voynich, 16,9%, contra 10,3% esperados por acaso. Quatro vezes mais eco que uma língua real. Somado às letras ornamentais que abrem parágrafos de forma desproporcional e à linha funcionando como unidade de composição visual, o que emerge tem forma de ladainha, de mantra, de encantamento escrito.

Existe precedente histórico. Hildegard von Bingen, abadessa alemã do século XII, inventou a *Lingua Ignota*, uma língua mística pessoal. Pintores italianos do século XV enchiam quadros de pseudo-cúfico, arabescos que imitam escrita árabe sem dizer nada, porque a forma da escrita estrangeira era bela e prestigiosa. Manuscritos mágicos medievais traziam *charaktêres*, símbolos de aparência alfabética sem leitura possível.

O Voynich seria o caso extremo dessa família. Duzentas e quarenta páginas de pergaminho caríssimo.

## O teste que dá credibilidade ao resto

Uma objeção derruba boa parte das análises publicadas sobre o Voynich: "seu resultado é artefato da transliteração". Existe mais de uma teoria sobre o que conta como um glifo, e elas discordam.

Refiz as medidas centrais na transliteração v101, que usa 63 símbolos onde a primeira usa 35. Todas as anomalias sobreviveram: entropia condicional baixíssima, palavras vizinhas quase idênticas, riqueza vocabular idêntica.

O que medi é propriedade do manuscrito, não da lente de leitura.

## Conclusão

Não existe tradução a extrair, e não por falta de esforço. Todo esconderijo testável foi aberto e estava vazio. O que resta são construções matematicamente irreversíveis, como anagramas ordenados ou um dicionário arbitrário de oito mil entradas, que nenhum método, humano ou de máquina, pode desfazer sem a chave.

Sobra uma fronteira que meus instrumentos não alcançam. Se a máscara fosse marcada por algo invisível na transliteração, uma tinta ligeiramente diferente, uma espessura de traço, só análise física do pergaminho detectaria.

Fora isso, a resposta mais provável é a que Friedman deixou lacrada em 1959, e que os dados de hoje sustentam melhor do que ele poderia imaginar.

Se o Voynich é arte, é a arte mais bem-sucedida da história do seu gênero. Seiscentos anos fazendo o mundo inteiro procurar um significado que talvez seja a própria procura.

---

**Nota de método.** Transliteração ZL 3b de Zandbergen e Landini e transliteração v101 (GC), ambas públicas em voynich.nu. Corpora de controle: Vulgata latina e traduções bíblicas paralelas em seis idiomas. Toda a análise foi feita em Python, com Claude como copiloto, ao longo de uma sessão de trabalho. Onde meus resultados divergem da literatura, a literatura vence: Timm e Schinner (2019) para autocitação, Lisa Fagin Davis (2020) para os cinco escribas, Jorge Stolfi (Unicamp) para a estrutura interna das palavras. O manuscrito inteiro está digitalizado e livre no site da Beinecke, em Yale. Vale folhear.
