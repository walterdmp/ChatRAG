import google.generativeai as generativeai
from google import genai
from google.genai import types
import numpy as np
import os

model_embedding = 'models/gemini-embedding-001'
modelo_llm = 'gemini-3-flash-preview'

def gerarBuscarConsulta(consulta, dataset):
    embedding_consulta = generativeai.embed_content(
        model=model_embedding,
        content=consulta,
        task_type="retrieval_query",
    )
    
    produtos_escalares = np.dot(np.stack(dataset["Embeddings"]), embedding_consulta['embedding']) 
    indice = np.argmax(produtos_escalares)
    
    return dataset.iloc[indice]['Conteúdo']

def melhorarResposta(inputText):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=inputText)],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""
            Você é um assistente de Engenharia de Dados baseado em RAG.
            Utilize exclusivamente o conteúdo recuperado da base de conhecimento para responder à consulta.
            Responda de forma simples, objetiva e com um tom humano e conversacional. Evite estruturas muito robóticas ou engessadas.
            Não invente dados que não estejam no contexto.
            """)
        ],
    )

    response = client.models.generate_content(
        model=modelo_llm,
        contents=contents,
        config=generate_content_config,
    )

    return response.text