![logo](https://github.com/Sanches2707/Fome-Zero/assets/140003889/767e60f1-53f3-467f-9382-dccb1ea9f059)


# 1 - Problema de negócio

A Cury Company é uma empresa de tecnologia que criou um aplicativo
que conecta restaurantes, entregadores e pessoas.
Através desse aplicativo, é possível realizar o pedido de uma refeição, em
qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por
um entregador também cadastrado no aplicativo da Cury Company.

O CEO da empresa foi contratado recentemente e precisa entender melhor o negócio para poder tomar as melhores decisões estratégicas e alavancar ainda mais o Fome Zero. Para isso, ele necessita de uma análise dos dados da empresa e da geração de dashboards, com base nessas análises, a fim de mapear a base de restaurantes cadastrados e entender o andamento do negócio através das seguintes informações:

A Cury Company possui um modelo de negócio chamado Marketplace,
que fazer o intermédio do negócio entre três clientes principais:
Restaurantes, entregadores e pessoas compradoras. Para acompanhar o
crescimento desses negócios, o CEO gostaria de ver as seguintes
métricas de crescimento:

## Visão Geral:

1. Quantos países únicos estão registrados?
2. Quantos restaurantes únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?
6. Mapa dos restaurantes com base nas notas.

## Visão por País:

1. Quantidade de Restaurantes registrados por país ?
2. Quantidade de cidades registrados por país ?
3. Média de avaliações feitas por País?
4. Avaliação média por país ?
5. Qual é a média de preço de um prato para duas pessoas por país ?

## Visão por Cidades:

1. Top 10 cidades com mais restaurantes na Base de dados ?
2. Top 7 cidades com Restaurantes com média de avaliação acima de 4 ?
3. (Top 8) Cidades com Restaurantes com média de avaliação abaixo de 2.5 ?
4. Quantos restaurantes têm avaliações abaixo de 2.5, em quais cidades eles estão ?
5. (Top 10) Cidades com mais Restaurantes, com tipo de culinária distinta ? 

## Visão por Restaurantes:

1. Top 10 Restaurantes ?
2. Top 10 melhores tipos de culinárias ?
3. Top 10 piores tipos de culinárias ?

# 2 - Premissas assumidas para a análise

1. Marketplace foi o modelo de negócio assumido.
2. Os 3 principais visões do negócio foram: Visão transação de pedidos,
visão restaurante e visão entregadores.

# 3 - Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1. Visão por Páis.
2. Visão por Cidades.
3. Visão por Restaurantes.

Dispomos na página inicial as informações gerais com opção de seleção de Filtro por país com as informações gerais do Marketplace, além de uma mapa interativo, em que é possível identificar a localização de cada restaurante com rank de cores e suas principais características (Valor prato para dois, Tipo de Culinária e Nota Média de avaliação)

# 4 - Top 3 Insights de dados

1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito.
3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado.

# 5- O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link:

# 6- Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 7 - Próximo passos

1. Reduzir o número de métricas.
2. Dispor de features com as informações dos clientes (Sexo, Idade).
3. Criar novos filtros.
4. Analisar o custo e/ou benefício de ampliar a diversidade gastronômica em restaurantes com baixa avaliações, considerando o preço dos pratos e as avaliações dos restaurantes.










