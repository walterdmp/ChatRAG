import google.generativeai as generativeai
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
model_emb = 'models/gemini-embedding-001'

def gerarBuscarConsulta(consulta, collection):
    embedding_consulta = generativeai.embed_content(
        model=model_emb,
        content=consulta,
        task_type="retrieval_query",
    )
    
    resultados = collection.query(
        query_embeddings=[embedding_consulta['embedding']],
        n_results=1
    )
    
    contexto_recuperado = resultados['documents'][0][0]
    return contexto_recuperado


modelo = 'gemini-3-flash-preview'

def melhorarResposta(inputText):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = modelo
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=inputText),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
      types.Part.from_text(text="""
      Você é um assistente baseado em RAG (Retrieval-Augmented Generation).
      Utilize exclusivamente o conteúdo recuperado da base de conhecimento para responder à consulta do usuário.
      Considere a consulta e o contexto recuperado, e gere uma resposta mais humana, direta e sem parecer engessada. 
      Não invente informações que não estejam presentes no contexto fornecido.
      """),
      ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return response.text