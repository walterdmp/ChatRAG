from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pickle
import google.generativeai as generativeai
from geminiFunctions import gerarBuscarConsulta, melhorarResposta

load_dotenv()

app = Flask(__name__)
CORS(app) 

chave_secreta = os.getenv('GEMINI_API_KEY')
generativeai.configure(api_key=chave_secreta)

modeloEmbeddings = pickle.load(open('datasetEmbeddings.pkl','rb'))

@app.route("/api", methods=["POST"])
def results():
    auth_key = request.headers.get("Authorization")
    if auth_key != chave_secreta:
        return jsonify({"error": "Não autorizado"}), 401
        
    data = request.get_json(force=True)
    consulta = data.get("consulta", "")
    
    resultado = gerarBuscarConsulta(consulta, modeloEmbeddings)
    
    prompt = f"Consulta: {consulta} Resposta: {resultado}"
    response = melhorarResposta(prompt)
    
    return jsonify({"mensagem": response})