from fpdf import FPDF
from fpdf.enums import XPos, YPos
import pandas as pd


class PDF(FPDF):
    def header(self):
        # Título no topo
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(25, 135, 84)
        self.cell(
            0,
            10,
            "Consultoria Financeira - Mapa do Tesouro",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
        )
        self.ln(5)


def gerar_mapa_tesouro(csv_path, nome_arquivo="mapa_tesouro.pdf"):
    # Lê CSV
    df = pd.read_csv(csv_path)
    dados = df.iloc[0].to_dict()

    # Cria PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Capa
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(
        0,
        20,
        "MAPA DO TESOURO FINANCEIRO",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
        align="C",
    )
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(
        0,
        10,
        "Consultoria de Samuel Pacheco",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
        align="C",
    )
    pdf.ln(10)

    # Dados do cliente
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(
        0, 10, "Dados do Cliente:", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L"
    )
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0,
        8,
        f"Nome: {dados.get('nome_completo', '')}\nIdade: {dados.get('idade', '')}\nProfissão: {dados.get('profissão', '')}\nEmail: {dados.get('seu_melhor_email', '')}\nWhatsApp: {dados.get('celular_com_ddd', '')}",
    )
    pdf.ln(10)

    # Checklist
    checklist = [
        "Abrir conta em corretora nacional",
        "Abrir conta em corretora internacional",
        "Criar reserva de emergência",
        "Aprender a enviar ordem de compra na bolsa",
        "Configurar aportes mensais automáticos",
        "Estudar perfil ARCA e definir alocação inicial",
        "Executar primeiro investimento em renda fixa",
        "Executar primeiro investimento em FIIs",
        "Executar primeiro investimento em ações",
        "Executar primeiro investimento internacional",
    ]

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(
        0,
        10,
        "Checklist Financeiro:",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
        align="L",
    )
    pdf.set_font("Helvetica", "", 11)

    for i, item in enumerate(checklist, 1):
        # sanitiza texto para evitar erro de largura
        texto = f"{i}. {item}".replace("–", "-").replace("—", "-").replace("•", "-")
        pdf.multi_cell(180, 8, texto, align="L")

    # Salva
    pdf.output(nome_arquivo)
    print(f"✅ PDF '{nome_arquivo}' gerado com sucesso!")


if __name__ == "__main__":
    gerar_mapa_tesouro(
        "../docs/diagnostico_financeiro_samuel.csv", nome_arquivo="mapa_tesouro_samuel.pdf"
    )
