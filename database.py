from sqlalchemy import create_engine
import pandas as pd
from instellingen import load_config
config = load_config()

def get_sql_data(query: str) -> pd.DataFrame:
    server = config.get('Database', 'server')
    database = config.get('Database', 'database')
    conn_str = (
        f"mssql+pyodbc://{server}/{database}?"
        "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def laad_data_weergave(optie):
    if optie == "Bedrijven":
        query = "SELECT * FROM bedrijven"
    elif optie == "IBP":
        ibp_tabel = config.get('Database', 'ibp_tabel')
        query = f"SELECT * FROM {ibp_tabel}"
    elif optie == "Bizzy":
        query = "SELECT * FROM bizzy"
    elif optie == "KBO":
        query = "SELECT * FROM kbo"
    else:
        raise ValueError("Onbekende data-optie.")

    try:
        df_result = get_sql_data(query)
        return df_result
    except Exception as e:
        raise RuntimeError(f"Fout bij het ophalen van gegevens: {e}")
        
def get_bedrijven() -> pd.DataFrame:
    query = """
        SELECT btwnummer, naam, gpshor, gpsver, partner, wiltsamenwerken, wijwillensamenwerken, opmerking
        FROM bedrijven
        WHERE gpshor IS NOT NULL AND gpsver IS NOT NULL
    """
    return get_sql_data(query)

def get_bedrijf_postcodes(btwnummer: str) -> pd.DataFrame:
    query = f"""
        SELECT postcode, afgesproken, verlangen
        FROM postcodes
        WHERE btwnummer = '{btwnummer}'
    """
    return get_sql_data(query)


