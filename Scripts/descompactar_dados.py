import zipfile
from pathlib import Path

pasta_origem = Path('dados_compactos')
pasta_destino = Path('dados_extraidos')

pasta_destino.mkdir(parents=True, exist_ok=True)

if pasta_origem.exists():
    for arquivo_zip in pasta_origem.rglob('*.zip'):
        # 1. Pega o nome da pasta pai onde o ZIP está (ex: "2020", "2021")
        ano_pasta = arquivo_zip.parent.name
        
        # 2. Cria a subpasta específica para o ano
        subpasta_ano = pasta_destino / ano_pasta
        subpasta_ano.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            # 3. Extrai temporariamente para a pasta do ano
            zip_ref.extractall(subpasta_ano)
            
            # 4. Renomeia os arquivos extraídos para incluir o ano no nome
            # O .glob('*') lista tudo que acabou de ser extraído dentro da pasta do ano
            for arquivo_extraido in subpasta_ano.glob('*'):
                # Garante que vamos mexer apenas em arquivos (ignorando pastas internas, se houver)
                if arquivo_extraido.is_file():
                    extensão = arquivo_extraido.suffix  # Pega o .csv
                    nome_puro = arquivo_extraido.stem   # Pega o finbra
                    
                    # Se o nome já não tiver o ano (evita renomear duas vezes se rodar de novo)
                    if ano_pasta not in nome_puro:
                        # Novo nome ex: finbra2020.csv
                        novo_nome = f"{nome_puro}{ano_pasta}{extensão}"
                        novo_caminho = subpasta_ano / novo_nome
                        
                        # Aplica a renomeação no sistema operacional
                        arquivo_extraido.rename(novo_caminho)
            
            print(f"Descompactado e renomeado com sucesso para o ano {ano_pasta}")
else:
    print("Aviso: A pasta 'dados_compactos' não foi encontrada.")