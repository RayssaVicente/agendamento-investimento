import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Carrega as variáveis de ambiente
load_dotenv(override=True)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("ERRO: Variáveis SUPABASE_URL ou SUPABASE_KEY não encontradas!")

# 2. Inicializa o cliente
supabase = create_client(url, key)

# Importações internas
from bot import enviar_telegram
from analise_ativos import dados_mercado

def verificar_metas_trade():
    metas = supabase.table("ativos_carteira").select("*").eq("notificado", False).execute()
    
    for item in metas.data:
        ticker = item['ticker']
        # Formatação do Ticker
        ticker_formatado = ticker if "." in ticker else f"{ticker}.SA"
        
        meta = item['meta_venda']
        preco_compra = item['preco_compra']
        qtd = item['qtd']
        
        dados = dados_mercado(ticker_formatado)
        preco_atual = dados.get("preco")
        
        if preco_atual and preco_atual >= (meta * 0.98): 
            # --- CÁLCULO DO GANHO ---
            lucro = calcular_ganho_total(preco_atual, preco_compra, qtd)
            percentual = ((preco_atual / preco_compra) - 1) * 100
            
            mensagem = (
                f"🎯 <b>META BATIDA!</b>\n"
                f"Ativo: <b>{ticker}</b>\n"
                f"Preço Atual: R$ {preco_atual:.2f}\n"
                f"Meta definida: R$ {meta:.2f}\n"
                f"💰 <b>Ganho Total: R$ {lucro:.2f}</b>\n"
                f"📈 Rentabilidade: {percentual:.2f}%"
            )
            
            # Envia para o Telegram (o seu bot.py precisa aceitar a mensagem formatada)
            enviar_telegram(mensagem)
            
            # Atualiza no banco
            supabase.table("ativos_carteira").update({"notificado": True}).eq("id", item['id']).execute()

def calcular_ganho_total(preco_atual, preco_compra, qtd):
    investido = preco_compra * qtd
    atual = preco_atual * qtd
    return atual - investido