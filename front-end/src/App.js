import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [prediction, setPrediction] = useState(null);

  const [comentarios, setComentarios] = useState([]);

  useEffect(() => {
    async function fetchComentarios() {
      try {
        const response = await fetch('http://localhost:8000/comentarios_clasificados/', {
          method: 'GET',
          mode: "cors",
          cache: "no-cache",
          credentials: "same-origin",
          headers: {
            'Content-Type': 'application/json'
          },
          redirect: "follow",
          referrerPolicy: "no-referrer",
          body: JSON.stringify({ pred: prediction })
        });
        const data = await response.json();
        setComentarios(data.comentarios);
      } catch (error) {
        console.error('Error:', error);
      }
    }

    fetchComentarios();
  }, []);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(inputText)
      const response = await fetch('http://localhost:8000/predict/', {
        method: 'POST',
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          'Content-Type': 'application/json'
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify({ text: inputText })
      });

      const data = await response.json();
      console.log(response)
      setPrediction(data.prediction);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Clasificador de Texto</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          value={inputText}
          onChange={handleInputChange}
          placeholder="Ingrese un texto..."
        />
        <br />
        <button type="submit">Predecir</button>
      </form>
      {prediction !== null && (
        <div>
          <h2>Predicción:</h2>
          <p>{prediction}</p>
        </div>
      )}

      <div>
          <h1>Comentarios Clasificados</h1>
          <ul>
            {comentarios.map((comentario, index) => (
              <li key={index}>
                <strong>Comentario:</strong> {comentario.comentario}, <strong>Clasificación:</strong> {comentario.clasificacion}
              </li>
            ))}
          </ul>
      </div>
    </div>
    
  );
}

export default App;
