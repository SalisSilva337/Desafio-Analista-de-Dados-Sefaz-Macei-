import pandas as pd
from pathlib import Path
import re  # Importação necessária para buscar o ano no caminho do arquivo

pasta_destino = Path('dados_extraidos')
# O rglob vai entrar em todas as subpastas de anos que criamos
arquivos_dados = list(pasta_destino.rglob('*.csv'))
lista_dfs = []

print("Iniciando a leitura e consolidação dos dados por ano...")
for arquivo in arquivos_dados:
    # CORREÇÃO CRUCIAL: Busca 4 números no caminho completo (str(arquivo)), capturando o ano da pasta!
    match_ano = re.search(r'\d{4}', str(arquivo))
    ano_arquivo = int(match_ano.group()) if match_ano else 0
    
    # 2. Lendo cada arquivo com os parâmetros tratados
    df_temp = pd.read_csv(
        arquivo, 
        sep=';',              # Separador de colunas: ponto e vírgula
        encoding='latin1',    # Encoding: ISO-8859-1 (Latin-1) para manter os acentos
        decimal=',',          # Separador decimal: vírgula (converte R$ corretos)
        skiprows=3,           # Pula as 3 primeiras linhas de metadados
        thousands='.'         # Separador de milhares: ponto (converte R$ corretos)
    )
    
    # 3. Adiciona a coluna "Ano" na tabela ANTES de enviar para a lista
    df_temp['Ano'] = ano_arquivo
    
    lista_dfs.append(df_temp)

# Verifica se a lista não está vazia antes de concatenar
if lista_dfs:
    # Concatena todos os DataFrames em um só
    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    print(f"\nTotal de registros consolidados: {len(df_consolidado)}")

    # Prepara o caminho do Parquet
    caminho_parquet = Path('dados_consolidados/dados_consolidados.parquet')
    caminho_parquet.parent.mkdir(parents=True, exist_ok=True)

    # Salva diretamente
    df_consolidado.to_parquet(caminho_parquet, index=False)
    print(f"Arquivo Parquet gerado com sucesso: {caminho_parquet}")

else:
    print("Aviso: Nenhum arquivo CSV foi encontrado ou processado.")