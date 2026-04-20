import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analyse Lemba", layout="wide")
st.title("⚡ Analyseur Électrique - Lemba")

uploaded_file = st.sidebar.file_uploader("Importer votre fichier Excel", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        
        # Nettoyage des colonnes
        df.columns = [" ".join(str(c).strip().split()) for c in df.columns]
        
        # Mapping pour uniformiser les noms
        mapping = {
            "DATE": "Date", "HEURE": "Heure", 
            "CONSOMMATION (KWH)": "Consommation(kWh)", "CONSOMMATION(KWH)": "Consommation(kWh)",
            "SECTEUR": "Secteur"
        }
        df.columns = [mapping.get(c.upper(), c) for c in df.columns]

        if all(col in df.columns for col in ["Date", "Heure", "Consommation(kWh)", "Secteur"]):
            df['Consommation(kWh)'] = pd.to_numeric(df['Consommation(kWh)'], errors='coerce')
            df['Timeline'] = df['Date'].astype(str) + " " + df['Heure'].astype(str)

            secteurs = df['Secteur'].unique()
            choix = st.sidebar.multiselect("Secteurs", secteurs, default=secteurs)
            df_filtre = df[df['Secteur'].isin(choix)]

            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Total kWh", round(df_filtre['Consommation(kWh)'].sum(), 2))
                st.dataframe(df_filtre.groupby('Secteur')['Consommation(kWh)'].sum())
            with c2:
                fig = px.line(df_filtre, x='Timeline', y='Consommation(kWh)', color='Secteur', markers=True)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Colonnes manquantes dans le fichier.")
    except Exception as e:
        st.error(f"Erreur : {e}")
else:
    st.info("Veuillez charger votre fichier Excel.")
    