from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load

# Cargar el modelo
pipeline = load('Modelo predictivo\model.joblib')

# FastAPI
app = FastAPI()

# Define el esquema para los datos de entrada
class InputData(BaseModel):
    text: str

# Define la ruta para realizar predicciones
@app.post('/predict/')
def predict(data: InputData):
    try:
        # Realiza la predicción utilizando el pipeline cargado
        prediction = pipeline.predict([data.features])[0]
        return {'prediction': prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ejecuta la aplicación FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
