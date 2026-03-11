import pandas as pd
import os
from datetime import datetime

def salvar_historico(ativo, preco, pvp, decisao):
    file_path = "historico.csv"
    data = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ativo": ativo,
        "preco": preco,
        "pvp": pvp,
        "decisao": decisao
    }
    df_novo = pd.DataFrame([data])

    # Se o arquivo não existe, cria com cabeçalho. Se existe, apenas adiciona (append).
    if not os.path.exists(file_path):
        df_novo.to_csv(file_path, index=False)
    else:
        df_novo.to_csv(file_path, mode='a', header=False, index=False)

def gerar_ranking(ativos_lista):
    # Salva um ranking atualizado na pasta dados/
    df = pd.DataFrame(ativos_lista)
    if not os.path.exists("dados"): os.makedirs("dados")
    df.sort_values(by="pvp", ascending=True).to_csv("dados/ranking.csv", index=False)