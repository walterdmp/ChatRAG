import google.generativeai as generativeai
import pandas as pd
import os
import time 
import pickle
from dotenv import load_dotenv

load_dotenv()

chave_secreta = os.getenv('GEMINI_API_KEY') 
generativeai.configure(api_key=chave_secreta)

df = pd.read_csv('base_chatRAG.csv') 

if 'Contexto' in df.columns:
    df['Conteúdo'] = df['Contexto']

vetores_embeddings = []
modelo = 'models/gemini-embedding-001'

print("Gerando os embeddings no Google AI Studio...")

for index, row in df.iterrows():
    pergunta = str(row['Pergunta'])
    contexto = str(row['Contexto'])
    
    texto_completo = f"Pergunta: {pergunta} | Contexto: {contexto}"
    
    sucesso = False
    while not sucesso:
        try:
            resultado = generativeai.embed_content(
                model=modelo,
                content=texto_completo,
                task_type="retrieval_document",
                title=pergunta
            )
            sucesso = True 
            
        except Exception as e:
            erro_str = str(e)
            if "429" in erro_str or "Quota exceeded" in erro_str:
                print(f"\n[Aviso] Limite de 100 requisições atingido. Pausando por 60 segundos na linha {index}...")
                time.sleep(60) 
            else:
                raise e 
                
    vetores_embeddings.append(resultado['embedding'])
    
    print(f"Processando: {index + 1} de {len(df)}", end="\r")
    time.sleep(0.5)

df["Embeddings"] = vetores_embeddings

print("\n\nSalvando a base de dados no formato leve (.pkl)...")
pickle.dump(df, open('datasetEmbeddings.pkl','wb'))

print("Arquivo datasetEmbeddings.pkl gerado com sucesso!")