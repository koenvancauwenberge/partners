import streamlit as st
from streamlit_option_menu import option_menu
from ontwerpsite import laad_home , laad_kaart, laad_instellingen
from database import laad_data_weergave
from instellingen import load_config
config = load_config()

# Hoofdmenu bovenaan de pagina
selected_main = option_menu(
    menu_title=None,  # Geen titel voor het hoofdmenu
    options=["Home", "Data", "Kaart", "Instellingen"],
    icons=["house", "bar-chart", "map", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Submenu in de zijbalk afhankelijk van de hoofdmenu-selectie
if selected_main == "Home":
    selected_sub = st.sidebar.radio("Home Submenu", ["Submenu 1", "Submenu 2"])
    laad_home()
    if selected_sub == "Submenu 1":
        st.write("Je hebt gekozen voor Home > Submenu 1.")
    elif selected_sub == "Submenu 2":
        st.write("Je hebt gekozen voor Home > Submenu 2.")

elif selected_main == "Data":
    selected_sub = st.sidebar.radio("Data Submenu", ["Bedrijven", "IBP", "Bizzy", "KBO"], index=0)
    if selected_sub == "Bedrijven":
        df_bedrijven = laad_data_weergave("Bedrijven")
        if not df_bedrijven.empty:
            st.write("Bedrijfsgegevens:", df_bedrijven)
        else:
            st.warning("Geen bedrijfsgegevens gevonden.")
        
    elif selected_sub == "IBP":
        df_ibp = laad_data_weergave("IBP")
        if not df_ibp.empty:
            st.write("IBP Gegevens:", df_ibp)
        else:
            st.warning("Geen IBP-gegevens gevonden.")
    elif selected_sub == "Bizzy":
        laad_data_weergave("Bizzy")
    elif selected_sub == "KBO":
        laad_data_weergave("KBO")

elif selected_main == "Kaart":
    selected_sub = st.sidebar.radio("Kaart Submenu", ["België", "Nederland"])
    laad_kaart()
    if selected_sub == "België":
        st.write("Je bekijkt de kaart van België.")
    elif selected_sub == "Nederland":
        st.write("Je bekijkt de kaart van Nederland.")

elif selected_main == "Instellingen":
    selected_sub = st.sidebar.radio("Instellingen Submenu", ["Algemeen", "Database", "Weergave"])
    laad_instellingen(selected_sub)

#in cmd
#eerst cd Desktop\PYTHON\PROJECTS\Partners
#git add . && git commit -m "update31-01" && git push