import streamlit as st
import pandas as pd

def _create_theme_selector():
    """Crée le sélecteur de thème"""
    st.sidebar.subheader("🎨 Thème")
    theme = st.sidebar.radio(
        "Choisir le thème:",
        options=["☀️ Clair", "🌙 Sombre"],
        key="theme_selector",
        horizontal=True
    )
    
    if theme == "🌙 Sombre":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

def _update_filter(filter_name, filter_value):
    """Met à jour le filtre dans la session_state"""
    st.session_state[filter_name] = filter_value

def create_sidebar(df):
    """Crée la barre latérale avec tous les filtres"""
    st.sidebar.title("🎛️ Filtres Interactifs")
    
    # Section d'information rapide
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Aperçu des données:**")
    st.sidebar.markdown(f"- **Période:** {df['Année'].min()} - {df['Année'].max()}")
    st.sidebar.markdown(f"- **Pays:** {len(df['Pays'].unique())}")
    st.sidebar.markdown(f"- **Gammes:** {len(df['Gamme_de_Produits'].unique())}")
    st.sidebar.markdown("---")
    
    # Sélecteur de thème
    _create_theme_selector()
    
    st.sidebar.markdown("---")
    
    # Filtres
    selected_years = _create_year_filters(df)
    selected_countries = _create_country_filters(df)
    selected_productlines = _create_product_filters(df)
    
    # Boutons d'action
    _create_action_buttons(df, selected_years, selected_countries, selected_productlines)
    
    # Indicateurs de filtres actifs
    _create_active_filters_indicator(df)

def _create_year_filters(df):
    """Crée les filtres pour les années"""
    st.sidebar.subheader("📅 Période")
    all_years = sorted(df['Année'].unique())
    
    # Utiliser une clé unique pour le widget avec callback
    selected_years = st.sidebar.multiselect(
        'Sélectionner Année(s)',
        options=all_years,
        default=st.session_state.selected_years,
        key="years_multiselect",
        on_change=lambda: _update_filter('selected_years', st.session_state.years_multiselect)
    )
    
    # Boutons de sélection rapide pour les années
    col_year1, col_year2 = st.sidebar.columns(2)
    with col_year1:
        if st.button("Toutes", key="all_years_btn", use_container_width=True):
            # Stocker l'action dans session_state et rerun
            st.session_state.pending_action = "select_all_years"
            st.rerun()
    with col_year2:
        if st.button("Dernière", key="last_year_btn", use_container_width=True):
            st.session_state.pending_action = "select_last_year"
            st.rerun()
    
    return selected_years

def _create_country_filters(df):
    """Crée les filtres pour les pays"""
    st.sidebar.subheader("🌍 Pays")
    all_countries = sorted(df['Pays'].unique())
    
    # Ajout d'une recherche pour les pays si la liste est longue
    if len(all_countries) > 10:
        search_country = st.sidebar.text_input("🔍 Rechercher un pays", key="country_search")
        if search_country:
            filtered_countries = [country for country in all_countries if search_country.lower() in country.lower()]
        else:
            filtered_countries = all_countries
    else:
        filtered_countries = all_countries
    
    # S'assurer que les valeurs par défaut existent dans les options
    valid_default_countries = [country for country in st.session_state.selected_countries if country in filtered_countries]
    
    selected_countries = st.sidebar.multiselect(
        'Sélectionner Pays',
        options=filtered_countries,
        default=valid_default_countries,
        key="countries_multiselect",
        on_change=lambda: _update_filter('selected_countries', st.session_state.countries_multiselect)
    )
    
    return selected_countries

def _create_product_filters(df):
    """Crée les filtres pour les gammes de produits"""
    st.sidebar.subheader("🏷️ Gammes de Produits")
    all_productlines = sorted(df['Gamme_de_Produits'].unique())
    
    selected_productlines = st.sidebar.multiselect(
        'Sélectionner Gamme de Produits',
        options=all_productlines,
        default=st.session_state.selected_productlines,
        key="productlines_multiselect",
        on_change=lambda: _update_filter('selected_productlines', st.session_state.productlines_multiselect)
    )
    
    return selected_productlines

def _create_action_buttons(df, selected_years, selected_countries, selected_productlines):
    """Crée les boutons d'action"""
    st.sidebar.markdown("---")
    col_reset = st.sidebar.columns(1)[0]
    
    with col_reset:
        if st.button("🔄 Réinitialiser", key="reset_btn", use_container_width=True):
            st.session_state.pending_action = "reset_all_filters"
            st.rerun()

def _create_active_filters_indicator(df):
    """Crée l'indicateur de filtres actifs"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🔍 Filtres Actifs:**")
    st.sidebar.markdown(f"- **Années:** {len(st.session_state.selected_years)}/{len(df['Année'].unique())}")
    st.sidebar.markdown(f"- **Pays:** {len(st.session_state.selected_countries)}/{len(df['Pays'].unique())}")
    st.sidebar.markdown(f"- **Gammes:** {len(st.session_state.selected_productlines)}/{len(df['Gamme_de_Produits'].unique())}")
    
    # Section de contact
    _create_contact_section()

def _create_contact_section():
    """Crée la section de contact du développeur"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("**👤 Développeur:**")
    st.sidebar.markdown("**Mamadou Lamine Gueye**")
    st.sidebar.markdown("📧 [mlamine.gueye1@univ-thies.sn](mailto:mlamine.gueye1@univ-thies.sn)")
    st.sidebar.markdown("💼 [LinkedIn](https://www.linkedin.com/in/mamadou-lamine-gueye-879103360)")
    st.sidebar.markdown("---")