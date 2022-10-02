from tkinter import Image
import altair as alt
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import pickle
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from matplotlib import pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from pybadges import badge
from typing import Optional
from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
from streamlit_lottie import st_lottie

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="DAÑO LENTICELAR EN PALTA HASS",
    page_icon=":pear:",#None
    layout="wide",#centered
    initial_sidebar_state="collapsed",
)

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

df = pd.read_csv("https://raw.githubusercontent.com/CCozd/Dataset/main/DANIO_PIEL.csv")

# --- USER AUTHENTICATION ---
names = ["Carlos Coz", "Walter Cueva"]
usernames = ["ccozd", "wcueva"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Usuario/Contraseña incorrecta")

if authentication_status == None:
    st.warning("Por favor ingresa tu usuario y contraseña")

if authentication_status:
    # ---- READ EXCEL ----
    @st.cache
    def visualizando_análisis():
        df = pd.read_csv("https://raw.githubusercontent.com/CCozd/Dataset/main/DANIO_PIEL.csv")
        return df

    df = visualizando_análisis()

    authenticator.logout("Cerrar Sesión", "sidebar")
    st.sidebar.header("Filtra aquí:")
    fund = st.sidebar.multiselect(
        "Seleccione Fundo:",
        options=df["Fundo"].unique(),
        default=df["Fundo"].unique()
    )

    year = st.sidebar.multiselect(
        "Seleccione año:",
        options=df["Anio"].unique(),
        default=df["Anio"].unique(),
    )

    etapa = st.sidebar.multiselect(
        "Seleccione etapa:",
        options=df["Etapa"].unique(),
        default=df["Etapa"].unique()
    )

    df_selection = df.query(
        "Fundo == @fund & Anio ==@year & Etapa == @etapa"
    )
    

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_book = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_xNnXdH.json")
    st_lottie(lottie_book, speed=1, height=250, key="initial")

    
    sns.set_style("darkgrid")
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
        (0.1, 2, 0.2, 1, 0.1)
    )

    row0_1.title("Analyzing Your Goodreads Reading Habits")


    with row0_2:
        st.write("")

    row0_2.subheader(
        "A Streamlit web app by [Tyler Richards](http://www.tylerjrichards.com), get my new book on Streamlit [here!](https://www.amazon.com/Getting-Started-Streamlit-Data-Science/dp/180056550X)"
    )

    row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

    with row1_1:
        st.markdown(
            "Hey there! Welcome to Tyler's Goodreads Analysis App. This app scrapes (and never keeps or stores!) the books you've read and analyzes data about your book list, including estimating the gender breakdown of the authors, and looking at the distribution of the age and length of book you read. After some nice graphs, it tries to recommend a curated book list to you from a famous public reader, like Barack Obama or Bill Gates. One last tip, if you're on a mobile device, switch over to landscape for viewing ease. Give it a go!"
        )
        st.markdown(
            "**To begin, please enter the link to your [Goodreads profile](https://www.goodreads.com/) (or just use mine!).** 👇"
        )

    row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))






    st.write("""# Dataframe de las lesiones en la piel.
    Se muestra la base de datos en la cual se va a trabajar en el análisis y conteo de lesiones*""")
    st.dataframe(df_selection)
    numero_resultados=df_selection.shape[0]
    st.markdown(f'*N° de registros: {numero_resultados}*')


    agrupado=df_selection.groupby(by=['Semana_de_cosecha','Etapa','Fundo','Anio','Resultado']).mean()
    #agrupado=agrupado.rename(columns={'Resultado':'Puntos dañados'}) cambia el nombre de los indicadores numericos
    agrupado=agrupado.reset_index()

    st.write("""# Análisis de daño lenticelar por etapa, fundo y año representados en diagrama de cajas.
    Determinar la distribución de daños en piel y alertar a gerencia las consecuencias en las diferentes etapas, empresas y año*""")

#ANALISIS POR ETAPA
#a =pd.read_csv("https://raw.githubusercontent.com/CCozd/Dataset/main/DANIO_PIEL.csv")
#data=a.query("Anio==2022")
    fig=px.box(agrupado,x='Semana_de_cosecha',y='Resultado',color='Etapa',hover_data=['Resultado'])
    fig.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")


    fig.add_vrect(x0="20", x1="25", col=1,
              annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)


#ANALISIS POR EMPRESA
    fig1=px.box(agrupado,x='Semana_de_cosecha',y='Resultado',color='Anio',hover_data=['Resultado'])
    fig1.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig1.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig1.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")


    fig1.add_vrect(x0="20", x1="25", col=1,
              annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)

#ANALISIS POR AÑO
    fig2=px.box(agrupado,x='Semana_de_cosecha',y='Resultado',color='Fundo',hover_data=['Resultado'])
    fig2.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig2.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig2.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")


    fig2.add_vrect(x0="20", x1="25", col=1,
              annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)



    #st.plotly_chart(fig)

    col1,col2=st.columns(2)
    img=Image.open('LENTICELAS.jpg')
    col1.image(img,caption='HOLA',use_column_width=True)
    col2.plotly_chart(fig,use_container_width=True)

    col3,col4=st.columns(2)
    col3.plotly_chart(fig1,use_container_width=True)
    col4.plotly_chart(fig2,use_container_width=True)


    st.write("""# Análisis de daño lenticelar por etapa, fundo y año representados en barras.
    Determinar el promedio del N° de daños en piel y alertar a gerencia las consecuencias en las diferentes etapas, empresas y año*""")

#ANALISIS POR ETAPA
#a =pd.read_csv("https://raw.githubusercontent.com/CCozd/Dataset/main/DANIO_PIEL.csv")
#data=a.query("Anio==2022")
    fig5 =px.histogram(agrupado,x="Semana_de_cosecha",y="Resultado",color='Etapa', barmode='group',histfunc='avg', text_auto=True,height=400)
    fig5.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig5.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig5.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")
    fig5.add_vrect(x0="20", x1="25", col=1,annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)


#ANALISIS POR EMPRESA
    fig6 =px.histogram(agrupado,x="Semana_de_cosecha",y="Resultado",color='Fundo', barmode='group',histfunc='avg', text_auto=True,height=400)
    fig6.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig6.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig6.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")


    fig6.add_vrect(x0="20", x1="25", col=1,annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)

#ANALISIS POR AÑO
    fig7 =px.histogram(agrupado,x="Semana_de_cosecha",y="Resultado",color='Anio', barmode='group',histfunc='avg', text_auto=True,height=400)
    fig7.add_hline(y=8, line_dash="dot",annotation_text="8",annotation_position="bottom right")
    fig7.add_hline(y=30, line_dash="dot",annotation_text="30",annotation_position="bottom right")
    fig7.add_hline(y=125, line_dash="dot",annotation_text="125",annotation_position="bottom right")


    fig7.add_vrect(x0="20", x1="25", col=1,annotation_text="Alerta", annotation_position="top left",
              fillcolor="green", opacity=0.35, line_width=0)

    col5,col6=st.columns(2)
    img=Image.open('DAÑOS.png')
    col5.image(img,caption='HOLA',use_column_width=True)
    col6.plotly_chart(fig5,use_container_width=True)

    col7,col8=st.columns(2)
    col7.plotly_chart(fig6,use_container_width=True)
    col8.plotly_chart(fig7,use_container_width=True)

    #PARA OCULTAR HECHO POR STREAMLIT Y MENU DEPLOY
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    





    fig8=sns.jointplot(data=agrupado, x="Temperatura_minima", y="Resultado")#Si se borra kind, interno se pone puntos , si se borra hue, externo se pone barra
    st.pyplot(fig8)

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
    st.header("Citación")

    """
    ```
    Evgeny Pogrebnyak. (2021). Github data for static site generators (SSG) popularity (Version 0.1.2) [Data set]. 
    Zenodo. http://doi.org/10.5281/zenodo.4429834
    ```
    """

    st.header("Créditos")

    """
    Gracias al equipo por toda su persistencia y excelente trabajo en este análisis.

    [![Facebook Follow](https://img.shields.io/twitter/follow/PogrebnyakE?label=Follow&style=social)](https://www.facebook.com/jhord4nno)
    [![MAIL Badge](https://img.shields.io/badge/-ccozd@outlook.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:ccozd@outlook.com)](mailto:ccozd@outlook.com)
    Please use GitHub [issues](https://github.com/epogrebnyak/ssg-dataset/issues) to send
    comments and suggestions.
    (C) COZ DE LA CRUZ CARLOS
"""