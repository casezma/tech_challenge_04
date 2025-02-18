from fastapi import FastAPI
import yfinance as yf
from datetime import datetime
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = FastAPI()

@app.get("/preco_acao/")
def buscar_precos( data_inicio: str, data_fim: str):
    """
    Retorna os preços de fechamento de uma ação dentro de um período específico.
    
    Parâmetros:
    - data_inicio: Data de início no formato 'YYYY-MM-DD'.
    - data_fim: Data de fim no formato 'YYYY-MM-DD'.
    
    Exemplo de chamada:
    http://127.0.0.1:8085/preco_acao/?data_inicio=2023-01-01&data_fim=2023-06-01
    """

    try:
        data_inicio_formatada = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m-%d")
        data_fim_formatada = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%Y-%m-%d")
        df = yf.download("PBR", start=data_inicio_formatada, end=data_fim_formatada)
        if df.empty:
            return {"erro": "Nenhum dado encontrado. Verifique o ticker e as datas."}
        data_close = df[["Close"]].values
        scaler = MinMaxScaler(feature_range=(0,1))
        data_scaled = scaler.fit_transform(data_close)
        seq_length = 120
        entrada_modelo = data_scaled[-seq_length:].reshape(1, seq_length, 1)
        modelo = load_model("model.h5")
        previsao_normalizada = modelo.predict(entrada_modelo)
        previsao_real = scaler.inverse_transform(previsao_normalizada)


        return {
            "preco_fechamento": int(previsao_real[0][0])
        }
    
    except Exception as e:
        return {"erro": str(e)}