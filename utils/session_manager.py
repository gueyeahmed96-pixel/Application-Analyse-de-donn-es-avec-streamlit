import streamlit as st

def initialize_session_state(df):
    """Initialise ou réinitialise l'état de session pour les filtres"""
    default_filters = {
        'filters_applied': False,
        'selected_years': sorted(df['Année'].unique()),
        'selected_countries': sorted(df['Pays'].unique()),
        'selected_productlines': sorted(df['Gamme_de_Produits'].unique()),
        'data_loaded': True,
        'df_original': df,
        'pending_action': None,
        # AJOUT DES FILTRES INDICATEURS
        'indicator_years': sorted(df['Année'].unique()),
        'indicator_countries': sorted(df['Pays'].unique()),
        'indicator_products': sorted(df['Gamme_de_Produits'].unique())
    }
    
    for key, value in default_filters.items():
        if key not in st.session_state:
            st.session_state[key] = value

def handle_pending_actions(df):
    """Gère les actions en attente (boutons cliqués)"""
    if hasattr(st.session_state, 'pending_action') and st.session_state.pending_action:
        action = st.session_state.pending_action
        
        if action == "select_all_years":
            st.session_state.selected_years = sorted(df['Année'].unique())
            st.session_state.filters_applied = True
            
        elif action == "select_last_year":
            all_years = sorted(df['Année'].unique())
            st.session_state.selected_years = [all_years[-1]] if all_years else []
            st.session_state.filters_applied = True
            
        elif action == "reset_all_filters":
            st.session_state.selected_years = sorted(df['Année'].unique())
            st.session_state.selected_countries = sorted(df['Pays'].unique())
            st.session_state.selected_productlines = sorted(df['Gamme_de_Produits'].unique())
            st.session_state.filters_applied = True
        
        # Réinitialiser l'action
        st.session_state.pending_action = None
        st.rerun()

def get_session_filters():
    """Retourne les filtres actuels de la session"""
    return {
        'years': st.session_state.selected_years,
        'countries': st.session_state.selected_countries,
        'productlines': st.session_state.selected_productlines
    }