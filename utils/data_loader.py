import pandas as pd
import streamlit as st
from config import get_data_path

@st.cache_data(ttl=3600)
def load_data(filepath=None):
    """
    Charge les données depuis le fichier CSV déjà nettoyé.
    """
    # Si aucun chemin n'est fourni, utiliser le système de détection automatique
    if filepath is None:
        filepath = get_data_path()
        if filepath is None:
            return None
    
    try:
        df = pd.read_csv(filepath)
        # Assurer que la colonne de date est bien au format datetime
        df['Date_Commande'] = pd.to_datetime(df['Date_Commande'])
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

def validate_data(df):
    """Valide que les données sont chargées correctement"""
    if df is None:
        st.error("""
        Le fichier 'sales_data_cleaned.csv' est introuvable ou corrompu. 
        
        Assurez-vous qu'il se trouve dans le dossier 'data/' ou dans le même dossier que app.py.
        """)
        st.stop()
    return df