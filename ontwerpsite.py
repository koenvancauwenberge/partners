import streamlit as st
from database import get_bedrijven, get_bedrijf_postcodes
from map import maak_kaart

def laad_home():
    st.subheader("Welkom op de Homepagina")
    st.image("https://lh5.googleusercontent.com/p/AF1QipNe2uzpkg0d6uq-vbLLhLuII2aAPylAD9oe7PgS=w408-h272-k-no")

def laad_data_weergave():
    st.subheader("Data Weergave")
    bedrijven = get_bedrijven(
        server="DESKTOP-IQ2Q8UN\\SQLEXPRESS",
        database="partners"
    )
    st.write(bedrijven.head())
    st.session_state["bedrijven_data"] = bedrijven

def laad_kaart():
    st.subheader("Interactie met Kaarten")
    bedrijven_df = get_bedrijven(
        server="DESKTOP-IQ2Q8UN\\SQLEXPRESS",
        database="partners"
    )

    if "selected_btwnummer" not in st.session_state:
        st.session_state["selected_btwnummer"] = bedrijven_df["btwnummer"].iloc[0]

    geselecteerd_btwnummer = st.session_state["selected_btwnummer"]

    # Haal postcodes op
    postcodes_df = get_bedrijf_postcodes(
        server="DESKTOP-IQ2Q8UN\\SQLEXPRESS",
        database="partners",
        btwnummer=geselecteerd_btwnummer
    )
    st.session_state["postcodes_df"] = postcodes_df

    # Selectie van een bedrijf via de dropdown
    bedrijf_select = st.selectbox(
        "Selecteer een bedrijf",
        options=bedrijven_df["naam"].astype(str),
        index=int(bedrijven_df[bedrijven_df["btwnummer"] == geselecteerd_btwnummer].index[0])
    )

    geselecteerd_btwnummer_dropdown = bedrijven_df.loc[bedrijven_df["naam"] == bedrijf_select, "btwnummer"].iloc[0]
    if geselecteerd_btwnummer_dropdown != geselecteerd_btwnummer:
        st.session_state["selected_btwnummer"] = geselecteerd_btwnummer_dropdown
        st.experimental_rerun()

    # Dynamische weergave van de kaart
    maak_kaart(bedrijven_df, geselecteerd_btwnummer, postcodes_df)

    # **Toon postcodes van geselecteerde partner**
    st.write("Postcodes van het geselecteerde bedrijf:")
    st.table(postcodes_df)


def laad_instellingen():
    st.subheader("Instellingen")
    instelling = st.selectbox("Kies een instelling", ["Algemeen", "Database", "Weergave"])

    if instelling == "Algemeen":
        app_name = st.text_input("Naam van de applicatie:", "Mijn Applicatie")
        st.write(f"Applicatie heet nu: {app_name}")

    elif instelling == "Database":
        db_host = st.text_input("Database Host:", "localhost")
        db_user = st.text_input("Database Gebruiker:", "root")
        db_password = st.text_input("Wachtwoord:", type="password")

    elif instelling == "Weergave":
        theme = st.selectbox("Kies een thema:", ["Licht", "Donker"])
        st.write(f"Geselecteerd thema: {theme}")
