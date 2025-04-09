
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide", page_title="Griglia Interattiva")

st.title("📊 Mappa Interattiva - Censimento Oggetti")

# Percorso file Excel
excel_file = "griglia_interattiva_dati.xlsx"

# Inizializza i dati se il file non esiste
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=["Colonna", "Riga", "Oggetto", "Difetto", "Intensità", "Foto", "Info"])
    df.to_excel(excel_file, index=False)

# Carica dati esistenti
df = pd.read_excel(excel_file)

# Definizione griglia (semplificata)
righe = list(range(1, 6))
colonne = ["RS", "RD", "C", "PS", "PD"]

# Crea layout griglia
st.subheader("🗺️ Clicca su una cella della griglia")

col1, col2 = st.columns([1, 3])

with col2:
    for r in righe:
        cols = st.columns(len(colonne))
        for i, c in enumerate(colonne):
            cell_label = f"{c}-{r}"
            if cols[i].button(cell_label):
                st.session_state.selected_cell = (c, r)

# Se una cella è stata selezionata
if "selected_cell" in st.session_state:
    col_sel, row_sel = st.session_state.selected_cell
    st.markdown(f"### ✍️ Inserisci dati per la cella: **{col_sel}-{row_sel}**")

    with st.form("form_dati"):
        oggetto = st.selectbox("Oggetto", ["Telecamera", "Sensore", "Altro"])
        difetto = st.selectbox("Difetto", ["Menu a tendina", "Connessione", "Assente", "Lente sporca"])
        intensita = st.radio("Intensità", ["P", "S"])
        foto = st.text_input("Nome file foto (es. foto1.jpg)")
        info = st.text_area("Info aggiuntive")
        submit = st.form_submit_button("Salva")

        if submit:
            nuovo_record = pd.DataFrame([{
                "Colonna": col_sel,
                "Riga": row_sel,
                "Oggetto": oggetto,
                "Difetto": difetto,
                "Intensità": intensita,
                "Foto": foto,
                "Info": info
            }])

            df = pd.concat([df, nuovo_record], ignore_index=True)
            df.to_excel(excel_file, index=False)
            st.success("Dati salvati correttamente!")

# Mostra anteprima dati
st.markdown("---")
st.subheader("📄 Dati inseriti")
st.dataframe(df, use_container_width=True)

# Mostra timestamp salvataggio
st.caption(f"Ultimo aggiornamento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
