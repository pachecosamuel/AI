# gerador_pdf.py

from fpdf import FPDF
import matplotlib.pyplot as plt
import os

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

        # Dados brutos
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, f"Renda mensal: R$ {renda:.2f}", ln=True)
        self.cell(0, 10, f"Gastos fixos: R$ {fixos:.2f}", ln=True)
        self.cell(0, 10, f"Gastos variáveis: R$ {variaveis:.2f}", ln=True)
        self.cell(0, 10, f"Investimento mensal: R$ {investido_mes:.2f}", ln=True)
        self.cell(0, 10, f"Reserva de emergência: R$ {reserva:.2f}", ln=True)

        # Gráfico barras: Distribuição real
        categorias = ["Gastos Fixos", "Gastos Variáveis", "Investimento Mensal", "Reserva Emergência"]
        valores = [fixos, variaveis, investido_mes, reserva]

        plt.figure(figsize=(6, 3))
        plt.barh(categorias, valores, color=["#007bff", "#ff9900", "#28a745", "#6c757d"])
        plt.xlabel("R$ Valor")
        plt.title("Distribuição financeira atual")
        plt.tight_layout()
        img_grafico = "grafico_distribuicao_real.png"
        plt.savefig(img_grafico)
        plt.close()
        self.image(img_grafico, x=30, w=150)
        os.remove(img_grafico)

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
        plt.bar(categorias_sug, valores_sug, color=["#007bff", "#ffc107", "#28a745"])
        plt.ylabel("R$ Valor sugerido")
        plt.title("Distribuição Sugerida")
        plt.tight_layout()
        img_sug = "grafico_distribuicao_sugerida.png"
        plt.savefig(img_sug)
        plt.close()
        self.image(img_sug, x=30, w=150)
        os.remove(img_sug)

        self.ln(10)

    def add_grafico_50_30_20(self, dados):
        essencial = dados["renda_individual"] * 0.5
        qualidade = dados["renda_individual"] * 0.3
        poupanca = dados["renda_individual"] * 0.2

        labels = ["Essencial (50%)", "Qualidade de vida (30%)", "Poupança/Investimentos (20%)"]
        valores = [essencial, qualidade, poupanca]

        plt.figure(figsize=(5, 5))
        plt.pie(valores, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Distribuição recomendada: 50 / 30 / 20")
        caminho_img = "grafico_50_30_20.png"
        plt.savefig(caminho_img)
        plt.close()

        self.image(caminho_img, x=40, w=130)
        os.remove(caminho_img)
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
    # pdf.add_grafico_50_30_20(dados)
    pdf.add_recomendacoes(dados)
    pdf.output(nome_arquivo)
    print(f"✅ PDF gerado com sucesso: {nome_arquivo}")
