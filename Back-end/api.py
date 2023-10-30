from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
from fastapi.middleware.cors import CORSMiddleware

# Cargar el modelo
pipeline = load('C:/Users/ADMIN/Documents/Semestre 8/BI/Proyecto/Etapa 1/Proyecto1_Inteligencia_de_Negocios/Modelo predictivo/model.joblib')

# FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Agrega aquí el origen de tu aplicación React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define el esquema para los datos de entrada
class InputData(BaseModel):
    text: str

# Define la ruta para realizar predicciones
@app.post('/predict/')
def predict(data: InputData):
    try:
        print(pipeline)
        # Realiza la predicción utilizando el pipeline cargado
        print(data.text)
        prediction = pipeline.predict(data.text)
        print(prediction)
        print(prediction.estimators_)
        return {'prediction': prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Ruta para ver los comentarios clasificados
@app.get('/comentarios_clasificados/')
def get_comentarios_clasificados():
    comentarios = df.to_dict(orient='records')
    return {'comentarios': comentarios}

# Ejecuta la aplicación FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
