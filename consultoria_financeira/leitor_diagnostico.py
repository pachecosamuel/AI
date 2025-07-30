# leitor_diagnostico.py

import pandas as pd
from transformar_dados_diagnostico import transformar_resposta_bruta

def carregar_dados(caminho_csv: str) -> list[dict]:
    """
    Lê o CSV exportado do Forms e retorna uma lista de dicionários,
    onde cada dicionário representa um mentorado.
    """
    # Leitura do CSV
    df = pd.read_csv(caminho_csv)

    # Padroniza os nomes das colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Converte para lista de dicionários (um por mentorado)
    dados_mentorados = df.to_dict(orient="records")

    return dados_mentorados

if __name__ == "__main__":
    caminho = "docs/diagnostico_financeiro_samuel.csv"
    
    mentorados = carregar_dados(caminho)
    mentor_padronizado = transformar_resposta_bruta(mentorados[0])

    print(f"{len(mentorados)} mentorado(s) carregado(s).\n")

    print("Exemplo:")
    for chave, valor in mentor_padronizado.items():
        print(f"{chave}: {valor}")
