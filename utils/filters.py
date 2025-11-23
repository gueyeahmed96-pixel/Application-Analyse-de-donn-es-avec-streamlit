import streamlit as st
import pandas as pd

def get_filtered_data(df):
    """Retourne le dataframe filtré avec gestion des erreurs"""
    try:
        filtered_df = df[
            df['Année'].isin(st.session_state.selected_years) &
            df['Pays'].isin(st.session_state.selected_countries) &
            df['Gamme_de_Produits'].isin(st.session_state.selected_productlines)
        ]
        return filtered_df
    except Exception as e:
        st.error(f"Erreur lors de l'application des filtres: {e}")
        return df

def validate_filtered_data(df_filtered):
    """Valide que les données filtrées ne sont pas vides"""
    if df_filtered.empty:
        st.warning("""
        ⚠️ **Aucune donnée ne correspond aux filtres sélectionnés.** 
        
        Suggestions:
        - Élargir la sélection des années
        - Ajouter plus de pays
        - Inclure d'autres gammes de produits
        """)
        
        # Bouton de réinitialisation rapide
        if st.button("🔄 Réinitialiser tous les filtres", key="reset_empty"):
            st.session_state.pending_action = "reset_all_filters"
            st.rerun()
        return False
    return True