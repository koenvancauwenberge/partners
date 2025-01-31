import folium
from folium import GeoJson
from streamlit_folium import st_folium
import geopandas as gpd
import streamlit as st
from database import get_bedrijf_postcodes

def maak_kaart(bedrijven_df, geselecteerd_btwnummer, postcodes_df):
    # Selecteer het huidige bedrijf
    selected_partner = bedrijven_df[bedrijven_df["btwnummer"] == geselecteerd_btwnummer].iloc[0]
    m = folium.Map(location=[float(selected_partner["gpshor"]), float(selected_partner["gpsver"])], zoom_start=10)

    # Voeg markers toe voor elk bedrijf
    for _, bedrijf_row in bedrijven_df.iterrows():
        marker_color = "green" if int(bedrijf_row["partner"]) == 1 else "red"
        marker_size = 10 if int(bedrijf_row["partner"]) == 1 else 6

        folium.CircleMarker(
            location=[float(bedrijf_row["gpshor"]), float(bedrijf_row["gpsver"])],
            radius=marker_size,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.9,
            popup=f"{bedrijf_row['btwnummer']}",
            tooltip=f"Klik om {bedrijf_row['naam']} te selecteren"
        ).add_to(m)

    # Gemeentes toevoegen
    gdf = gpd.read_file("gemeenteskleiner4.gpkg")
    GeoJson(
        data=gdf.to_json(),
        style_function=lambda feature: style_function(feature, postcodes_df),
        tooltip=folium.GeoJsonTooltip(fields=["ADMUNAFR"], aliases=["Gemeente:"]),
        interactive=False
    ).add_to(m)

    # De kaart renderen
    st_map = st_folium(m, width=700, height=500)

    # **Verwerk klik op een marker**
    if st_map.get("last_object_clicked_popup"):
        clicked_btwnummer = st_map["last_object_clicked_popup"]
        st.session_state["selected_btwnummer"] = clicked_btwnummer

        # Herlaad postcodes
        postcodes_df = get_bedrijf_postcodes(clicked_btwnummer)
        st.rerun()

    # **Verwerk klik op een willekeurig punt**
    if st_map.get("last_clicked"):
        lat, lon = st_map["last_clicked"]["lat"], st_map["last_clicked"]["lng"]
        st.write(f"Je hebt geklikt op punt: Lat: {lat}, Lon: {lon}")

        # Controleer in welke gemeente dit punt valt
        clicked_location = gpd.points_from_xy([lon], [lat])
        gemeente_row = gdf[gdf.geometry.contains(clicked_location[0])]

        if not gemeente_row.empty:
            gemeente_naam = gemeente_row.iloc[0]["ADMUNAFR"]
            st.write(f"Je hebt geklikt op gemeente: {gemeente_naam}")
        else:
            st.write("Geen gemeente gevonden op deze locatie.")

    return st_map

def style_function(feature, postcodes_df):
    gemeente_postcode = feature["properties"].get("CODE_INS")
    gemeente_data = postcodes_df[postcodes_df["postcode"].str.strip() == gemeente_postcode]

    if not gemeente_data.empty:
        if gemeente_data["afgesproken"].iloc[0] == 1 and gemeente_data["verlangen"].iloc[0] == 1:
            return {"fillColor": "green", "color": "#666666", "weight": 1, "fillOpacity": 0.8}
        elif gemeente_data["afgesproken"].iloc[0] == 1:
            return {"fillColor": "purple", "color": "#666666", "weight": 1, "fillOpacity": 0.8}
        elif gemeente_data["verlangen"].iloc[0] == 1:
            return {"fillColor": "pink", "color": "#666666", "weight": 1, "fillOpacity": 0.8}

    return {"fillColor": "transparent", "color": "#666666", "weight": 0.5, "fillOpacity": 0.5}
