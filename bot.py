import yfinance as yf
import requests
from datetime import datetime

# ================= CONFIG =================
BOT_TOKEN = "8534388996:AAGzGJa5Cu6spw4WHQdwspARbzk28J9TMag"
CHAT_ID = 960680160

ativos = {
    # ===== AÇÕES =====
    "ITSA3.SA": {"nome": "ITSA3", "tipo": "acao"},
    "TAEE11.SA": {"nome": "TAEE11", "tipo": "acao"},
    "SAPR4.SA": {"nome": "SAPR4", "tipo": "acao"},
    "AAPL34.SA": {"nome": "AAPL34", "tipo": "acao"},

    # ===== FIIs (VP MANUAL) =====
    "NEWL11.SA": {
        "nome": "NEWL11",
        "tipo": "fii",
        "valor_patrimonial": 130.48
    },
    "VGHF11.SA": {
        "nome": "VGHF11",
        "tipo": "fii",
        "valor_patrimonial": 8.67
    }
}

# ================= FUNÇÕES =================

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    })

def analisar_acao(preco, lpa, book_value):
    if not preco or not lpa or not book_value:
        return None

    pl = preco / lpa
    pvp = preco / book_value
    preco_justo = lpa * 15

    score = 0
    score += 2 if pl <= 10 else 1 if pl <= 15 else -1
    score += 2 if pvp <= 1.2 else 1 if pvp <= 1.8 else -1

    decisao = (
        "🟢 COMPRA" if score >= 3
        else "🟡 HOLD" if score >= 1
        else "🔴 VENDA"
    )

    return preco, preco_justo, pl, pvp, decisao

def analisar_fii(preco, vp):
    if not preco or not vp:
        return None

    pvp = preco / vp

    if pvp <= 0.95:
        decisao = "🟢 COMPRA"
    elif pvp <= 1.10:
        decisao = "🟡 HOLD"
    else:
        decisao = "🔴 VENDA"

    return preco, pvp, decisao

# ================= MAIN =================

def rodar_bot():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensagens = [f"🤖 <b>BOT TRADER – Análise Inteligente</b>\n🕒 {agora}\n"]

    for ticker, cfg in ativos.items():
        info = yf.Ticker(ticker).info
        preco = info.get("currentPrice")

        # ===== AÇÕES =====
        if cfg["tipo"] == "acao":
            resultado = analisar_acao(
                preco,
                info.get("trailingEps"),
                info.get("bookValue")
            )

            if not resultado:
                continue

            preco, justo, pl, pvp, decisao = resultado
            mensagens.append(
                f"<b>{cfg['nome']}</b> (Ação)\n"
                f"💰 Preço: R$ {preco:.2f}\n"
                f"📊 Preço justo: R$ {justo:.2f}\n"
                f"P/L: {pl:.2f}\n"
                f"P/VP: {pvp:.2f}\n"
                f"📌 {decisao}\n"
            )

        # ===== FIIs =====
        elif cfg["tipo"] == "fii":
            resultado = analisar_fii(preco, cfg["valor_patrimonial"])
            if not resultado:
                continue

            preco, pvp, decisao = resultado
            mensagens.append(
                f"<b>{cfg['nome']}</b> (FII)\n"
                f"💰 Preço: R$ {preco:.2f}\n"
                f"P/VP: {pvp:.2f}\n"
                f"📌 {decisao}\n"
            )

    enviar_telegram("\n".join(mensagens))

if __name__ == "__main__":
    rodar_bot()
