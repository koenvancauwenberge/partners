import streamlit as st
from ontwerpsite import laad_home, laad_data_weergave, laad_kaart, laad_instellingen

# Maak de bovenste horizontale navigatiebalk
hoofdmenu = st.radio(
    "Navigatie",
    ["Home", "Data", "Kaart", "Instellingen"],
    horizontal=True,
    label_visibility="collapsed"
)

# Toon het submenu aan de linkerkant afhankelijk van het hoofdmenu
with st.sidebar:
    if hoofdmenu == "Home":
        submenu = st.radio("Home Submenu", ["Submenu 1", "Submenu 2"])
    elif hoofdmenu == "Data":
        submenu = st.radio("Data Submenu", ["IBP", "Bizzy", "KBO"])
    elif hoofdmenu == "Kaart":
        submenu = st.radio("Kaart Submenu", ["België", "Nederland"])
    elif hoofdmenu == "Instellingen":
        submenu = st.radio("Instellingen Submenu", ["Algemene instellingen", "Database instellingen", "Weergave instellingen"])

# Inhoud van de pagina afhankelijk van de keuzes
if hoofdmenu == "Home":
    laad_home()  # Laadt de homepagina met het correcte ontwerp
    if submenu == "Submenu 1":
        st.write("Je bent op de Homepagina - Submenu 1.")
    elif submenu == "Submenu 2":
        st.write("Je bent op de Homepagina - Submenu 2.")

elif hoofdmenu == "Data":
    laad_data_weergave()  # Laadt de dataweergave-functionaliteiten
    if submenu == "IBP":
        st.write("Dataweergave - IBP data.")
    elif submenu == "Bizzy":
        st.write("Dataweergave - Bizzy data.")
    elif submenu == "KBO":
        st.write("Dataweergave - KBO data.")

elif hoofdmenu == "Kaart":
    laad_kaart()  # Laadt de interactieve kaart
    if submenu == "België":
        st.write("Kaart van België")
    elif submenu == "Nederland":
        st.write("Kaart van Nederland")

elif hoofdmenu == "Instellingen":
    laad_instellingen()  # Laadt de instellingen
    if submenu == "Algemene instellingen":
        st.write("Pas de algemene instellingen aan.")
    elif submenu == "Database instellingen":
        st.write("Pas de database-instellingen aan.")
    elif submenu == "Weergave instellingen":
        st.write("Pas de weergave-instellingen aan.")

