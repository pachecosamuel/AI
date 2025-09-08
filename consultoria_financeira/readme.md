# 📊 Consultoria Financeira Automatizada

Automatização de planos financeiros personalizados a partir de dados coletados via formulário.

---

## 📌 Objetivo
Transformar dados brutos de um diagnóstico financeiro (Google Forms) em um **plano estratégico em PDF**, com insights claros sobre a situação atual, projeções e recomendações práticas.

---

## ⚙️ Tecnologias
- Python (Pandas, ReportLab/FPDF)
- CSV (Google Forms)
- PDF estruturado com storytelling financeiro

---

## 🛠️ Funcionalidades
- Leitura de dados de diagnóstico financeiro em CSV.
- Processamento e análise das respostas:
  - Consolidação de renda, despesas, dívidas e investimentos.
  - Cálculo de indicadores (poupança mensal, percentual de endividamento, reserva).
- Geração automática de um relatório em PDF:
  - Situação Atual
  - Projeções e Insights
  - Plano Financeiro personalizado

---

## 📂 Estrutura
consultoria_financeira/
│── data/ # Exemplos de CSVs de entrada
│── etl/ # Scripts de extração e transformação
│── pdf/ # Saída e templates dos relatórios
│── plano_financeiro.py # Execução principal




---

## 🚀 Como Executar
1. Clone o repositório e acesse a pasta:
   ```sh
   git clone https://github.com/SEU_USUARIO/seu-repositorio.git
   cd consultoria_financeira
    
    poetry install

    poetry run python plano_financeiro.py
