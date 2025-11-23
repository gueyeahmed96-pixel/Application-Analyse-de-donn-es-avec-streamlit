# Configuration globale de l'application
import streamlit as st
import os

def setup_page_config():
    st.set_page_config(
        page_title="Dashboard d'Analyse des Ventes",
        page_icon="📊",
        layout="wide"
    )

# Constantes
CACHE_TTL = 3600  # 1 heure

# Chemins possibles pour les données
DATA_PATHS = [
    "data/sales_data_cleaned.csv",      # Dans le dossier data/
    "sales_data_cleaned.csv",           # Dans le même dossier que app.py
]

def get_data_path():
    """Retourne le premier chemin de données valide"""
    for path in DATA_PATHS:
        if os.path.exists(path):
            return path
    return None