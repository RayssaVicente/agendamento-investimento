import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_grafico_rendimento():
    if not os.path.exists("historico.csv"): return False
    
    df = pd.read_csv("historico.csv")
    df['data'] = pd.to_datetime(df['data'])
    
    plt.figure(figsize=(10, 6))
    for ativo in df['ativo'].unique():
        dados_ativo = df[df['ativo'] == ativo]
        plt.plot(dados_ativo['data'], dados_ativo['preco'], marker='o', label=ativo)
    
    plt.title("Evolução de Preços dos Ativos")
    plt.xlabel("Data")
    plt.ylabel("Preço (R$)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if not os.path.exists("graficos"): os.makedirs("graficos")
    plt.savefig("graficos/rendimento.png")
    plt.close()
    return True