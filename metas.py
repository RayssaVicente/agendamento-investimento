from db_config import supabase
from analise_ativos import dados_mercado


def verificar_metas_trade(enviar_telegram):
    print("🔍 Verificando metas...")

    try:
        metas = (
            supabase
            .table("ativos_carteira")
            .select("*")
            .eq("notificado", False)
            .execute()
        )

        print(f"📊 Metas encontradas: {len(metas.data)}")

        for item in metas.data:

            print(f"➡️ Analisando: {item}")

            ticker = item["ticker"]
            ticker_formatado = ticker if "." in ticker else f"{ticker}.SA"

            dados = dados_mercado(ticker_formatado)

            if not dados:
                print(f"❌ Não foi possível obter dados para {ticker}")
                continue

            preco_atual = dados.get("preco")

            print(
                f"📈 {ticker} | "
                f"Preço Atual: {preco_atual} | "
                f"Meta: {item['meta_venda']}"
            )

            if preco_atual is None:
                print(f"❌ Preço não encontrado para {ticker}")
                continue

            if preco_atual >= item["meta_venda"]:

                mensagem = (
                    f"🎯 <b>META BATIDA!</b>\n\n"
                    f"📈 Ativo: <b>{ticker}</b>\n"
                    f"💰 Preço Atual: R$ {preco_atual:.2f}\n"
                    f"🎯 Meta: R$ {item['meta_venda']:.2f}"
                )

                enviar_telegram(mensagem)

                print(f"✅ Telegram enviado para {ticker}")

                (
                    supabase
                    .table("ativos_carteira")
                    .update({"notificado": True})
                    .eq("id", item["id"])
                    .execute()
                )

                print(f"✅ Registro atualizado no Supabase")

            else:
                print(
                    f"⏳ Meta ainda não atingida "
                    f"({preco_atual:.2f} < {item['meta_venda']:.2f})"
                )

    except Exception as e:
        print(f"❌ Erro ao verificar metas: {e}")