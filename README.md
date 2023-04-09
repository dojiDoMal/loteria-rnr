##  Gerador de apostas para loteria

### Jogo: LOTOMANIA

É gerado um conjunto de 50 número com base nos seguintes passos:

* A rede neural recorrente gera um conjunto de 20 números. Esse conjunto é a previsão da RN para o próximo sorteio com base nos sorteios anteriores.
* São gerados mais 20 números (um para cada bola) seguindo a distribuição normal<sup>[[1]](#ref_1)</sup> de cada uma.
* Para completar o conjunto de números são gerados mais 10 números usando uma distribuição uniforme

Esse último passo serve para gerar o conjunto completo com 50 números, além disso o uso da distribuição uniforme adiciona ruído.

<a name="ref_1"></a>
[1] Apesar de as bolas seguirem de fato uma distribuição normal, nesse caso foi utilizada uma distribuição [beta](https://en.wikipedia.org/wiki/Beta_distribution) pois na prática ela apresentou um comportamento mais parecido com o desejado.