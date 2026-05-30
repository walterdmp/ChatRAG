from flask import Flask, jsonify, request
import google.generativeai as generativeai
import chromadb
from flask_cors import CORS
from dotenv import load_dotenv
import os
from geminiFunctions import gerarBuscarConsulta, melhorarResposta

load_dotenv()
app = Flask(__name__)
CORS(app)  

chave_secreta = os.getenv('GEMINI_API_KEY')
generativeai.configure(api_key=chave_secreta)

chroma_client = chromadb.PersistentClient(path="./banco_vetorial")
collection = chroma_client.get_collection(name="base_rag")

@app.route("/")
def home():
    consulta = "O que é Engenharia de Dados?"
    resposta = gerarBuscarConsulta(consulta, collection)
    prompt = f"Consulta: {consulta} Contexto: {resposta}"
    response = melhorarResposta(prompt)
    return response

@app.route("/api", methods=["POST"])
def results():
    auth_key = request.headers.get("Authorization")
    if auth_key != chave_secreta:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json(force=True)
    consulta = data["consulta"]
    
    resultado = gerarBuscarConsulta(consulta, collection)
    prompt = f"Consulta: {consulta} Contexto: {resultado}"
    response = melhorarResposta(prompt)
    
    return jsonify({"mensagem":  response})

if __name__ == '__main__':
    app.run(debug=True)