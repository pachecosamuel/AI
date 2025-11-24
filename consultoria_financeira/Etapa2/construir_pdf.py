# gerador_pdf.py

from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
from matplotlib.ticker import StrMethodFormatter

# Convertendo cor hex para RGB (f3fffa → 243, 255, 250)
BACKGROUND_COLOR = (243, 255, 250)

def as_bool(val):
    # aceita bool (True/False), strings ("sim", "não", "true", "false", "1", "0", etc.) e None
    if isinstance(val, bool):
        return val
    s = str(val if val is not None else "").strip().lower()
    return s in {"sim", "s", "yes", "y", "true", "1", "on"}


def as_float(val, default=0.1):
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace("R$", "").replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return default



class PlanoFinanceiroPDF(FPDF):
    def header(self):
        # Aplica cor de fundo em cada nova página
        self.set_fill_color(*BACKGROUND_COLOR)
        self.rect(0, 0, self.w, self.h, 'F')


    def add_capa(self):
        self.add_page()
        self.set_font("Helvetica", "B", 24)
        self.ln(60)
        self.cell(0, 20, "Consultoria Financeira", ln=True, align="C")
        self.set_font("Helvetica", "", 14)
        self.cell(0, 10, "Mudando sua relação com o dinheiro", ln=True, align="C")
        self.ln(100)
        self.set_font("Helvetica", "I", 12)
        self.cell(0, 10, "por Samuel Pacheco", ln=True, align="C")


    def add_dados_pessoais(self, dados):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, "Dados Pessoais", ln=True, align="C")
        self.ln(10) # Adicionei uma quebra de linha de 10 pontos

        def linha(titulo, valor):
            self.set_font("Helvetica", "B", 12)
            self.cell(40, 10, f"{titulo}:", ln=False)
            self.set_font("Helvetica", "", 12)
            self.cell(0, 10, str(valor), ln=True)

        linha("Nome", dados["nome"])
        linha("Idade", dados["idade"])
        linha("Profissão", dados["profissao"])
        linha("E-mail", dados["email"])
        linha("WhatsApp", dados["telefone"])
        self.ln(10)

    def add_painel_financeiro(self, dados):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, "Resumo Financeiro", ln=True, align="C")
        self.ln(5)

        # Cálculos
        renda = dados['renda_individual']
        fixos = dados['despesas_fixas']
        variaveis = dados['despesas_variaveis']
        investido_mes = dados.get('valor_investido_mes', 0)
        investimento_total = dados.get('valor_investido', 0)
        reserva = dados.get('reserva_emergencia', 0)
        sobra = renda - (fixos + variaveis)
        percentual_investimento = (investido_mes / renda) * 100 if renda else 0
        meses_reserva = dados.get("meses_cobertura_reserva", 0)

        # Perfil financeiro (frases automáticas)
        frases = []
        if sobra > 0:
            frases.append("[OK] Você tem superávit mensal. Excelente!")
        else:
            frases.append("[ALERTA] Seus gastos totais superam sua renda.")

        if meses_reserva >= 6:
            frases.append("[OK] Sua reserva de emergência está saudável.")
        elif 1 <= meses_reserva < 6:
            frases.append("[ATENÇÃO] Sua reserva é moderada. Busque ampliar.")
        else:
            frases.append("[CRÍTICO] É fundamental construir uma reserva de emergência.")

        if percentual_investimento >= 15:
            frases.append("[OK] Ótimo hábito de investir mensalmente.")
        elif 5 <= percentual_investimento < 15:
            frases.append("[ATENÇÃO] Seu percentual de investimento pode crescer.")
        else:
            frases.append("[CRÍTICO] Comece a investir de forma consistente.")

        self.set_font("Helvetica", "", 12)
        for f in frases:
            self.multi_cell(0, 8, f)
            self.ln(2)
        self.ln(5)

        # Valores básicos apresentados
        self.cell(0, 10, f"Renda mensal: R$ {renda:.2f}", ln=True)
        self.cell(0, 10, f"Gastos fixos: R$ {fixos:.2f}", ln=True)
        self.cell(0, 10, f"Gastos variáveis: R$ {variaveis:.2f}", ln=True)
        self.cell(0, 10, f"Investimento mensal: R$ {investido_mes:.2f}", ln=True)
        self.cell(0, 10, f"Reserva de emergência: R$ {reserva:.2f}", ln=True)
        self.cell(0, 10, f"Investimentos totais acumulados: R$ {investimento_total:.2f}", ln=True)
        self.ln(5)

        # ---------- GRÁFICO 1: GASTOS MENSAL ----------
        categorias_gasto = ["Gastos Fixos", "Gastos Variáveis"]
        valores_gasto = [fixos, variaveis]

        plt.figure(figsize=(5, 3))
        barras = plt.bar(categorias_gasto, valores_gasto, color=["#5DADE2", "#F5B041"])
        plt.title("Distribuição de Gastos Mensais")
        plt.ylabel("Valor (R$)")
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('R$ {x:,.0f}'))

        for bar in barras:
            yval = bar.get_height()
            if yval > 300:  # Limite para mostrar dentro da barra
                plt.text(bar.get_x() + bar.get_width()/2, yval * 0.5, f"R$ {yval:,.0f}", ha='center', va='center', fontsize=10, color='white')
            else:
                plt.text(bar.get_x() + bar.get_width()/2, yval + 50, f"R$ {yval:,.0f}", ha='center', va='bottom', fontsize=10, color='black')


        plt.tight_layout()
        img1 = "grafico_gastos_mensais.png"
        plt.savefig(img1)
        plt.close()
        self.image(img1, x=30, w=150)
        os.remove(img1)

        self.ln(5)

        # ---------- GRÁFICO 2: PATRIMÔNIO / RESERVA ----------
        categorias_acumulacao = ["Aporte mensal", "Reserva", "Investimentos Totais"]
        valores_acumulacao = [investido_mes, reserva, investimento_total]

        plt.figure(figsize=(5, 3))
        barras2 = plt.bar(categorias_acumulacao, valores_acumulacao, color=["#58D68D", "#82E0AA", "#239B56"])
        plt.title("Distribuição Patrimonial")
        plt.ylabel("Valor (R$)")
        plt.grid(True, axis='y', linestyle='-', alpha=0.7)
        plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('R$ {x:,.0f}'))

        for bar in barras2:
            yval = bar.get_height()
            offset = yval * 0.05
            if yval > 10000:
                plt.text(bar.get_x() + bar.get_width()/2, yval - offset*3, f"R$ {yval:,.0f}", 
                        ha='center', va='bottom', fontsize=10, color='white')
            else:
                plt.text(bar.get_x() + bar.get_width()/2, yval + offset, f"R$ {yval:,.0f}", 
                        ha='center', va='bottom', fontsize=10, color='black')



        plt.tight_layout()
        img2 = "grafico_acumulacao.png"
        plt.savefig(img2)
        plt.close()
        self.image(img2, x=30, w=150)
        os.remove(img2)

        self.ln(10)


        # Distribuição sugerida (adaptativa, não fixa)
        
        # ---------- DISTRIBUIÇÃO 50-30-20 (ADAPTATIVA) ----------
            # Regras:
            # - Saudável (reserva >= 6 meses e sem dívidas): 50 / 30 / 20
            # - Moderado (1 a 5 meses de reserva, sem dívidas): 55 / 25 / 20
            # - Crítico (sem reserva ou com dívidas / déficit): 60 / 25 / 15
            # Obs.: mantemos tudo dentro das faixas 50–60 / 20–30 / 10–20

        self.ln(5)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Distribuição sugerida com base no seu perfil:", ln=True)
        self.set_font("Helvetica", "", 12)

        
        
        perfil = (dados.get("perfil_risco") or "").strip().lower()
        
        # depois:
        raw_dividas = dados.get("você_possui_dívidas_atualmente")
        if raw_dividas is None:
            raw_dividas = dados.get("possui_dividas")
        possui_dividas = as_bool(raw_dividas)


        
        if renda and renda > 0:
            if meses_reserva >= 6 and not possui_dividas:
                base = (0.50, 0.30, 0.20)
            elif 1 <= meses_reserva < 6 and not possui_dividas:
                base = (0.55, 0.25, 0.20)
            else:
                base = (0.60, 0.25, 0.15)

            # Ajuste suave pelo perfil (apenas quando a reserva está ok)
            if meses_reserva >= 6:
                if "arrojado" in perfil:
                    base = (0.50, 0.30, 0.20)  # mantém 50-30-20
                elif "conserv" in perfil:
                    base = (0.60, 0.25, 0.15)
                elif "moderado" in perfil:
                    base = (0.55, 0.25, 0.20)

            ess_pct, qual_pct, pou_pct = base
        else:
            ess_pct, qual_pct, pou_pct = 0.0, 0.0, 0.0

        
        # Calcula valores-alvo a partir da renda (somatório exato)
        essencial = round(renda * ess_pct, 2)
        qualidade = round(renda * qual_pct, 2)
        # Usa o restante para evitar erro de arredondamento
        poupanca = round(renda - essencial - qualidade, 2)

        # Gráfico de barras da distribuição sugerida
        categorias_sug = [
            f"Essenciais ({int(ess_pct*100)}%)",
            f"Lazer ({int(qual_pct*100)}%)",
            f"Investimento. ({int(pou_pct*100)}%)",
        ]
        valores_sug = [essencial, qualidade, poupanca]

        plt.figure(figsize=(6, 3))
        colors = ["#5B8FA9", "#AACFCF", "#78C3A9"]
        barras3 = plt.bar(categorias_sug, valores_sug, color=colors)
        plt.title("Distribuição Sugerida da Renda (Princípio 50-30-20)")
        plt.ylabel("R$ sugerido")
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('R$ {x:,.0f}'))

        
        for bar in barras3:
            yval = bar.get_height()
            offset = max(50, yval * 0.04)
            if yval > 1000:
                plt.text(bar.get_x() + bar.get_width()/2, yval - offset,
                         f"R$ {yval:,.0f}", ha='center', va='top',
                         fontsize=10, color='white', fontweight='bold')
            else:
                plt.text(bar.get_x() + bar.get_width()/2, yval + offset * 0.5,
                         f"R$ {yval:,.0f}", ha='center', va='bottom',
                         fontsize=10, color='black')

        
        plt.tight_layout()
        img_sug = "grafico_distribuicao_503020.png"
        plt.savefig(img_sug)
        plt.close()
        self.image(img_sug, x=25, w=160)
        os.remove(img_sug)

        self.ln(10)


    def add_grafico_evolucao_patrimonial(self, dados):
        
        # 1 Leitura dos valores
        investimento_mensal = as_float(
            dados.get("valor_investido_mes", dados.get("se_sim,_qual_a_média_de_investimento_mensal?"))
        )
        reserva_inicial = as_float(
            dados.get("reserva_emergencia", dados.get("se_sim,_qual_o_valor_atual_da_reserva?_(aproximado)"))
        )

        # 2) Construção da série
        meses = 60
        taxa_juros = 0.006  # 0,6% ao mês

        montante = reserva_inicial
        historico = []

        for _ in range(meses + 1):
            historico.append(montante)
            montante += montante * taxa_juros + investimento_mensal

        # 3) Plot da curva
        plt.figure(figsize=(7, 3.5))
        plt.plot(range(meses + 1), historico, linestyle="-", color="#198754")
        
        
    # Protege contra série toda zerada e controla as anotações
        max_val = max(historico) if historico else 0.0
        if max_val <= 0.0:
            # Define um range mínimo para evitar eixo degenerado
            plt.ylim(-1, 1)
            # Não adiciona anotações (não há o que anotar)
        else:
            # Mantém seu padrão de anotações a cada 36 meses a partir do 24
            for i in range(24, meses + 1, 36):
                # Usa um deslocamento proporcional ao valor máximo (fica adaptativo)
                offset = max_val * 0.05
                plt.text(
                    i - 3,
                    historico[i] - offset,
                    f"R$ {historico[i]:,.0f}",
                    fontsize=8,
                    fontweight="bold",
                    ha="right",
                    va="top",
                    color="black",
                )

        # 5) Títulos, eixos e salvamento
        plt.title("Evolução Simulada do Patrimônio (5 anos)")
        plt.xlabel("Meses")
        plt.ylabel("Valor Acumulado (R$)")
        plt.grid(True)
        plt.tight_layout()

        for i in [12, 24, 36, 48, 60]:
            plt.text(i - 2, historico[i] - 5000, f"R$ {historico[i]:,.0f}", fontsize=8, ha='right', va='top', fontweight='bold', color='black' )

        img_evolucao = "grafico_evolucao.png"
        plt.savefig(img_evolucao)
        plt.close()
        self.image(img_evolucao, x=20, w=170)
        os.remove(img_evolucao)
        self.ln(10)

    def add_grafico_evolucao_10anos(self, dados):

        investimento_mensal = as_float(
            dados.get("valor_investido_mes", dados.get("se_sim,_qual_a_média_de_investimento_mensal?"))
        )
        reserva_inicial = as_float(
            dados.get("reserva_emergencia", dados.get("se_sim,_qual_o_valor_atual_da_reserva?_(aproximado)"))
        )

        meses = 120
        taxa_juros = 0.006  # 0,6% ao mês

        montante = reserva_inicial
        historico = []

        for _ in range(meses + 1):
            historico.append(montante)
            montante += montante * taxa_juros + investimento_mensal

        plt.figure(figsize=(7, 3.5))
        plt.plot(range(meses + 1), historico, linestyle="-", color="#0d6efd")
        
        
    # Protege contra série toda zerada e controla as anotações
        max_val = max(historico) if historico else 0.0
        if max_val <= 0.0:
            # Define um range mínimo para evitar eixo degenerado
            plt.ylim(-1, 1)
            # Não adiciona anotações (não há o que anotar)
        else:
            # Mantém seu padrão de anotações a cada 36 meses a partir do 24
            for i in range(24, meses + 1, 36):
                # Usa um deslocamento proporcional ao valor máximo (fica adaptativo)
                offset = max_val * 0.05
                plt.text(
                    i - 3,
                    historico[i] - offset,
                    f"R$ {historico[i]:,.0f}",
                    fontsize=8,
                    fontweight="bold",
                    ha="right",
                    va="top",
                    color="black",
                )

        
        plt.title("Evolução Simulada do Patrimônio (10 anos)")
        plt.xlabel("Meses")
        plt.ylabel("Valor Acumulado (R$)")
        plt.grid(True)
        plt.tight_layout()

        for i in range(24, meses + 1, 36):
            plt.text(i - 3, historico[i] - historico[i]*0.05, f"R$ {historico[i]:,.0f}",
                    fontsize=8, fontweight='bold', ha='right', va='top', color='black')

        img = "grafico_evolucao_10anos.png"
        plt.savefig(img)
        plt.close()
        self.image(img, x=20, w=170)
        os.remove(img)
        self.ln(10)

    def add_grafico_evolucao_20anos(self, dados):

        investimento_mensal = as_float(
            dados.get("valor_investido_mes", dados.get("se_sim,_qual_a_média_de_investimento_mensal?"))
        )
        reserva_inicial = as_float(
            dados.get("reserva_emergencia", dados.get("se_sim,_qual_o_valor_atual_da_reserva?_(aproximado)"))
        )

        meses = 240
        taxa_juros = 0.006  # 0,6% ao mês

        montante = reserva_inicial
        historico = []

        for _ in range(meses + 1):
            historico.append(montante)
            montante += montante * taxa_juros + investimento_mensal

        plt.figure(figsize=(7, 3.5))
        plt.plot(range(meses + 1), historico, linestyle="-", color="#6f42c1")
        
            # Protege contra série toda zerada e controla as anotações
        max_val = max(historico) if historico else 0.0
        if max_val <= 0.0:
            # Define um range mínimo para evitar eixo degenerado
            plt.ylim(-1, 1)
            # Não adiciona anotações (não há o que anotar)
        else:
            # Mantém seu padrão de anotações a cada 36 meses a partir do 24
            for i in range(24, meses + 1, 36):
                # Usa um deslocamento proporcional ao valor máximo (fica adaptativo)
                offset = max_val * 0.05
                plt.text(
                    i - 3,
                    historico[i] - offset,
                    f"R$ {historico[i]:,.0f}",
                    fontsize=8,
                    fontweight="bold",
                    ha="right",
                    va="top",
                    color="black",
                )

        
        plt.title("Evolução Simulada do Patrimônio (20 anos)")
        plt.xlabel("Meses")
        plt.ylabel("Valor Acumulado (R$)")
        plt.grid(True)
        plt.tight_layout()

        for i in range(60, meses + 1, 60):
            plt.text(i - 3, historico[i] - historico[i]*0.05, f"R$ {historico[i]:,.0f}",
                    fontsize=8, fontweight='bold', ha='right', va='top', color='black')

        img = "grafico_evolucao_20anos.png"
        plt.savefig(img)
        plt.close()
        self.image(img, x=20, w=170)
        os.remove(img)
        self.ln(10)

    def add_estrategia_arca(self, dados):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.multi_cell(0, 12, "Estratégia Financeira - Método ARCA", ln=True, align="C")
        self.ln(8)
        perfil = (dados.get("perfil_risco") or "").strip().lower()
        aporte = dados.get("valor_investido_mes", 0)
        if "arrojado" in perfil:
            dist = {
                "Ações": 0.25,
                "FIIs (Real Estate)": 0.25,
                "Caixa / Renda Fixa": 0.25,
                "Internacional": 0.25
            }
            perfil_texto = "Perfil Arrojado"
        elif "moderado" in perfil:
            dist = {
                "Ações": 0.10,
                "FIIs (Real Estate)": 0.20,
                "Caixa / Renda Fixa": 0.60,
                "Internacional": 0.10
            }
            perfil_texto = "Perfil Moderado"
        else:
            dist = {
                "Ações": 0.05,
                "FIIs (Real Estate)": 0.10,
                "Caixa / Renda Fixa": 0.80,
                "Internacional": 0.05
            }
            perfil_texto = "Perfil Conservador"
        # Texto introdutório
        self.set_font("Helvetica", "", 12)
        explicacao = (
            f"A metodologia ARCA propõe uma diversificação estratégica em 4 classes de ativos:\n"
            f"- **Ações** (empresas perenes: bancos, energia, saneamento)\n"
            f"- **FIIs (Real Estate)**: fundos imobiliários de qualidade\n"
            f"- **Caixa / Renda Fixa**: segurança e liquidez\n"
            f"- **Internacional**: exposição ao dólar e mercados globais\n\n"
            f"Com base no seu perfil atual identificado como **{perfil_texto}**, sugerimos a seguinte distribuição dos seus aportes mensais de R$ {aporte:,.2f}.\n"
        )
        self.multi_cell(0, 8, explicacao)
        self.ln(50)
        # ---------- GRÁFICO PIZZA ----------
        import matplotlib.pyplot as plt
        labels = list(dist.keys())
        sizes = [v * 100 for v in dist.values()]
        cores = ["#5DADE2", "#F4D03F", "#58D68D", "#AF7AC5"]
        plt.figure(figsize=(5, 4))
        plt.pie(sizes, labels=labels, colors=cores, autopct="%1.0f%%", startangle=90, textprops={'fontsize': 10})
        plt.title("Distribuição ARCA sugerida (%)", fontsize=12, pad=20)
        plt.axis("equal")
        img_pizza = "grafico_arca.png"
        plt.tight_layout()
        plt.savefig(img_pizza)
        plt.close()
        self.image(img_pizza, x=35, w=140)
        os.remove(img_pizza)
        self.ln(10)
        # ---------- TABELA COM VALORES ----------
        self.set_font("Helvetica", "B", 12)
        self.cell(60, 10, "Tipo de Ativo", border=1)
        self.cell(40, 10, "Percentual", border=1)
        self.cell(0, 10, "Valor Alocado (R$)", border=1, ln=True)
        self.set_font("Helvetica", "", 12)
        for k, v in dist.items():
            self.cell(60, 10, k, border=1)
            self.cell(40, 10, f"{v*100:.0f}%", border=1)
            self.cell(0, 10, f"R$ {aporte * v:,.2f}", border=1, ln=True)
        self.ln(10)



    def add_recomendacoes(self, dados):
        self.set_font("Helvetica", "B", 13)
        self.multi_cell(0, 10, "Sugestões e Próximos Passos", ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.ln(10) # Adicionei uma quebra de linha de 10 pontos
        self.multi_cell(0, 10, 
            f"- Reforce o hábito de controle mensal com planilha ou app.\n"
            f"- Mantenha a consistência dos investimentos mensais (R$ {dados['valor_investido_mes']:.2f}).\n"
            f"- Estude sobre diversificação e perfil de risco.\n"
            f"- Seu objetivo principal é: {dados['objetivo_principal']}.\n"
            f"- Prazo estimado: {dados['prazo_objetivo'] or 'não definido'}.\n"
        )
        self.ln(10)

    def add_metas_smart(self, dados):
        self.set_fill_color(243, 255, 250)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Metas SMART e Cronograma", ln=True, fill=True)
        self.ln(5)

        self.set_font("Helvetica", "", 12)
        texto_intro = (
            "Nesta seção, definiremos objetivos financeiros usando o método SMART - "
            "uma abordagem que torna as metas mais claras, mensuráveis e alcançáveis.\n\n"
            "SMART é um acrônimo para:\n"
            "- S: Específica - O que exatamente você quer alcançar?\n"
            "- M: Mensurável - Como saberá que alcançou?\n"
            "- A: Atingível - É viável com sua realidade atual?\n"
            "- R: Relevante - Por que isso é importante para você?\n"
            "- T: Temporal - Quando pretende alcançar?\n\n"
            "Com base nas suas respostas, listamos abaixo suas principais metas:"
        )
        self.multi_cell(0, 8, texto_intro)
        self.ln(5)

        objetivo = dados.get("qual_seu_objetivo_financeiro_mais_importante_hoje", "")
        prazo = dados.get("para_esse_objetivo_você_tem_algum_prazo_específico_para_realizar", "")
        possui_dividas = as_bool(dados.get("você_possui_dívidas_atualmente", dados.get("possui_dividas")))
        reserva = float(dados.get("se_sim_qual_o_valor_atual_da_reserva_aproximado", 0) or 0)

        # Curto prazo
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "Meta de Curto Prazo (0 a 6 meses):", ln=True)
        self.set_font("Helvetica", "", 12)
        if possui_dividas or reserva < 10000:
            self.multi_cell(0, 8, "Organizar as finanças, quitar dívidas (se houver) e montar uma reserva de emergência equivalente a pelo menos 6 meses de gastos.")
        else:
            self.multi_cell(0, 8, "Otimizar seus gastos e aumentar seus aportes mensais de forma consistente.")
        self.ln(4)

        # Médio prazo
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 8, "Meta de Médio Prazo (6 a 24 meses):", ln=True)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, "Melhorar sua estratégia de investimentos, diversificar sua carteira e aumentar seu patrimônio líquido com consistência.")
        self.ln(4)

        # Longo prazo
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 8, "Meta de Longo Prazo (5+ anos):", ln=True)
        self.set_font("Helvetica", "", 12)
        if objetivo:
            self.multi_cell(0, 8, f"Atingir seu principal objetivo: {objetivo.strip()} ({prazo.strip()})")
        else:
            self.multi_cell(0, 8, "Construir patrimônio sólido visando aposentadoria, renda passiva ou independência financeira.")
        self.ln(10)

    def add_tabela_metas_smart(self, dados):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Tabela SMART: Detalhamento das Metas", ln=True)
        self.ln(4)

        
        # Larguras proporcionais às margens atuais
        total_w = self.w - self.l_margin - self.r_margin
        col_w = round(total_w / 5.0, 2)
        widths = [col_w, col_w, col_w, col_w, total_w - 4 * col_w]  # a última fecha a conta
        line_h = 7  # altura base por linha

        
        def _split_lines(text, w):
            """Usa split_only do fpdf2 quando disponível; senão, quebra simples por palavras."""
            try:
                return self.multi_cell(w, line_h, text, split_only=True)
            except TypeError:
                words = (text or "").split()
                lines, cur = [], ""
                for word in words or [""]:
                    test = (cur + " " + word).strip()
                    if self.get_string_width(test) <= (w - 2):
                        cur = test
                    else:
                        lines.append(cur)
                        cur = word
                if cur or not lines:
                    lines.append(cur)
                return lines

        
        def _tabela_row(texts, border=1, align='L'):
            """Imprime uma linha com 5 colunas, ajustando a altura pela maior célula."""
            lines_per_col = [max(1, len(_split_lines(txt, w))) for txt, w in zip(texts, widths)]
            row_h = max(lines_per_col) * line_h
            x0, y0 = self.get_x(), self.get_y()

            for txt, w in zip(texts, widths):
                x, y = self.get_x(), self.get_y()
                # retângulo da célula
                self.rect(x, y, w, row_h)
                # texto dentro da célula
                self.multi_cell(w, line_h, txt or "", border=0, align=align)
                # volta topo da célula e avança para a próxima coluna
                self.set_xy(x + w, y)
            # desce para a próxima linha da tabela
            self.set_xy(x0, y0 + row_h)



        def cabecalho_tabela():
            self.set_font("Helvetica", "B", 11)
            self.set_fill_color(200, 230, 210)
            headers = ["S", "M", "A", "R", "T"]
            for htxt, w in zip(headers, widths):
                x, y = self.get_x(), self.get_y()
                self.set_fill_color(200, 230, 210)
                self.rect(x, y, w, line_h, style='F')
                self.set_xy(x, y)
                self.cell(w, line_h, htxt, border=1, align='C')
            self.ln(line_h)


        # Tabela 1 – Curto Prazo
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "Curto Prazo (0 a 6 meses):", ln=True)
        cabecalho_tabela()
        if dados.get("você_possui_dívidas_atualmente", "").lower() == "sim":
            row1 = [
                "Quitar dívidas e montar reserva de emergência",
                "Eliminar 100% das dívidas e acumular 6 meses de despesas",
                "Reduzir gastos e manter disciplina mensal",
                "Garante segurança e reduz risco financeiro",
                "Em até 6 meses"
            ]
        else:
            row1 = [
                "Aumentar aportes mensais e otimizar gastos",
                "Aportar 20% da renda e revisar orçamento mensal",
                "Possível com ajustes simples nos gastos atuais",
                "Maximiza a capacidade de investimento",
                "Nos próximos 6 meses"
            ]
        _tabela_row(row1)

        # Tabela 2 – Médio Prazo
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "Médio Prazo (6 a 24 meses):", ln=True)
        cabecalho_tabela()
        row2 = [
            "Diversificar investimentos e aumentar patrimônio",
            "Dobrar o valor investido mensalmente e aumentar capital acumulado",
            "Com planejamento contínuo e consistência",
            "Viabiliza objetivos de médio prazo com rentabilidade",
            "Entre 6 e 24 meses"
        ]
        _tabela_row(row2)

        # Tabela 3 – Longo Prazo
        objetivo = dados.get("qual_seu_objetivo_financeiro_mais_importante_hoje", "").strip()
        prazo = dados.get("para_esse_objetivo_você_tem_algum_prazo_específico_para_realizar", "").strip()
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, "Longo Prazo (5+ anos):", ln=True)
        cabecalho_tabela()
        row3 = [
            f"Alcançar: {objetivo}" if objetivo else "Atingir independência financeira",
            "Acumular capital necessário para objetivo de longo prazo",
            "Com disciplina, aportes e boas decisões financeiras",
            "Realiza sonhos e garante estabilidade futura",
            prazo if prazo else "Em até 5 a 10 anos"
        ]
        _tabela_row(row3)

        self.ln(10)

    def add_cronograma_acao(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Cronograma / Plano de Ação", ln=True)
        self.ln(4)

        
        def _bullet_item(acao, descricao, indent=4, label_w=55, h=6):
                """
                Desenha '- <acao>:' em negrito e a descrição ao lado com quebra automática.
                """
                # prefixo '- '
                self.set_font("Helvetica", "", 11)
                self.cell(indent, h, "- ", ln=0)
                # rótulo em negrito
                self.set_font("Helvetica", "B", 11)
                self.cell(label_w, h, f"{acao}:", ln=0)
                # descrição ocupa o restante
                self.set_font("Helvetica", "", 11)
                self.multi_cell(0, h, descricao)
                self.ln(1)


        def bloco_cronograma(titulo, acoes):
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(34, 139, 34)  # verde escuro
            self.cell(0, 8, titulo, ln=True)
            self.set_text_color(0, 0, 0)

            self.set_font("Helvetica", "", 11)
            
            for acao, descricao in acoes:
                _bullet_item(acao, descricao)
                self.ln(2)


        curto_prazo = [
            ("Organizar orçamento", "Categorizar e acompanhar gastos fixos e variáveis"),
            ("Quitar dívidas", "Priorizar dívidas caras e eliminar atrasos"),
            ("Montar reserva de emergência", "   Acumular de 3 a 6 meses dos custos mensais"),
            ("Automatizar aportes", "Criar hábito de investir mensalmente, mesmo que pouco"),
        ]

        medio_prazo = [
            ("Aumentar investimentos", "Direcionar percentual maior da renda para aportes"),
            ("Diversificar ativos", "Explorar renda fixa, FIIs e ações sólidas"),
            ("Disciplina financeira", "Manter consistência nos hábitos e aprendizado"),
            ("Evoluir conhecimento", "Expandir o conhecimento com orientação"),
        ]

        longo_prazo = [
            ("Realizar metas financeiras", "Comprar imóvel, alcançar independência, etc."),
            ("Rebalancear carteira", "Ajustar a estratégia conforme mudanças"),
            ("Expandir horizontes", "Avaliar ativos internacionais ou novos negócios"),
            ("Educar dependentes", "Incluir educação financeira na família"),
        ]

        bloco_cronograma("Curto Prazo (0 a 6 meses)", curto_prazo)
        bloco_cronograma("Médio Prazo (6 a 24 meses)", medio_prazo)
        bloco_cronograma("Longo Prazo (2+ anos)", longo_prazo)
        self.ln(10)
        
            
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        from datetime import date
        data = date.today().strftime("%d/%m/%Y")
        self.cell(0, 10, f"Gerado em {data}  |  Página {self.page_no()}/{{nb}}", align="C")


    def add_disclaimer(self):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, "Disclaimers e Limitacoes", ln=True, align="C")
        self.ln(4)
        self.set_font("Helvetica", "", 11)
        texto = (
            "Este material tem caráter educacional e informativo. Não constitui recomendação de "
            "investimento, oferta, solicitação de compra ou venda de valores mobiliários. "
            "As decisões financeiras são de responsabilidade do cliente.\n\n"
            "As projeções de evolução patrimonial apresentadas são simulações baseadas em premissas "
            "definidas no documento (por exemplo, taxa de juros hipotética) e não representam garantia "
            "de resultados futuros. Resultados passados não são indicativos de performance futura.\n\n"
            "As informações utilizadas foram fornecidas pelo cliente e/ou coletadas de forma declaratória. "
            "Recomendamos revisão periódica deste plano, especialmente diante de mudanças relevantes "
            "de renda, despesas, objetivos ou perfil de risco.\n"
        )
        self.multi_cell(0, 7, texto)
        self.ln(2)
        
        
        def as_bool(val):
            # aceita bool (True/False), strings ("sim", "não", "true", "false", "1", "0", etc.) e None
            if isinstance(val, bool):
                return val
            s = str(val if val is not None else "").strip().lower()
            return s in {"sim", "s", "yes", "y", "true", "1", "on"}



def gerar_plano_pdf(dados, nome_arquivo="plano_financeiro.pdf"):
    pdf = PlanoFinanceiroPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_capa()
    pdf.add_dados_pessoais(dados)
    pdf.add_painel_financeiro(dados)
    # pdf.add_grafico_evolucao_patrimonial(dados)
    # pdf.add_grafico_evolucao_10anos(dados)
    # pdf.add_grafico_evolucao_20anos(dados)  
    pdf.add_estrategia_arca(dados)
    pdf.add_metas_smart(dados)
    pdf.add_tabela_metas_smart(dados)
    pdf.add_cronograma_acao()
    pdf.add_recomendacoes(dados)
    pdf.footer()
    pdf.add_disclaimer()
    pdf.output(nome_arquivo)
    print(f"✅ PDF gerado com sucesso: {nome_arquivo}")
