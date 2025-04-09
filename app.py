import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Report Generator", layout="wide")

st.title("📊 Report Generator da Excel")
uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Anteprima dei dati:", df.head())

    # Statistiche
    st.subheader("📈 Statistiche")
    st.write(df.describe())

    # Grafico 2D
    if df.select_dtypes(include='number').shape[1] >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Variabile X", df.select_dtypes(include='number').columns)
        with col2:
            y_axis = st.selectbox("Variabile Y", df.select_dtypes(include='number').columns, index=1)

        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        st.pyplot(fig)

    # Commenti
    st.subheader("📝 Aggiungi commenti al report")
    commenti = st.text_area("Scrivi qui...")

    # Esportazione
    st.subheader("📤 Esporta report")
    if st.button("Genera PDF"):
        st.info("Funzionalità di esportazione in PDF sarà disponibile nella prossima versione.")