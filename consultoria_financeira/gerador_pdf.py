# gerador_pdf.py

from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
from matplotlib.ticker import StrMethodFormatter

# Convertendo cor hex para RGB (f3fffa → 243, 255, 250)
BACKGROUND_COLOR = (243, 255, 250)

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
        categorias_acumulacao = ["Investimento Mensal", "Reserva Emergência", "Investimentos Totais"]
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
        self.ln(5)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Distribuição sugerida com base no seu perfil:", ln=True)
        self.set_font("Helvetica", "", 12)

        if sobra > 0:
            essencial = fixos
            qualidade = variaveis
            poupanca = sobra
        else:
            essencial = renda * 0.6
            qualidade = renda * 0.2
            poupanca = renda * 0.2

        categorias_sug = ["Essencial", "Qualidade de Vida", "Poupança/Investimentos"]
        valores_sug = [essencial, qualidade, poupanca]

        plt.figure(figsize=(6, 3))
        # plt.bar(categorias_sug, valores_sug, color=["#007bff", "#ffc107", "#28a745"])
        
        colors = ["#5B8FA9", "#AACFCF", "#78C3A9"]
        barras3 = plt.bar(categorias_sug, valores_sug, color=colors)
        
        for bar in barras3:
            yval = bar.get_height()
            offset = yval * 0.05
            if yval > 1000:
                plt.text(bar.get_x() + bar.get_width()/2, yval - offset*3, f"R$ {yval:,.0f}", 
                        ha='center', va='bottom', fontsize=10, color='white')
            else:
                plt.text(bar.get_x() + bar.get_width()/2, yval + offset, f"R$ {yval:,.0f}", 
                        ha='center', va='bottom', fontsize=10, color='black')



        plt.ylabel("R$ Valor sugerido")
        plt.title("Distribuição Sugerida")
        plt.tight_layout()
        img_sug = "grafico_distribuicao_sugerida.png"
        plt.savefig(img_sug)
        plt.close()
        self.image(img_sug, x=30, w=150)
        os.remove(img_sug)

        self.ln(10)

    def add_grafico_evolucao_patrimonial(self, dados):
        investimento_mensal = dados.get("valor_investido_mes", 0)
        reserva_inicial = dados.get("reserva_emergencia", 0)
        meses = 60
        taxa_juros = 0.006  # 0,6% ao mês

        montante = reserva_inicial
        historico = []

        for _ in range(meses + 1):
            historico.append(montante)
            montante += montante * taxa_juros + investimento_mensal

        plt.figure(figsize=(7, 3.5))
        plt.plot(range(meses + 1), historico, linestyle="-", color="#198754")
        plt.title("Evolução Simulada do Patrimônio (5 anos)")
        plt.xlabel("Meses")
        plt.ylabel("Valor Acumulado (R$)")
        plt.grid(True)
        plt.tight_layout()

        for i in [12, 24, 36, 48, 60]:
            plt.text(i - 2, historico[i] - 5000, f"R$ {historico[i]:,.0f}", fontsize=8, ha='right', va='top')

        img_evolucao = "grafico_evolucao.png"
        plt.savefig(img_evolucao)
        plt.close()
        self.image(img_evolucao, x=20, w=170)
        os.remove(img_evolucao)
        self.ln(10)


    def add_recomendacoes(self, dados):
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, "Sugestões e Próximos Passos", ln=True, align="C")
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

def gerar_plano_pdf(dados, nome_arquivo="plano_financeiro.pdf"):
    pdf = PlanoFinanceiroPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_capa()
    pdf.add_dados_pessoais(dados)
    pdf.add_painel_financeiro(dados)
    pdf.add_grafico_evolucao_patrimonial(dados)
    pdf.add_recomendacoes(dados)
    pdf.output(nome_arquivo)
    print(f"✅ PDF gerado com sucesso: {nome_arquivo}")
