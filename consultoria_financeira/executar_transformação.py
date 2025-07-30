# executar_transformacao.py

from leitor_diagnostico import carregar_dados
from transformar_dados_diagnostico import transformar_resposta_bruta

def exibir_dados_mentorado(mentor: dict, indice: int = 0):
    """
    Mostra os dados transformados de um mentorado no terminal.
    """
    print(f"\nMentorado {indice + 1} transformado:\n" + "-" * 40)
    for chave, valor in mentor.items():
        print(f"{chave}: {valor}")
    print("-" * 40)

def main():
    caminho_csv = "docs/diagnostico_financeiro_samuel.csv"  # ou substitua por input() se quiser parametrizar

    print("🔄 Carregando dados brutos do Forms...")
    respostas_brutas = carregar_dados(caminho_csv)
    print(f"✅ {len(respostas_brutas)} resposta(s) carregada(s) do CSV.")

    for i, resposta in enumerate(respostas_brutas):
        mentorado_transformado = transformar_resposta_bruta(resposta)
        exibir_dados_mentorado(mentorado_transformado, i)

if __name__ == "__main__":
    main()
