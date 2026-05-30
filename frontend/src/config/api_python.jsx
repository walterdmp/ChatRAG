import axios from "axios";

const apiKey = import.meta.env.VITE_AUTHORIZATION_KEY; 

const getPythonData = async (query) => {
    try {
      const response = await axios.post("https://chat-rag-engenharia-de-dados.onrender.com/api", {
        consulta: query
      },
      {
        headers: {
            'Authorization': apiKey
        }
      });
      return response.data.mensagem;
    } catch (error) {
      console.error(error);
      return "Erro ao conectar com o servidor.";
    }
  };

export default getPythonData;