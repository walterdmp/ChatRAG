import React, { useContext } from "react";
import "./Main.css";
import { assets } from "../../assets/assets";
import { Context } from "../../context/Context";

const Main = () => {
  const {
    onSentApi,
    recentPrompt,
    showResult,
    loading,
    resultData,
    setInput,
    input,
  } = useContext(Context);

  const handleCardClick = (text) => {
    setInput(text);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      onSentApi();
    }
  };

  return (
    <div className="main">
      <div className="nav">
        <p>Assistente de Engenharia de Dados</p>
        <img src={assets.user_icon} alt="Usuário" />
      </div>
      <div className="main-container">
        {!showResult ? (
          <>
            <div className="greet">
              <p><span>Olá.</span></p>
              <p>Como posso ajudar com a arquitetura de dados hoje?</p>
            </div>
            <div className="cards">
              <div className="card" onClick={() => handleCardClick('Qual a diferença entre ETL e ELT?')}>
                <p>Qual a diferença entre ETL e ELT?</p>
                <img src={assets.compass_icon} alt="Dica" />
              </div>
              <div className="card" onClick={() => handleCardClick('Como o BigQuery atua na engenharia de dados?')}>
                <p>Como o BigQuery atua na engenharia de dados?</p>
                <img src={assets.bulb_icon} alt="Ideia" />
              </div>
              <div className="card" onClick={() => handleCardClick('O que é particionamento de tabelas?')}>
                <p>O que é particionamento de tabelas?</p>
                <img src={assets.message_icon} alt="Mensagem" />
              </div>
              <div className="card" onClick={() => handleCardClick('Por que usar Python em pipelines de dados?')}>
                <p>Por que usar Python em pipelines de dados?</p>
                <img src={assets.code_icon} alt="Código" />
              </div>
            </div>
          </>
        ) : (
          <div className="result">
            <div className="result-title">
              <img src={assets.user_icon} alt="Usuário" />
              <p>{recentPrompt}</p>
            </div>
            <div className="result-data">
              <img src={assets.dummy_icon} alt="Assistente" />
              {loading ? (
                <div className="loader">
                  <hr /><hr /><hr />
                </div>
              ) : (
                <p dangerouslySetInnerHTML={{ __html: resultData }}></p>
              )}
            </div>
          </div>
        )}
        
        <div className="main-bottom">
          <div className="search-box">
            <input
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown} 
              value={input}
              type="text"
              placeholder="Pergunte sobre pipelines, nuvem, bancos de dados..."
            />
            <div>
              <img onClick={() => onSentApi()} src={assets.send_icon} alt="Enviar" />
            </div>
          </div>
          <p className="bottom-info">
            Assistente RAG desenvolvido para fins de pesquisa. Respostas geradas via ChromaDB e LLM.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Main;