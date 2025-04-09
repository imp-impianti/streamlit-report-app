
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime
from io import BytesIO

# --- Configurazione Streamlit ---
st.set_page_config(layout="wide", page_title="Metrica Interattiva")
st.title("📏 Metrica Interattiva da 0 a 3000 m")

# --- Caricamento dati ---
uploaded_file = st.file_uploader("Carica il file Excel con i dati", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'imbocco' in df.columns and df['imbocco'].dtype in ['int64', 'float64']:

        with st.expander("📄 Visualizza dati caricati"):
            st.dataframe(df)

        fig = go.Figure()
        colors = px.colors.qualitative.Plotly
        legenda_color = {}

        for i, row in df.iterrows():
            x = row['imbocco']
            label = row.get('descrizione', f"Punto {i}")
            tipo = row.get('tipo', 'Generico')
            colore = colors[hash(tipo) % len(colors)]
            legenda_color[tipo] = colore

            fig.add_trace(go.Scatter(
                x=[x], y=[0],
                mode='markers',
                marker=dict(size=12, color=colore),
                name=label,
                hovertemplate=f"<b>{label}</b><br>Metrica: {x} m",
                customdata=[[i]],
                hoverinfo='text'
            ))

        fig.update_layout(
            title="Visualizzazione metrica (0 - 3000 m)",
            xaxis=dict(range=[0, 3000], title="Distanza (m)", tick0=0, dtick=100),
            yaxis=dict(visible=False),
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🎨 Legenda colori per tipo oggetto"):
            for tipo, color in legenda_color.items():
                st.markdown(f"<div style='display:flex;align-items:center;'><div style='width:20px;height:20px;background:{color};margin-right:10px;border-radius:3px;'></div> {tipo}</div>", unsafe_allow_html=True)

        selected_index = st.selectbox("Seleziona un punto per modificarlo:", options=range(len(df)), format_func=lambda i: f"{df.iloc[i]['descrizione']} - {df.iloc[i]['imbocco']} m")

        if selected_index is not None:
            punto = df.iloc[selected_index]
            st.subheader("🔧 Modifica punto")

            new_descrizione = st.text_input("Descrizione", punto['descrizione'])
            new_note = st.text_area("Note", punto.get('note', ''))
            new_tipo = st.text_input("Tipo", punto.get('tipo', ''))

            if st.button("Salva modifiche"):
                df.at[selected_index, 'descrizione'] = new_descrizione
                df.at[selected_index, 'note'] = new_note
                df.at[selected_index, 'tipo'] = new_tipo

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"modifiche_dati_{timestamp}.xlsx"
                df.to_excel(save_path, index=False)
                st.success(f"Modifiche salvate in '{save_path}'")

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("📥 Scarica Excel aggiornato", buffer.getvalue(), file_name="dati_aggiornati.xlsx")

    else:
        st.error("Il file deve contenere una colonna 'imbocco' con valori numerici.")
