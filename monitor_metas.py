import time
from metas import verificar_metas_trade
from bot import enviar_telegram  # ou mova essa função pra um arquivo comum

def loop_metas():
    while True:
        print("🔍 Verificando metas...")
        verificar_metas_trade(enviar_telegram)

        print("⏳ Aguardando 15 minutos...")
        time.sleep(900)  # 900 segundos = 15 min


if __name__ == "__main__":
    loop_metas()