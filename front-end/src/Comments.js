import React, { useState, useEffect } from 'react';

function Comments() {
  const [comentarios, setComentarios] = useState([]);

  useEffect(() => {
    async function fetchComentarios() {
      try {
        const response = await fetch('http://localhost:8000/comentarios_clasificados/', {
            method: 'POST',
            mode: "no-cors",
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
        setComentarios(data.comentarios);
      } catch (error) {
        console.error('Error:', error);
      }
    }

    fetchComentarios();
  }, []);

  return (
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
  );
}

export default Comments;
