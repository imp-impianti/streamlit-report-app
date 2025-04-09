
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO

st.set_page_config(layout="wide", page_title="Metrica Interattiva")
st.title("📏 Metrica Interattiva da 0 a 3000 m")

# Upload Excel
uploaded_file = st.file_uploader("Carica file Excel con colonna 'imbocco' e 'descrizione'", type=["xlsx"])

if uploaded_file:
    if "df" not in st.session_state:
        st.session_state.df = pd.read_excel(uploaded_file)
    
    df = st.session_state.df

    if 'imbocco' in df.columns and df['imbocco'].dtype in ['int64', 'float64']:
        st.subheader("📊 Dati caricati")
        st.dataframe(df)

        # Grafico
        fig = go.Figure()
        colors = st.session_state.get("colors", {})
        color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

        for i, row in df.iterrows():
            tipo = row.get("tipo", "Generico")
            if tipo not in colors:
                colors[tipo] = color_palette[len(colors) % len(color_palette)]
            color = colors[tipo]

            fig.add_trace(go.Scatter(
                x=[row["imbocco"]], y=[0],
                mode="markers",
                marker=dict(size=12, color=color),
                name=row["descrizione"],
                hovertemplate=f"{row['descrizione']}<br>{row['imbocco']} m<br>{tipo}",
                customdata=[i],
            ))

        fig.update_layout(
            title="Visualizzazione metrica (0 - 3000 m)",
            xaxis=dict(range=[0, 3000], title="Distanza (m)", tick0=0, dtick=100),
            yaxis=dict(visible=False),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # Modifica punto
        st.subheader("🛠️ Modifica punto")
        index = st.selectbox("Seleziona un punto", options=df.index, format_func=lambda i: f"{df.loc[i, 'descrizione']} ({df.loc[i, 'imbocco']} m)")

        with st.form("modifica_form"):
            descrizione = st.text_input("Descrizione", df.loc[index, "descrizione"])
            tipo = st.text_input("Tipo", df.loc[index].get("tipo", ""))
            note = st.text_area("Note", df.loc[index].get("note", ""))

            submitted = st.form_submit_button("Salva modifiche")
            if submitted:
                df.at[index, "descrizione"] = descrizione
                df.at[index, "tipo"] = tipo
                df.at[index, "note"] = note
                st.session_state.df = df
                st.success("✅ Modifiche salvate!")

        # Download Excel aggiornato
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("📥 Scarica Excel aggiornato", data=buffer.getvalue(), file_name="dati_modificati.xlsx")

    else:
        st.error("Il file deve contenere una colonna 'imbocco' con valori numerici.")
