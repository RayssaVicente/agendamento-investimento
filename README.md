# 🤖 BOT TRADER – Análise Inteligente de Investimentos

Sistema automatizado de análise de ativos (Ações, FIIs e BDRs) com envio de relatórios via Telegram.

## 📌 Sobre o Projeto

O **BOT TRADER** é um sistema desenvolvido em Python que coleta dados do mercado financeiro, realiza análises fundamentalistas e gera recomendações automáticas de investimento.

O bot executa análises periódicas e envia os resultados diretamente para um grupo no Telegram, facilitando o acompanhamento diário dos ativos.

---

## 🚀 Funcionalidades

✅ Coleta automática de dados de ativos (Ações, FIIs e BDRs)
✅ Análise fundamentalista com base em indicadores como:

* P/L (Preço/Lucro)
* P/VP (Preço/Valor Patrimonial)
* Preço justo estimado

✅ Classificação automática dos ativos:

* 🟢 COMPRA
* 🟡 HOLD
* 🔴 VENDA

✅ Geração de relatórios:

* 📊 Histórico de preços
* 📈 Ranking de ativos
* 📄 Relatório textual com análise detalhada

✅ Envio automático via Telegram:

* Mensagem formatada com análise
* Arquivos CSV e/ou relatórios

---

## 🤖 Automação com GitHub Actions

O projeto utiliza **GitHub Actions** para execução automática, sem necessidade de deixar o computador ligado.

### 🔄 Como funciona:

* O workflow é executado em horários definidos
* O bot roda automaticamente na nuvem
* Os relatórios são gerados e enviados para o Telegram

---

## 📊 Exemplo de Análise

```text
BOT TRADER – Análise Inteligente
🕒 18/03/2026 16:48

ITSA3 (Ação)
💰 Preço: R$ 13.44
📊 Preço justo: R$ 20.70
P/L: 9.74 | P/VP: 1.63
📌 🟢 COMPRA
```

---

## 📁 Estrutura do Projeto

```text
📦 agendamento-investimento
 ┣ 📜 main.py
 ┣ 📜 config.py
 ┣ 📜 historico.csv
 ┣ 📜 ranking.csv
 ┣ 📜 bot.py
 ┗ 📜 requirements.txt
```

---

## ⚙️ Tecnologias Utilizadas

* Python 🐍
* yFinance
* Pandas
* Requests
* GitHub Actions ⚙️
* Telegram 

---

## 📈 Lógica de Análise

### Ações:

* Comparação entre preço atual e preço justo
* Avaliação de múltiplos (P/L e P/VP)

### FIIs:

* < 0.9 → 🟢 COMPRA
* 0.9 - 1.0 → 🟡 HOLD
* > 1.0 → 🔴 VENDA

---

## 📦 Saídas Geradas

* 📊 `historico.csv` → evolução dos preços
* 🏆 `ranking.csv` → classificação dos ativos
* 📩 Mensagem automática no Telegram

---

## 👩‍💻 Autora

Desenvolvido por **Rayssa Silva** 🚀

---

## ⚠️ Aviso

Este projeto tem fins educacionais e não constitui recomendação financeira.
