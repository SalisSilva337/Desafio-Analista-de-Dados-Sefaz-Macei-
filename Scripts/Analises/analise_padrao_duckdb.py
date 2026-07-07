import duckdb
import pandas as pd
import math

# =========================================================
# FUNÇÕES DE FORMATAÇÃO
# =========================================================
def formata_moeda(valor):
    if pd.isna(valor) or valor == 0:
        return "R$ 0,00"
    elif valor >= 1e9: # Bilhões
        return f"R$ {valor/1e9:.2f} Bi".replace('.', ',')
    elif valor >= 1e6: # Milhões
        return f"R$ {valor/1e6:.2f} Mi".replace('.', ',')
    else:
        # Milhares
        txt = f"{valor:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        return f"R$ {txt}"

# =========================================================
# FUNÇÃO DE PAGINAÇÃO INTERATIVA
# =========================================================
def paginar_dataframe(df, linhas_por_pagina=20):
    total_linhas = len(df)
    total_paginas = math.ceil(total_linhas / linhas_por_pagina)
    pagina_atual = 1
    
    while True:
        inicio = (pagina_atual - 1) * linhas_por_pagina
        fim = inicio + linhas_por_pagina
        
        print(f"\n{'='*80}")
        print(f" EXIBINDO PÁGINA {pagina_atual} DE {total_paginas} (Total de registros: {total_linhas})")
        print(f"{'='*80}\n")
        
        print(df.iloc[inicio:fim].to_string(index=False))
        
        print("\n" + "-"*80)
        print("COMANDOS: [Número da página] | [P]róxima | [A]nterior | [S]air")
        comando = input("Digite um comando: ").strip().lower()
        
        if comando == 's':
            print("\nEncerrando a análise. Até logo!")
            break
        elif comando == 'p':
            if pagina_atual < total_paginas:
                pagina_atual += 1
            else:
                print("\n⚠️ Você já está na última página!")
        elif comando == 'a':
            if pagina_atual > 1:
                pagina_atual -= 1
            else:
                print("\n⚠️ Você já está na primeira página!")
        elif comando.isdigit():
            num_pagina = int(comando)
            if 1 <= num_pagina <= total_paginas:
                pagina_atual = num_pagina
            else:
                print(f"\n⚠️ Página inválida! Digite um número entre 1 e {total_paginas}.")
        else:
            print("\n⚠️ Comando não reconhecido.")

# =========================================================
# FUNÇÃO PRINCIPAL DE ANÁLISE
# =========================================================
def analisar_dados():
    con = duckdb.connect(database=':memory:')
    caminho_parquet = 'dados_consolidados/dados_consolidados.parquet'
    
    # Ajusta o layout do terminal
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    print("Executando consultas no banco de dados...")
    
    # OBSERVE A MUDANÇA: Mudamos Populacao para "População" (com aspas duplas na query)
    query_gastos = f"""
        SELECT 
            UF,
            Conta AS Funcao_Subfuncao,
            SUM(Valor) AS Total_Gasto,
            AVG("População") AS Populacao_Media,
            SUM(Valor) / AVG("População") AS Gasto_Per_Capita
        FROM read_parquet('{caminho_parquet}')
        WHERE Coluna LIKE '%Liquidada%' 
          AND Conta NOT LIKE 'Despesas%' 
        GROUP BY UF, Conta
        ORDER BY UF ASC, Total_Gasto DESC
    """
    
    # Executa a query e salva no DataFrame
    df_gastos = con.execute(query_gastos).df()
    
    # --- MAQUIAGEM DOS DADOS ---
    df_gastos['Total_Gasto'] = df_gastos['Total_Gasto'].apply(formata_moeda)
    
    df_gastos['Gasto_Per_Capita'] = df_gastos['Gasto_Per_Capita'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    )
    
    df_gastos['Populacao_Media'] = df_gastos['Populacao_Media'].apply(
        lambda x: f"{int(x):,}".replace(',', '.') if pd.notna(x) else "0"
    )
    
    # Chama a função de paginação
    paginar_dataframe(df_gastos, linhas_por_pagina=20)

if __name__ == "__main__":
    analisar_dados()