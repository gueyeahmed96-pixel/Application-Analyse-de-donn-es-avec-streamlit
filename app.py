# Fichier principal de l'application Streamlit
import streamlit as st

# Import des modules
from config import setup_page_config
from utils.data_loader import load_data, validate_data
from utils.session_manager import initialize_session_state, handle_pending_actions
from utils.filters import get_filtered_data, validate_filtered_data
from components.sidebar import create_sidebar


# Import des onglets
from tabs.global_performance import render_global_performance_tab
from tabs.temporal_analysis import render_temporal_analysis_tab
from tabs.geographic_analysis import render_geographic_analysis_tab
from tabs.customer_segmentation import render_customer_segmentation_tab
from tabs.product_performance import render_product_performance_tab
from tabs.behavior_analysis import render_behavior_analysis_tab

def main():
    """Fonction principale de l'application"""
    
    # Configuration de la page
    setup_page_config()
    
    # Chargement des données
    df = load_data()
    df = validate_data(df)
    
    # Initialisation de l'état de session
    initialize_session_state(df)
    
    # Gérer les actions en attente (boutons cliqués)
    handle_pending_actions(df)
    
    # Barre latérale avec filtres PRINCIPAUX
    create_sidebar(df)
    
    # Application des filtres PRINCIPAUX
    df_filtered = get_filtered_data(df)
    
    # Validation des données filtrées
    if not validate_filtered_data(df_filtered):
        return
    
    # En-tête principal
    _render_main_header()
    
    # Organisation des onglets
    _render_tabs(df_filtered, df)

def _render_main_header():
    """Affiche l'en-tête principal"""
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 25px 0; border: 2px solid #E0E0E0;">
        <h1 style="color: white; font-size: 3.5em; margin-bottom: 15px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            📊 TABLEAU DE BORD ANALYTIQUE
        </h1>
        <p style="color: white; font-size: 1.8em; opacity: 0.95; font-weight: 300; margin-bottom: 10px;">
            Performances & Insights Commerciaux
        </p>
        <p style="color: #E0E0E0; font-size: 1.1em; opacity: 0.8;">
            Analyse stratégique des données de vente 2003-2005
        </p>
    </div>
    """, unsafe_allow_html=True)

def _render_tabs(df_filtered, df_original):
    """Affiche tous les onglets de l'application"""
    
    tab_globale, tab_temporelle, tab_geo, tab_client, tab_produit, tab_comportement = st.tabs([
        "🎯 Performance Globale",
        "📈 Analyse Temporelle", 
        "🌍 Analyse Géographique",
        "👥 Segmentation Clientèle",
        "🏷️ Performance Produits",
        "🛒 Comportements d'Achat et ⚡ Indicateurs Opérationnels"
    ])
    
    # Onglet Performance Globale
    with tab_globale:
        render_global_performance_tab(df_filtered, df_original)
    
    # Onglet Analyse Temporelle  
    with tab_temporelle:
        render_temporal_analysis_tab(df_filtered, df_original)
    
    # Onglet Analyse Géographique
    with tab_geo:
        render_geographic_analysis_tab(df_filtered, df_original)
    
    # Onglet Segmentation Clientèle
    with tab_client:
        render_customer_segmentation_tab(df_filtered, df_original)
    
    # Onglet Performance Produits
    with tab_produit:
        render_product_performance_tab(df_filtered, df_original)
    
    # Onglet Comportements d'Achat
    with tab_comportement:
        render_behavior_analysis_tab(df_filtered, df_original)

if __name__ == "__main__":
    main()