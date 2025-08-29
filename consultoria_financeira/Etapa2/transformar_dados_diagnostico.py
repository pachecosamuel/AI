# transformador_dados.py

import re

def _converter_faixa_renda(faixa: str) -> int:
    """
    Converte faixa de renda para um valor médio estimado.
    """
    if not isinstance(faixa, str):
        return 0
    if "R$" in faixa:
        numeros = re.findall(r'\d[\d\.]*', faixa)
        if len(numeros) == 2:
            return (int(numeros[0].replace('.', '')) + int(numeros[1].replace('.', ''))) // 2
        elif len(numeros) == 1:
            return int(numeros[0].replace('.', ''))
    return 0

def transformar_resposta_bruta(resposta: dict) -> dict:
    """
    Recebe uma linha do formulário (dict) e transforma em uma estrutura padronizada.
    """
    def parse_float(valor):
        try:
            return float(str(valor).replace('.', '').replace(',', '.'))
        except:
            return 0.0

    dados = {
        "nome": resposta.get("nome_completo", ""),
        "email": resposta.get("seu_melhor_email", ""),
        "telefone": resposta.get("celular_com_ddd", ""),
        "idade": int(resposta.get("idade", 0)),
        "estado_civil": resposta.get("estado_civil", ""),
        "dependentes": int(resposta.get("quantas_pessoas_dependem_financeiramente_de_você?", 0)),
        "profissao": resposta.get("profissão", ""),
        "renda_individual": _converter_faixa_renda(resposta.get("renda_mensal_líquida_individual_(o_quanto_você_recebe_diretamente_na_sua_conta)", "")),
        "renda_familiar": _converter_faixa_renda(resposta.get("renda_mensal_líquida_familiar_(o_quanto_e_seu_conjugê_recebem_juntos)", "")),
        "tem_controle_gastos": resposta.get("você_faz_o_controle_das_suas_despesas?", "") == "Sim",
        "despesas_fixas": parse_float(resposta.get("qual_o_valor_médio_mensal_das_despesas_fixas_acima_descritas?", 0)),
        "despesas_variaveis": parse_float(resposta.get("qual_o_valor_médio_mensal_dos_seus_gastos_variáveis_mensais?_(aqueles_com_lazeres,_viagens,_comer_fora,_etc.)", 0)),
        "gasta_mais_que_ganha": resposta.get("você_costuma_gastar_mais_do_que_ganha?", "") == "Sim",
        "possui_dividas": resposta.get("você_possui_dívidas_atualmente?", "") == "Sim",
        "valor_dividas": parse_float(resposta.get("se_sim,_qual_o_valor_total_aproximado?", 0)),
        "reserva_emergencia": parse_float(resposta.get("se_sim,_qual_o_valor_atual_da_reserva?_(aproximado)", 0)),
        "meses_cobertura_reserva": int(resposta.get("quanto_meses_dos_seus_gastos,_sua_reserva_atual_cobriria?", 0)),
        "possui_investimentos": resposta.get("você_possui_algum_tipo_de_investimento?", "") == "Sim",
        "valor_investido": parse_float(resposta.get("valor_estimado_do_seu_patrimônio_investido", 0)),
        "bem_imovel_quitado": resposta.get("possui_algum_bem_imóvel_quitado?", "") == "Sim",
        "veiculo_proprio": resposta.get("possui_veículo_próprio?", "") == "Sim",
        "bens_nao_financeiros": parse_float(resposta.get("valor_estimado_dos_bens_não_financeiros_(carro,_imóvel,_etc.)", 0)),
        "guarda_dinheiro_mensalmente": resposta.get("tem_o_hábito_de_guardar_dinheiro_mensalmente?", "") == "Sim",
        "valor_guardado_mes": parse_float(resposta.get("se_sim,_qual_a_média_de_dinheiro_guardado_mensalmente?", 0)),
        "investe_mensalmente": resposta.get("tem_o_hábito_de_investir_mensalmente?", "") == "Sim",
        "valor_investido_mes": parse_float(resposta.get("se_sim,_qual_a_média_de_investimento_mensal?", 0)),
        "corretoras": resposta.get("se_sim,_em_qual_banco/corretora?", ""),
        "objetivo_mentoria": resposta.get("qual_seu_maior_objetivo_com_essa_consultoria?", ""),
        "objetivo_principal": resposta.get("qual_seu_objetivo_financeiro_mais_importante_hoje?", ""),
        "prazo_objetivo": resposta.get("para_esse_objetivo,_você_tem_algum_prazo_específico_para_realizar?", ""),
        "perfil_risco": resposta.get("em_relação_ao_risco_na_área_de_investimentos,_você_se_considera::", ""),
        "conhecimento_previo": resposta.get("já_ouviu_falar_dos_termos:_renda_fixa,_renda_variável,_liquidez,_diversificação,_inflação?", ""),
        "mercado_interesse": resposta.get("deseja_investir_no_brasil,_no_exterior_ou_ambos?", ""),
        "estilo_aprendizado": resposta.get("você_está_disposto(a)_a_estudar_ou_prefere_apenas_receber_recomendações_guiadas?", ""),
        "horario_reuniao": resposta.get("melhor_horário_para_reuniões_online", ""),
        "dia_reuniao": resposta.get("melhores_dias_para_reuniões_online", ""),
        "canal_contato": resposta.get("melhor_canal_para_contato_rápido", ""),
        "formato_atendimento": resposta.get("deseja_atendimento_individual_ou_com_o(a)_parceiro(a)?", ""),
    }

    return dados
