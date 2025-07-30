# gerador_pdf.py

from fpdf import FPDF
import matplotlib.pyplot as plt
import os

class PlanoFinanceiroPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Plano Financeiro Personalizado", ln=True, align="C")
        self.ln(10)

    def add_dados_pessoais(self, dados):
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, f"Nome: {dados['nome']}", ln=True)
        self.cell(0, 10, f"Idade: {dados['idade']}  |  Profissão: {dados['profissao']}", ln=True)
        self.cell(0, 10, f"E-mail: {dados['email']}  |  WhatsApp: {dados['telefone']}", ln=True)
        self.ln(5)

    def add_painel_financeiro(self, dados):
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, "Resumo Financeiro", ln=True)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, f"Renda mensal individual: R$ {dados['renda_individual']:.2f}", ln=True)
        self.cell(0, 10, f"Gastos fixos: R$ {dados['despesas_fixas']:.2f}", ln=True)
        self.cell(0, 10, f"Gastos variáveis: R$ {dados['despesas_variaveis']:.2f}", ln=True)
        self.cell(0, 10, f"Reserva de emergência: R$ {dados['reserva_emergencia']:.2f}", ln=True)
        self.cell(0, 10, f"Investimentos atuais: R$ {dados['valor_investido']:.2f}", ln=True)
        self.ln(5)

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
        self.cell(0, 10, "Sugestões e Próximos Passos", ln=True)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 10, 
            f"- Reforce o hábito de controle mensal com planilha ou app.\n"
            f"- Mantenha a consistência dos investimentos mensais (R$ {dados['valor_investido_mes']:.2f}).\n"
            f"- Estude sobre diversificação e perfil de risco.\n"
            f"- Seu objetivo principal é: {dados['objetivo_principal']}.\n"
            f"- Prazo estimado: {dados['prazo_objetivo'] or 'não definido'}.\n"
        )
        self.ln(5)

def gerar_plano_pdf(dados, nome_arquivo="plano_financeiro.pdf"):
    pdf = PlanoFinanceiroPDF()
    pdf.add_page()
    pdf.add_dados_pessoais(dados)
    pdf.add_painel_financeiro(dados)
    pdf.add_grafico_50_30_20(dados)
    pdf.add_recomendacoes(dados)
    pdf.output(nome_arquivo)
    print(f"✅ PDF gerado com sucesso: {nome_arquivo}")
