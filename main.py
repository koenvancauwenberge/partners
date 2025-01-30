import streamlit as st
from ontwerpsite import laad_home, laad_data_weergave, laad_kaart, laad_instellingen

st.title("Mijn partners")

menu = st.sidebar.selectbox(
    "Hoofdmenu",
    ["Home", "Data Weergave", "Kaart", "Instellingen"]
)

if menu == "Home":
    laad_home()
elif menu == "Data Weergave":
    laad_data_weergave()
elif menu == "Kaart":
    laad_kaart()
elif menu == "Instellingen":
    laad_instellingen()
