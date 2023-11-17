from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
from fastapi.middleware.cors import CORSMiddleware
import re, string, unicodedata
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Agrega aquí el origen de tu aplicación React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def es_entero(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def es_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def prep_text(opinion: str,stop_words,nlp):
    try:
    
        opinionP = opinion.lower() #Se pone el texto en minusculas
        
        opinionP = unicodedata.normalize('NFKD', opinionP).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        #Se quitan caracteres especiales
        opinionDoc = nlp(opinionP) #Se crea un doc con npl para procesar el texto
        tokensIN = []
        for word in opinionDoc:
            wordP = re.sub(r'[^\w\s]', '', word.text) #Remover signos de puntuación
            if wordP != '':
                if ((((es_float(word.lemma_)) or (es_entero(word.lemma_))) != True) and (word.text not in stop_words)): #No se tienen en cuenta las stop words ni los digitos
                    if(word.lemma_ == "15"):
                        print(es_float(word.lemma_))
                        print(es_entero(word.lemma_))

                    tokensIN.append(word.lemma_) #Se toma en cuenta solo el lemma de la palabra
        return tokensIN
    except Exception as ex:
        template = "An exception of type {0} occurred on the preparation of the texts. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    
# Cargar el modelo
data_M=pd.read_excel('Modelo predictivo/data/cat_345.xlsx')

pipeline = load('Modelo predictivo/model.joblib')
tokenizer = load('Modelo predictivo/tokenizer.joblib')
nlp = spacy.load('es_core_news_sm')

stop_words = nlp.Defaults.stop_words  #Stop words en español

texts = data_M['Textos_espanol']
tokensN = []

for opinion in texts:
    tI = prep_text(opinion, stop_words, nlp)
    tokensN.append(tI)

data_M['words'] = pd.Series(tokensN, copy=False)

data_M['words'] = data_M['words'].apply(lambda x: ' '.join(map(str, x)))

X_data, Y_data = data_M['words'], data_M['sdg'].astype(int)

#Vectorizer
tf_idf = TfidfVectorizer(max_features=3000)
X_data = tf_idf.fit_transform(X_data)
#print(data_M)


# Define el esquema para los datos de entrada
class InputData(BaseModel):
    text: str



# Define la ruta para realizar predicciones
@app.post('/predict/')
def predict(data: InputData):
    try:
        #stop_words = nlp.Defaults.stop_words  #Stop words en español
        print(pipeline)
        # Realiza la predicción utilizando el pipeline cargado
        
        opinion = data.text
        print(opinion)

        tokensIN = prep_text(opinion, stop_words, nlp)

        norm = [' '.join(tokensIN)]
        X_data = tf_idf.transform(norm)
        print(X_data)
        prediction = pipeline.predict(X_data)
        print(prediction)
        print(type(prediction[0]))
        """
        tfidf_estimators = prediction.estimators_
        print(tfidf_estimators)
        print("Number of trees:", len(tfidf_estimators))
        """
        
        
        #print("Trees depth (mean):", np.mean([tree.get_depth() for tree in tfidf_estimators]))
        
        return {'prediction': prediction[0].item()}
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
        print(e.__traceback__)
        raise HTTPException(status_code=500, detail=str(e))

#Ruta para ver los comentarios clasificados
@app.get('/comentarios_clasificados/')
def get_comentarios_clasificados(pred):
    print(pred)
    print(type(pred))
    print(str(pred))
    comentarios = None
    df_filtrado = data_M[data_M['sdg'] == int(pred)].head(5)
    print(data_M['sdg'].dtype)
    print(data_M['sdg'] == pred)
    print(df_filtrado)
    comentarios = df_filtrado['Textos_espanol'].tolist()
    print(comentarios)
    """
    if pred == "3":
        comentarios = data_M.loc[data_M['sdg'] == '3'].to_dict
        print(data_M.loc[data_M['sdg'] == '3'])
    elif pred == "4":
        comentarios = data_M.loc[data_M['sdg'] == '4'].to_dict
    elif pred == "5":
        comentarios = data_M.loc[data_M['sdg'] == '5'].to_dict
    print(comentarios)
    """
    return {'comentarios': comentarios}

# Ejecuta la aplicación FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
