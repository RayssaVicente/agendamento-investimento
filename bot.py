import yfinance as yf
import requests
from datetime import datetime
import os

# --- IMPORTANDO SEUS MÓDULOS ---
from salvar_dados import salvar_historico, gerar_ranking
from graficos import gerar_grafico_rendimento
from analise_ativos import dados_mercado

# ================= CONFIG =================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ativos = {
    "ITSA3.SA": {"nome": "ITSA3", "tipo": "acao"},
    "TAEE11.SA": {"nome": "TAEE11", "tipo": "acao"},
    "KLBN3.SA": {"nome": "TAEE11", "tipo": "acao"},
    "SAPR4.SA": {"nome": "SAPR4", "tipo": "acao"},
    "AAPL34.SA": {"nome": "AAPL34", "tipo": "acao"},
    "NEWL11.SA": {"nome": "NEWL11", "tipo": "fii", "valor_patrimonial": 130.77},
    "HSLG11.SA": {"nome": "HSLG11", "tipo": "fii", "valor_patrimonial": 109.83},
    "XPLG11.SA": {"nome": "XPLG11", "tipo": "fii", "valor_patrimonial": 105.72},
    "GGRC11.SA": {"nome": "GGRC11", "tipo": "fii", "valor_patrimonial": 11.21},
    "BTCI11.SA": {"nome": "BTCI11", "tipo": "fii", "valor_patrimonial": 10.12}
}

# ================= FUNÇÕES DE ENVIO =================

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def enviar_grafico_telegram():
    path_img = "graficos/rendimento.png"
    if os.path.exists(path_img):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(path_img, "rb") as photo:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": photo})

def enviar_documento_telegram(caminho_arquivo, legenda):
    """Envia arquivos CSV ou outros documentos para o Telegram"""
    if os.path.exists(caminho_arquivo):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(caminho_arquivo, "rb") as file:
            requests.post(url, data={"chat_id": CHAT_ID, "caption": legenda}, files={"document": file})

# ================= LÓGICA DE ANÁLISE =================

def analisar_acao(preco, lpa, book_value):
    if not preco or not lpa or not book_value: return None
    pl = preco / lpa
    pvp = preco / book_value
    preco_justo = lpa * 15
    score = 0
    score += 2 if pl <= 10 else 1 if pl <= 15 else -1
    score += 2 if pvp <= 1.2 else 1 if pvp <= 1.8 else -1
    decisao = "🟢 COMPRA" if score >= 3 else "🟡 HOLD" if score >= 1 else "🔴 VENDA"
    return preco, preco_justo, pl, pvp, decisao

def analisar_fii(preco, vp):
    if not preco or not vp: return None
    pvp = preco / vp
    decisao = "🟢 COMPRA" if pvp <= 0.95 else "🟡 HOLD" if pvp <= 1.10 else "🔴 VENDA"
    return preco, pvp, decisao

# ================= MAIN =================

def rodar_bot():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensagens = [f"🤖 <b>BOT TRADER – Análise Inteligente</b>\n🕒 {agora}\n"]
    lista_para_ranking = []

    for ticker, cfg in ativos.items():
        try:
            # Busca dados usando o módulo analise_ativos
            info = yf.Ticker(ticker).info
            preco = info.get("currentPrice")
            if not preco: continue

            # ===== PROCESSAMENTO AÇÕES =====
            if cfg["tipo"] == "acao":
                res = analisar_acao(preco, info.get("trailingEps"), info.get("bookValue"))
                if res:
                    preco, justo, pl, pvp, decisao = res
                    # SALVANDO DADOS NO HISTÓRICO
                    salvar_historico(cfg['nome'], preco, pvp, decisao)
                    lista_para_ranking.append({"ativo": cfg['nome'], "pvp": pvp})
                    
                    mensagens.append(
                        f"<b>{cfg['nome']}</b> (Ação)\n"
                        f"💰 Preço: R$ {preco:.2f}\n"
                        f"📊 Preço justo: R$ {justo:.2f}\n"
                        f"P/L: {pl:.2f} | P/VP: {pvp:.2f}\n"
                        f"📌 {decisao}\n"
                    )

            # ===== PROCESSAMENTO FIIs =====
            elif cfg["tipo"] == "fii":
                res = analisar_fii(preco, cfg["valor_patrimonial"])
                if res:
                    preco, pvp, decisao = res
                    # SALVANDO DADOS NO HISTÓRICO
                    salvar_historico(cfg['nome'], preco, pvp, decisao)
                    lista_para_ranking.append({"ativo": cfg['nome'], "pvp": pvp})
                    
                    mensagens.append(
                        f"<b>{cfg['nome']}</b> (FII)\n"
                        f"💰 Preço: R$ {preco:.2f}\n"
                        f"P/VP: {pvp:.2f}\n"
                        f"📌 {decisao}\n"
                    )
        except Exception as e:
            print(f"Erro ao processar {ticker}: {e}")

    # --- FINALIZAÇÃO E ENVIO DE ARQUIVOS ---
    
    # 1. Envia o relatório de texto
    enviar_telegram("\n".join(mensagens))
    
    # 2. Gera o ranking e envia o arquivo CSV
    if lista_para_ranking:
        gerar_ranking(lista_para_ranking)
        enviar_documento_telegram("dados/ranking.csv", "📊 Ranking de P/VP (Os mais baratos)")
    
    # 3. Gera o gráfico e envia (Foto + Arquivo de Histórico)
    if gerar_grafico_rendimento():
        enviar_grafico_telegram() # Envia a imagem .png
        enviar_documento_telegram("historico.csv", "📈 Histórico completo de preços")

if __name__ == "__main__":
    rodar_bot()