import axios from "axios";

const apiKey = import.meta.env.VITE_AUTHORIZATION_KEY; 

const getPythonData = async (query) => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api", {
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
      return "Erro ao conectar com o servidor local.";
    }
  };

export default getPythonData;