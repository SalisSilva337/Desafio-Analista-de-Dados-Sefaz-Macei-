# **📊 Desafio Analista de Dados Sefaz Maceió**

Este projeto é um pipeline completo de **Engenharia e Análise de Dados** desenvolvido para processar, limpar e analisar os dados abertos do Siconfi/Finbra (Tesouro Nacional) referentes às Despesas por Função das capitais brasileiras entre 2020 e 2025\.

O foco analítico central é a **Saúde Fiscal e Eficiência Pública**, com um aprofundamento específico no município de **Maceió (AL)**, avaliando não apenas o quanto se gasta, mas *como* se gasta (Empenhado vs. Pago).

## **🎯 Objetivos do Projeto**

1. **Engenharia de Dados (ETL):** Automatizar a extração de múltiplos arquivos .zip anuais, tratar inconsistências de formatação governamental (encodings, separadores de milhares/decimais) e consolidar milhões de registros em um formato colunar otimizado (.parquet).  
2. **Análise de Eficiência:** Ultrapassar a análise descritiva básica (Gasto Total) e focar em métricas de eficiência, como a **Taxa de Execução Financeira** (o que foi prometido/empenhado *versus* o que foi efetivamente pago).  
3. **Inteligência de Negócio (Auditoria Fiscal):** Identificar gargalos de caixa (atrasos com fornecedores), rastrear a evolução da "bomba fiscal" (Restos a Pagar) e desvendar as prioridades discricionárias das gestões municipais além das obrigações constitucionais (Saúde e Educação).

## **🛠️ Stack Tecnológico**

O projeto foi construído utilizando um ecossistema Python moderno e focado em alta performance para dados:

* [**Python 3.x**](https://www.python.org/)**:** Linguagem base.  
* [**Pandas**](https://pandas.pydata.org/)**:** Utilizado primariamente na etapa de Transformação (Tratamento de enconding latin1, separadores decimais e agregação inicial) e na maquiagem de dados para exibição (formatação em R$ Milhões/Bilhões).  
* [**DuckDB**](https://duckdb.org/)**:** O motor analítico principal (OLAP). Substitui o Pandas nas agregações complexas, permitindo consultas SQL ultrarrápidas diretamente sobre arquivos .parquet sem sobrecarregar a memória RAM.  
* [**PyArrow**](https://arrow.apache.org/docs/python/index.html)**:** Motor por trás da geração do formato Parquet, garantindo compressão e leitura eficiente.  
* [**Matplotlib**](https://matplotlib.org/) & [NumPy](https://numpy.org/): Responsáveis pela geração do Dashboard visual (Gráficos de barras, linhas e rosca).  
* **Bibliotecas Padrão (os, zipfile, pathlib, re):** Gerenciamento dinâmico de diretórios e extração segura de dados.

## **📁 Estrutura do Projeto**

O projeto adota uma arquitetura modular, separando claramente o pipeline de ETL das análises analíticas:

📦 Projeto  
 ┣ 📂 dados\_compactos/          \# Arquivos .zip originais do Finbra separados por pastas de anos (2020 a 2025\)  
 ┣ 📂 dados\_extraidos/          \# Destino automático dos .csv extraídos e renomeados (ex: finbra2020.csv)  
 ┣ 📂 dados\_consolidados/       \# Base final otimizada (dados\_consolidados.parquet)  
 ┣ 📂 Scripts/  
 ┃ ┣ 📜 descompactar\_dados.py           \# \[ETL \- Passo 1\] Extrai ZIPs organizados por ano para evitar sobrescrita.  
 ┃ ┣ 📜 tratar\_dados\_e\_gerar\_parquet.py \# \[ETL \- Passo 2 e 3\] Limpa os CSVs, insere o ano da pasta e compila a base Parquet.  
 ┃ ┗ 📂 Analises/  
 ┃   ┣ 📜 analise\_padrao\_duckdb.py      \# Script de consistência de dados e panorama geral (Ranking básico).  
 ┃   ┗ 📜 analise\_avancada\_duckdb.py    \# Script principal de BI (Business Intelligence) e geração do Dashboard Visual.  
 ┣ 📜 requirements.txt          \# Dependências do projeto.  
 ┗ 📜 README.md                 \# Documentação (Você está aqui).

## **🚀 Como Executar**

Para reproduzir este projeto em sua máquina local, siga os passos abaixo na ordem apresentada:

**1\. Clone o repositório e crie um ambiente virtual (Recomendado):**

python \-m venv .venv  
source .venv/Scripts/activate  \# No Windows  
\# ou source .venv/bin/activate \# No Linux/macOS

**2\. Instale as dependências:**

pip install \-r requirements.txt

**3\. Execute o Pipeline ETL:**

*(Certifique-se de que a pasta dados\_compactos possui as subpastas anuais com os arquivos .zip)*

python Scripts/descompactar\_dados.py  
python Scripts/tratar\_dados\_e\_gerar\_parquet.py

*Isso gerará o arquivo dados\_consolidados.parquet necessário para as consultas.*

**4\. Execute as Análises:**

Para visualizar os *insights* no terminal (com paginação interativa) e gerar o Dashboard gráfico:

python Scripts/Analises/analise\_avancada\_duckdb.py

## **🔍 Insights e Pontos Analisados**

O script analise\_avancada\_duckdb.py responde a perguntas complexas de gestão pública divididas em 6 blocos principais:

1. **Ranking Per Capita e Eficiência na Saúde:**  
   * *Métrica:* Não avalia apenas quem gasta mais em valor absoluto, mas normaliza o gasto pela população.  
   * *Diferencial:* Calcula a **Taxa de Pagamento** (Pago vs. Empenhado). Se uma capital tem baixa execução, o orçamento é "fictício" (empenha mas não paga).  
2. **Evolução Histórica (Maceió vs. Média Nacional):**  
   * *Métrica:* Acompanha a linha do tempo (2020-2024) do gasto per capita em Saúde de Maceió (AL) e compara o *gap* com a média das demais capitais, evidenciando o comportamento pós-pandemia.  
3. **Drill-Down de Subfunções (Onde o dinheiro está?):**  
   * *Métrica:* Descobre a concentração percentual dentro de uma função. (Ex: O percentual exato do orçamento da Saúde destinado à *Atenção Básica* vs. *Assistência Hospitalar*).  
4. **O Gargalo de Caixa (Calote de Curto Prazo):**  
   * *Métrica:* Subtrai as Despesas Pagas das Despesas Liquidadas (usando 2023 como exemplo). Identifica as prefeituras que receberam o serviço do fornecedor, mas não possuíam caixa para honrar o pagamento no mesmo exercício financeiro.  
5. **A "Bomba Fiscal" (Evolução de Restos a Pagar em AL):**  
   * *Métrica:* Rastreia a inscrição de dívidas roladas para exercícios futuros em Maceió, dividindo a evolução entre Restos a Pagar Processados e Não Processados.  
6. **Prioridades Discricionárias (A Verdadeira Agenda):**  
   * *Métrica:* Filtra as obrigações constitucionais e as despesas com juros/dívidas (Saúde, Educação, Previdência, Dívida, etc.) para revelar o "Top 3" de onde a gestão de Maceió escolhe investir seus recursos livres (ex: Urbanismo, Saneamento).

## **⚠️ Data Completeness (Tratamento de Dados Faltantes)**

Durante o desenvolvimento da pipeline, identificou-se que a base do Finbra pode conter inconsistências temporais (ex: nem todos os municípios haviam entregue os balanços mais recentes de 2024/2025).

Para evitar a "armadilha analítica" de considerar quedas globais artificiais no orçamento, a Engenharia de Dados foi adaptada para compilar todos os arquivos históricos de forma segura e **as análises temporais foram ancoradas na métrica de Média Per Capita**. Isso garante que a ausência pontual de um ente federativo não corrompa a visualização da tendência nacional real.

*Desenvolvido como demonstração de proficiência em Análise e Engenharia de Dados para gestão pública.*