import streamlit as st
import pandas as pd
from database import get_bedrijven, get_bedrijf_postcodes
from map import maak_kaart
from sqlalchemy import create_engine
import configparser
from instellingen import load_config
config = load_config()

# Haal de database-instellingen op
#db_host = config.get('Database', 'host')
#db_user = config.get('Database', 'user')
#db_password = config.get('Database', 'password')
ibp_tabel = config.get('Database', 'ibp_tabel')
print(ibp_tabel)

def laad_home():
    st.subheader("Welkom op de Homepagina")
    st.image("https://lh5.googleusercontent.com/p/AF1QipNe2uzpkg0d6uq-vbLLhLuII2aAPylAD9oe7PgS=w408-h272-k-no")

def toon_data(optie):
    st.subheader(f"Data Weergave - {optie}")
    try:
        df_result = laad_data_weergave(optie)
        if df_result.empty:
            st.warning("Geen gegevens gevonden.")
        else:
            st.write(df_result.head())
    except Exception as e:
        st.error(str(e))



"""    
def get_sql_data(server: str, database: str, query: str) -> pd.DataFrame:
    conn_str = (
        f"mssql+pyodbc://{server}/{database}?"
        "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
"""


def laad_kaart():
    st.subheader("Interactie met Kaarten")
    bedrijven_df = get_bedrijven()

    if "selected_btwnummer" not in st.session_state:
        st.session_state["selected_btwnummer"] = bedrijven_df["btwnummer"].iloc[0]

    geselecteerd_btwnummer = st.session_state["selected_btwnummer"]

    # Haal postcodes op
    postcodes_df = get_bedrijf_postcodes(geselecteerd_btwnummer)
    
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

def laad_instellingen(optie):
    st.subheader(f"Instellingen - {optie}")
    if optie == "Algemeen":
        st.write("Algemene instellingen aanpassen.")
        app_name = st.text_input("Naam van de applicatie:", "Mijn Applicatie")
        st.write(f"Applicatie heet nu: {app_name}")
    elif optie == "Database":
        st.write("Database instellingen aanpassen.")
        
        # Huidige instellingen ophalen
        db_host = config.get('Database', 'host')
        db_user = config.get('Database', 'user')
        db_password = config.get('Database', 'password')
        ibp_tabel = config.get('Database', 'ibp_tabel')
        
        # Instellingen weergeven in invoervelden
        db_host = st.text_input("Database Host:", db_host)
        db_user = st.text_input("Database Gebruiker:", db_user)
        db_password = st.text_input("Wachtwoord:", db_password, type="password")
        ibp_tabel = st.text_input("Huidige IBP-tabel:", ibp_tabel)
        
        if st.button("Opslaan"):
            # Wijzigingen opslaan in het configuratiebestand
            config.set('Database', 'host', db_host)
            config.set('Database', 'user', db_user)
            config.set('Database', 'password', db_password)
            config.set('Database', 'ibp_tabel', ibp_tabel)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            st.success("Instellingen zijn opgeslagen.")
