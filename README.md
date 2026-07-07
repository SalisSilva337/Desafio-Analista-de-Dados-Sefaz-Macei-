# **📊 Desafio de Estágio \- Análise de Dados (SEFAZ)**

O objetivo desse desafio foi extrair, limpar e analisar os dados abertos do Siconfi/Finbra sobre as Despesas por Função das capitais brasileiras (2020 a 2025), com um olhar especial para as finanças de **Maceió (AL)**.

## **🛠️ Ferramentas Utilizadas**

O projeto foi construído em Python, utilizando as seguintes bibliotecas:

* **Pandas:** Para a limpeza inicial, formatação de textos (separadores de milhares/decimais) e tratamento do encoding dos CSVs governamentais.  
* **DuckDB:** Utilizado como motor SQL para fazer os cruzamentos analíticos pesados de forma muito mais rápida, consultando direto do arquivo .parquet.  
* **Matplotlib & NumPy:** Para a geração do Dashboard visual com os gráficos da análise.  
* **Bibliotecas nativas (os, zipfile, pathlib, re):** Para automatizar a descompactação e organização dos arquivos.

## **💡 O que foi analisado?**

O script de análise principal (analise\_avancada\_duckdb.py) responde a 6 perguntas centrais:

1. **Eficiência na Saúde:** Um ranking que mostra o Gasto Per Capita das capitais e a **Taxa de Pagamento** (percentual do que foi empenhado que realmente foi pago).  
2. **Histórico de Maceió:** Como o gasto per capita de Maceió evoluiu de 2020 a 2024 em comparação à média nacional.  
3. **Detalhamento (Subfunções):** Dentro do orçamento da Saúde, para onde vai o dinheiro? (Ex: Atenção Básica vs. Hospitalar).  
4. **Gargalo de Caixa:** A diferença entre o serviço entregue (Liquidado) e o dinheiro pago em 2023, mostrando possíveis atrasos com fornecedores.  
5. **Restos a Pagar:** A evolução da dívida rolada para o ano seguinte na capital alagoana.  
6. **Prioridades Livres:** Tirando os gastos obrigatórios (Saúde, Educação, etc.), onde Maceió escolheu investir mais recursos em 2023?

*(Nota: Para lidar com o fato de que nem todas as capitais enviaram os dados de 2024/2025 ainda, foi utilizado médias Per Capita e Médias Nacionais nas comparações evolutivas, evitando distorções ou "falsas quedas" nos gastos).*

## **📁 Estrutura do Projeto**

📦 Projeto  
 ┣ 📂 dados\_compactos/          \# Arquivos .zip originais do Finbra (Anos 2020 a 2025\)  
 ┣ 📂 dados\_extraidos/          \# Destinos dos .csv organizados por ano  
 ┣ 📂 dados\_consolidados/       \# Base final otimizada (.parquet)  
 ┣ 📂 Scripts/  
 ┃ ┣ 📜 descompactar\_dados.py             \# Extrai e organiza os ZIPs  
 ┃ ┣ 📜 tratar\_dados\_e\_gerar\_parquet.py   \# Limpa, adiciona a coluna "Ano" e gera o Parquet  
 ┃ ┗ 📂 Analises/  
 ┃   ┣ 📜 analise\_padrao\_duckdb.py        \# Consultas de panorama geral  
 ┃   ┗ 📜 analise\_avancada\_duckdb.py      \# Script principal com os insights e geração do Dashboard  
 ┣ 📜 requirements.txt          \# Lista de dependências (Pandas, DuckDB, Matplotlib)  
 ┗ 📜 README.md                 \# Você está aqui

## **🚀 Como Executar**

Para testar o projeto na sua máquina:

1. Instale as dependências:  
   pip install \-r requirements.txt

2. Rode a preparação dos dados (Garante que os dados sejam descompactados e unificados corretamente):  
   python Scripts/descompactar\_dados.py  
   python Scripts/tratar\_dados\_e\_gerar\_parquet.py

3. Rode a análise principal para ver as tabelas no terminal e o Dashboard gráfico:  
   python Scripts/Analises/analise\_avancada\_duckdb.py  
