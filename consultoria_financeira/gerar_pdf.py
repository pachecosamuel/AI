from leitor_diagnostico import carregar_dados
from transformar_dados_diagnostico import transformar_resposta_bruta
from construir_pdf import gerar_plano_pdf

dados_brutos = carregar_dados("docs/diagnostico_financeiro_samuel.csv")
mentor = transformar_resposta_bruta(dados_brutos[0])
gerar_plano_pdf(mentor, nome_arquivo="plano_samuel.pdf")
