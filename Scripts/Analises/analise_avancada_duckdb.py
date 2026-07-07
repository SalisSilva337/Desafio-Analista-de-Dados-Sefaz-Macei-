import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# FUNÇÕES DE FORMATAÇÃO VISUAL (Terminal)
# =========================================================
def formata_moeda(valor):
    if pd.isna(valor) or valor == 0:
        return "R$ 0,00"
    sinal = "-" if valor < 0 else ""
    valor_abs = abs(valor)
    if valor_abs >= 1e9:
        return f"{sinal}R$ {valor_abs/1e9:.2f} Bi".replace('.', ',')
    elif valor_abs >= 1e6:
        return f"{sinal}R$ {valor_abs/1e6:.2f} Mi".replace('.', ',')
    else:
        txt = f"{valor_abs:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        return f"{sinal}R$ {txt}"

# =========================================================
# FUNÇÃO DO DASHBOARD (Gráficos)
# =========================================================
def exibir_dashboard_graficos(df_ranking, df_evolucao, df_subfuncoes, df_gargalo, df_rap, df_prioridades):
    print("Gerando dashboard interativo...")
    
    # Cria uma figura grande com 6 espaços (3 linhas, 2 colunas)
    fig, axs = plt.subplots(3, 2, figsize=(18, 12))
    fig.suptitle('Dashboard Fiscal de Capitais (Foco: Maceió/AL)', fontsize=20, fontweight='bold', y=0.98)
    
    # Cores padronizadas
    cor_maceio = '#1f77b4' # Azul
    cor_media = '#ff7f0e'  # Laranja
    cor_alerta = '#d62728' # Vermelho

    # ---------------------------------------------------------
    # 1. Gráfico de Barras: Top 10 Ranking de Saúde Per Capita
    # ---------------------------------------------------------
    ax = axs[0, 0]
    df_top10 = df_ranking.head(10).sort_values(by='Gasto_Pago_Per_Capita', ascending=True)
    ax.barh(df_top10['UF'], df_top10['Gasto_Pago_Per_Capita'], color='teal')
    ax.set_title('Top 10 Capitais: Gasto em Saúde Per Capita (R$)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Valor Pago por Habitante')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # ---------------------------------------------------------
    # 2. Gráfico de Linha: Evolução Maceió vs Média (Saúde)
    # ---------------------------------------------------------
    ax = axs[0, 1]
    ax.plot(df_evolucao['Ano'], df_evolucao['Gasto_Maceió'], marker='o', linewidth=2.5, color=cor_maceio, label='Maceió (AL)')
    ax.plot(df_evolucao['Ano'], df_evolucao['Média_Demais_Capitais'], marker='x', linewidth=2.5, linestyle='--', color=cor_media, label='Média Outras Capitais')
    ax.set_title('Evolução do Gasto em Saúde Per Capita (2020-2024)', fontsize=12, fontweight='bold')
    ax.set_xticks(df_evolucao['Ano'].dropna().unique())
    ax.set_ylabel('Gasto Per Capita (R$)')
    ax.legend()
    ax.grid(linestyle='--', alpha=0.7)

    # ---------------------------------------------------------
    # 3. Gráfico de Rosca (Donut): Drill-Down Subfunções
    # ---------------------------------------------------------
    ax = axs[1, 0]
    
    # Limpar textos muito longos ou com códigos (ex: "10.301 - Atenção Básica" -> "Atenção Básica")
    labels_clean = [texto.split('-')[-1].strip() if '-' in texto else texto for texto in df_subfuncoes['Subfunção']]
    valores = df_subfuncoes['Percentual_Do_Gasto']
    
    # Criar pie chart apenas com os valores em % (sem labels ao redor para não poluir)
    wedges, texts, autotexts = ax.pie(
        valores, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.Paired.colors,
        pctdistance=0.75, # Joga a porcentagem para o meio do anel
        textprops=dict(color="black", fontweight='bold', fontsize=10) # Formata os números
    )
    
    # Transforma o Pie Chart em Donut Chart (Rosca)
    centro_circulo = plt.Circle((0, 0), 0.55, fc='white')
    ax.add_artist(centro_circulo)
    ax.set_title('Concentração do Gasto da Saúde (Subfunções)', fontsize=12, fontweight='bold')
    
    # Adicionar legenda organizada externamente à direita do gráfico
    ax.legend(wedges, labels_clean,
              title="Subfunções",
              loc="center left",
              bbox_to_anchor=(0.95, 0, 0.5, 1),
              fontsize=9)

    # ---------------------------------------------------------
    # 4. Gráfico de Barras Agrupadas: Gargalo de Caixa (Liquidado vs Pago)
    # ---------------------------------------------------------
    ax = axs[1, 1]
    df_g = df_gargalo.head(8) # Pega os 8 maiores para não poluir
    x = np.arange(len(df_g['UF']))
    width = 0.35
    ax.bar(x - width/2, df_g['Servico_Entregue'] / 1e6, width, label='Liquidado (Entregue)', color='#2ca02c')
    ax.bar(x + width/2, df_g['Efetivamente_Pago'] / 1e6, width, label='Pago (Caixa)', color=cor_maceio)
    ax.set_title('Gargalo de Caixa (Em Milhões R$) - 2023', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df_g['UF'])
    ax.set_ylabel('Milhões de Reais')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # ---------------------------------------------------------
    # 5. Gráfico de Barras Empilhadas: Bomba Fiscal (Restos a Pagar - AL)
    # ---------------------------------------------------------
    ax = axs[2, 0]
    ax.bar(df_rap['Ano'].astype(str), df_rap['RAP_Processado_R$'] / 1e6, label='Processados', color='skyblue')
    ax.bar(df_rap['Ano'].astype(str), df_rap['RAP_Nao_Processado_R$'] / 1e6, bottom=df_rap['RAP_Processado_R$'] / 1e6, label='Não Processados', color=cor_alerta)
    ax.set_title('Evolução de Restos a Pagar em Maceió (Milhões R$)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Dívida Rolada (Milhões R$)')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # ---------------------------------------------------------
    # 6. Gráfico de Barras Horizontais: Prioridades Livres (Maceió)
    # ---------------------------------------------------------
    ax = axs[2, 1]
    df_p = df_prioridades.sort_values(by='Gasto_Pago', ascending=True)
    
    # Limpa os nomes para o eixo Y não ficar ilegível (Tira o "15 - ", "04 - ")
    labels_p = [texto.split('-')[-1].strip() for texto in df_p['Area_de_Governo']]
    labels_p = [texto[:35] + '...' if len(texto) > 35 else texto for texto in labels_p]
    
    ax.barh(labels_p, df_p['Gasto_Pago'] / 1e6, color='mediumpurple')
    ax.set_title('Onde Maceió mais gasta além do Obrigatório? (2023)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Valor Gasto (Milhões R$)')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Ajusta o layout para não sobrepor textos e exibe
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# =========================================================
# FUNÇÃO PRINCIPAL DE ANÁLISE (Extração DuckDB)
# =========================================================
def executar_analise_avancada():
    con = duckdb.connect(database=':memory:')
    caminho_parquet = 'dados_consolidados/dados_consolidados.parquet'
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    
    # ---------------------------------------------------------
    # QUERY 1
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 1: RANKING DE GASTOS EM SAÚDE PER CAPITA & TAXA DE PAGAMENTO")
    print("="*95)
    query_ranking = f"""
        SELECT 
            UF,
            AVG("População") AS População_Estimada,
            SUM(CASE WHEN Coluna = 'Despesas Empenhadas' THEN Valor ELSE 0 END) AS Empenhado,
            SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) AS Pago,
            (SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) / AVG("População")) AS Gasto_Pago_Per_Capita,
            (SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN Coluna = 'Despesas Empenhadas' THEN Valor ELSE 0 END), 0)) * 100 AS Taxa_Execucao_Pago
        FROM read_parquet('{caminho_parquet}')
        WHERE Conta LIKE '%10 - Saúde%' OR Conta = '10 - Saúde'
        GROUP BY UF
        ORDER BY Gasto_Pago_Per_Capita DESC
    """
    df_ranking = con.execute(query_ranking).df()
    df_vis1 = df_ranking.copy()
    df_vis1['Empenhado'] = df_vis1['Empenhado'].apply(formata_moeda)
    df_vis1['Pago'] = df_vis1['Pago'].apply(formata_moeda)
    df_vis1['Gasto_Pago_Per_Capita'] = df_vis1['Gasto_Pago_Per_Capita'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.'))
    df_vis1['Taxa_Execucao_Pago'] = df_vis1['Taxa_Execucao_Pago'].apply(lambda x: f"{x:.1f}%".replace('.', ','))
    df_vis1['População_Estimada'] = df_vis1['População_Estimada'].apply(lambda x: f"{int(x):,}".replace(',', '.'))
    print(df_vis1.head(10).to_string(index=False)) 
    
    # ---------------------------------------------------------
    # QUERY 2
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 2: EVOLUÇÃO DO GASTO EM SAÚDE PER CAPITA (2020-2024) - MACEIÓ VS MÉDIA")
    print("="*95)
    query_evolucao = f"""
        WITH GastoAnualPorUF AS (
            SELECT
                Ano,
                UF,
                SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) / AVG("População") AS Gasto_Per_Capita
            FROM read_parquet('{caminho_parquet}')
            WHERE (Conta LIKE '%10 - Saúde%' OR Conta = '10 - Saúde')
              AND Ano BETWEEN 2020 AND 2024
            GROUP BY Ano, UF
        ),
        MediaOutrasCapitais AS (
            SELECT Ano, AVG(Gasto_Per_Capita) AS Media_Nacional_Per_Capita
            FROM GastoAnualPorUF
            WHERE UF != 'AL'
            GROUP BY Ano
        ),
        MaceioGasto AS (
            SELECT Ano, Gasto_Per_Capita AS Maceio_Per_Capita
            FROM GastoAnualPorUF
            WHERE UF = 'AL'
        )
        SELECT
            m.Ano,
            mac.Maceio_Per_Capita AS Gasto_Maceió,
            m.Media_Nacional_Per_Capita AS Média_Demais_Capitais,
            (mac.Maceio_Per_Capita - m.Media_Nacional_Per_Capita) AS Diferenca_Maceio
        FROM MediaOutrasCapitais m
        LEFT JOIN MaceioGasto mac ON m.Ano = mac.Ano
        ORDER BY m.Ano ASC
    """
    df_evolucao = con.execute(query_evolucao).df()
    df_vis2 = df_evolucao.copy()
    for col in ['Gasto_Maceió', 'Média_Demais_Capitais', 'Diferenca_Maceio']:
        df_vis2[col] = df_vis2[col].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.') if pd.notna(x) else "Sem Dados")
    print(df_vis2.to_string(index=False))
    
    # ---------------------------------------------------------
    # QUERY 3
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 3: DRILL-DOWN - QUAIS SUBFUNÇÕES CONCENTRAM O GASTO DA SAÚDE?")
    print("="*95)
    query_subfuncoes = f"""
        SELECT 
            Conta AS Subfunção,
            SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) AS Total_Efetivamente_Pago,
            (SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) / SUM(SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END)) OVER()) * 100 AS Percentual_Do_Gasto
        FROM read_parquet('{caminho_parquet}')
        WHERE Conta LIKE '10.%' AND Conta NOT LIKE '%10 - Saúde%' AND Conta NOT LIKE 'Despesas%'
        GROUP BY Conta
        ORDER BY Total_Efetivamente_Pago DESC LIMIT 5
    """
    df_subfuncoes = con.execute(query_subfuncoes).df()
    df_vis3 = df_subfuncoes.copy()
    df_vis3['Total_Efetivamente_Pago'] = df_vis3['Total_Efetivamente_Pago'].apply(formata_moeda)
    df_vis3['Percentual_Do_Gasto'] = df_vis3['Percentual_Do_Gasto'].apply(lambda x: f"{x:.2f}%".replace('.', ','))
    print(df_vis3.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 4
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 4: O GARGALO DE CAIXA (Liquidado vs Pago) - TODAS AS FUNÇÕES (2023)")
    print(" Contexto: O serviço foi entregue (Liquidado), mas a prefeitura não pagou no ano.")
    print("="*95)
    query_gargalo = f"""
        SELECT 
            UF,
            SUM(CASE WHEN Coluna = 'Despesas Liquidadas' THEN Valor ELSE 0 END) AS Servico_Entregue,
            SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) AS Efetivamente_Pago,
            SUM(CASE WHEN Coluna = 'Despesas Liquidadas' THEN Valor ELSE 0 END) - 
            SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) AS Atraso_Fornecedores
        FROM read_parquet('{caminho_parquet}')
        WHERE Ano = 2023 AND Conta NOT LIKE 'Despesas%'
        GROUP BY UF
        ORDER BY Atraso_Fornecedores DESC LIMIT 10
    """
    df_gargalo = con.execute(query_gargalo).df()
    df_vis4 = df_gargalo.copy()
    for col in ['Servico_Entregue', 'Efetivamente_Pago', 'Atraso_Fornecedores']:
        df_vis4[col] = df_vis4[col].apply(formata_moeda)
    print(df_vis4.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 5
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 5: A BOMBA FISCAL - EVOLUÇÃO DE RESTOS A PAGAR EM MACEIÓ (AL)")
    print(" Contexto: Dívidas roladas para o ano seguinte comprometem o orçamento futuro.")
    print("="*95)
    query_rap = f"""
        SELECT 
            Ano,
            SUM(CASE WHEN Coluna = 'Inscrição de Restos a Pagar Processados' THEN Valor ELSE 0 END) AS RAP_Processado_R$,
            SUM(CASE WHEN Coluna = 'Inscrição de Restos a Pagar Não Processados' THEN Valor ELSE 0 END) AS RAP_Nao_Processado_R$,
            SUM(CASE WHEN Coluna LIKE 'Inscrição de Restos a Pagar%' THEN Valor ELSE 0 END) AS Total_Dívida_Rolada_R$
        FROM read_parquet('{caminho_parquet}')
        WHERE UF = 'AL' AND Ano BETWEEN 2020 AND 2024 AND Conta NOT LIKE 'Despesas%'
        GROUP BY Ano
        ORDER BY Ano ASC
    """
    df_rap = con.execute(query_rap).df()
    df_vis5 = df_rap.copy()
    for col in ['RAP_Processado_R$', 'RAP_Nao_Processado_R$', 'Total_Dívida_Rolada_R$']:
        df_vis5[col] = df_vis5[col].apply(formata_moeda)
    print(df_vis5.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 6
    # ---------------------------------------------------------
    print("\n" + "="*95)
    print(" INSIGHT 6: PRIORIDADES LIVRES - ONDE MACEIÓ GASTA ALÉM DO OBRIGATÓRIO? (2023)")
    print(" Contexto: Excluindo Saúde, Educação e Previdência, qual a verdadeira prioridade?")
    print("="*95)
    query_prioridades = f"""
        SELECT 
            Conta AS Area_de_Governo,
            SUM(CASE WHEN Coluna = 'Despesas Pagas' THEN Valor ELSE 0 END) AS Gasto_Pago
        FROM read_parquet('{caminho_parquet}')
        WHERE UF = 'AL' AND Ano = 2023
          AND Conta NOT LIKE 'Despesas%'
          AND Conta NOT LIKE '10 -%' 
          AND Conta NOT LIKE '12 -%' 
          AND Conta NOT LIKE '09 -%' 
          AND Conta NOT LIKE '28 -%' 
          AND Conta NOT LIKE '01 -%' 
          AND Conta NOT LIKE '%.%'   
        GROUP BY Conta
        ORDER BY Gasto_Pago DESC LIMIT 5
    """
    df_prioridades = con.execute(query_prioridades).df()
    df_vis6 = df_prioridades.copy()
    df_vis6['Gasto_Pago'] = df_vis6['Gasto_Pago'].apply(formata_moeda)
    print(df_vis6.to_string(index=False))
    print("\n")

    # =========================================================
    # CHAMA A FUNÇÃO DE PLOTAGEM DOS GRÁFICOS
    # =========================================================
    exibir_dashboard_graficos(df_ranking, df_evolucao, df_subfuncoes, df_gargalo, df_rap, df_prioridades)

if __name__ == "__main__":
    executar_analise_avancada()