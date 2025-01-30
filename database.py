from sqlalchemy import create_engine
import pandas as pd

def get_sql_data(server: str, database: str, query: str) -> pd.DataFrame:
    conn_str = (
        f"mssql+pyodbc://{server}/{database}?"
        "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def get_bedrijven(server, database):
    query = """
        SELECT btwnummer, naam, gpshor, gpsver, partner, wiltsamenwerken, wijwillensamenwerken, opmerking
        FROM bedrijven
        WHERE gpshor IS NOT NULL AND gpsver IS NOT NULL
    """
    return get_sql_data(server, database, query)

def get_bedrijf_postcodes(server, database, btwnummer):
    query = f"""
        SELECT postcode, afgesproken, verlangen
        FROM postcodes
        WHERE btwnummer = '{btwnummer}'
    """
    return get_sql_data(server, database, query)
