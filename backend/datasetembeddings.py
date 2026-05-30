import google.generativeai as generativeai
import pandas as pd
import chromadb
import os
import time 
from dotenv import load_dotenv

load_dotenv()

chave_secreta = os.getenv('GEMINI_API_KEY') 
generativeai.configure(api_key=chave_secreta)

df = pd.read_csv('base_chatRAG.csv') 

chroma_client = chromadb.PersistentClient(path="./banco_vetorial")

collection = chroma_client.get_or_create_collection(name="base_rag")

documentos = []
metadados = []
ids = []
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
                
    documentos.append(contexto) 
    metadados.append({"pergunta": pergunta}) 
    ids.append(f"linha_{index}") 
    vetores_embeddings.append(resultado['embedding'])
    
    print(f"Processando: {index + 1} de {len(df)}", end="\r")
    time.sleep(0.5)

collection.add(
    embeddings=vetores_embeddings,
    documents=documentos,
    metadatas=metadados,
    ids=ids
)

print("\n\nOs registros foram processados e salvos no ChromaDB com sucesso.")