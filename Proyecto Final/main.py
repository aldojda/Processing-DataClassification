
import  streamlit as st
from collections import Counter
import pandas as pd
import numpy as np
import re 
import json
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from wordcloud import WordCloud
from nltk.corpus import stopwords
import spacy
nlp = spacy.load("es_core_news_sm")

def lemmatize_text(text):
    doc = nlp(text)
    lemmatized = ' '.join([token.lemma_ for token in doc if not token.is_stop])
    return lemmatized

def clean_text(series):
    # Convertir la serie a una sola cadena de texto
    text = ' '.join(series.dropna().astype(str))
    # Eliminar caracteres no deseados (opcional, pero recomendado)
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Lematizar el texto
    lemmatized_text = lemmatize_text(text)
    # Eliminar stopwords adicionales que no fueron removidas por spaCy
    stop_words = set(stopwords.words('spanish'))
    stop_words.update(["maestro", "clase", "profesor", "doctor", "profe", "alumno", "dr", "doctora", "material", "maestra", "ms", "mejor"])
    words = [word for word in lemmatized_text.split() if word not in stop_words]
    cleaned_text = ' '.join(words)
    return cleaned_text

    # Crear la nube de palabras
def create_wordcloud_from_series(cleaned_text, escuela):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)
    # Mostrar la nube de palabras
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    #st.write(f"Palabras mas utilizadas por los alumnos de {escuela}")
    st.pyplot(plt)
    


def plot_top_words(words, top_n=20):
    words = words.split(" ")
    word_counts = Counter(words)
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(words, counts)
    plt.xticks(rotation=90)
    plt.xlabel('Palabras')
    plt.ylabel('Frecuencia')
    plt.title(f'Top {top_n} palabras más usadas')
    st.pyplot(fig)


# cargamos información de Escuelas
escuelas = pd.read_json('./escuelas.json', orient='records', lines=True).drop(columns = "Unnamed: 0")
categories = escuelas["Escuela"].unique()

# cargamos datos
datos = pd.read_json('./datos.json', orient='records', lines=True)
print(datos.columns)

def tabla_materias(df):
    # seleccionamos las materias con más comentarios
    materias = df["Class Name"].value_counts().index[:12]
    df_f = df[df["Class Name"].isin(materias)].groupby("Class Name").sentimiento.value_counts(normalize = True).fillna(0).unstack(-1).style.format('{:.2%}')
    return df_f

def tabla_anio(df):
    # seleccionamos las materias con más comentarios
    df["year"] = df.Date.dt.year
    df_f = df.groupby(["year"]).sentimiento.value_counts(normalize = True).fillna(0.0).unstack(0).T.reset_index() # .style.format('{:.2%}')
    fig, ax = plt.subplots(figsize=(10, 5))
    for column in ["postivo", "negativo"]:
        ax.plot(df_f['year'], df_f[column], label=column)
    ax.set_xlabel('Year')
    ax.set_ylabel('%')
    ax.set_title('Sentimiento anual por años')
    ax.legend()
    return st.pyplot(fig)
    


def main():
    st.title('Análisis de Sentimiento a comentarios Realizados en MisProfesores.com')
    selected_category = st.selectbox("Seleccionar una Escuela para hacer Web Scrapping", categories)
    datos_f= datos[datos.escuela == selected_category] 
    # eliminar al cambiar el dato
    # generamos dos conjuntos de datos para comparar
    datos_positivos = datos_f[datos_f.sentimiento == "postivo"]
    # generamos dos conjuntos de datos para comparar
    datos_negativos = datos_f[datos_f.sentimiento == "negativo"]


    for key, dat in {"positivas": datos_positivos , "negativas": datos_negativos}.items():
        st.header(f"Palabras mas utilizadas por los alumnos con calificaciones {key}")
        # generamos nube de palabras
        cleaned_text = clean_text(dat.Comments)
        create_wordcloud_from_series(cleaned_text, selected_category)
        plot_top_words(cleaned_text, top_n=20)
    
    # desplegamos los resultados de las 5 materias mas comunes 
    st.header(f"Así es cómo los alumnos de la {selected_category} se sienten a lo largo de los años")
    tabla_anio(datos_f)

    st.header(f"estas fueron las calificaciones de las materias más comentadas de {selected_category}")
    st.dataframe( tabla_materias(datos_f))
    
    st.write(f"aqui puedes observar los datos por si tienes curiosidad de lo que dicen los usuarios!")
    st.dataframe( datos_positivos)

if __name__ == "__main__":
    main()
    





