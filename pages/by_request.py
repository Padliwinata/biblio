import pandas as pd
import requests
import streamlit as st


st.title("These data are provided by request")
st.write("The 'app' page can be explored to get another data or just request to get another specific data")

st.sidebar.write("This image of a cat to cheer your day")
res = requests.get("https://api.thecatapi.com/v1/images/search")
st.sidebar.image(res.json()[0]['url'], width=200)

tab1, tab2 = st.tabs(['Indonesia', 'Unpad'])

with tab1:
    st.header("Gender research trend in Indonesia (2020-2025)")
    df = pd.read_csv('pages/datasets/gender_trend_indonesia.csv')
    df = df.drop(columns=["Unnamed: 0"])
    st.dataframe(df)
    st.write('Specific with "gender" keyword')
    df = pd.read_csv('pages/datasets/gender_trend_indonesia_specific.csv')
    df = df.drop(columns=["Unnamed: 0"])
    st.dataframe(df)

with tab2:
    st.header("Gender research trend in Unpad (2020-2025)")
    df = pd.read_csv('pages/datasets/gender_trend_unpad.csv')
    df = df.drop(columns=["Unnamed: 0"])
    st.dataframe(df)
    st.write('Specific with "gender" keyword')
    df = pd.read_csv('pages/datasets/gender_trend_unpad_specific.csv')
    df = df.drop(columns=["Unnamed: 0"])
    st.dataframe(df)


