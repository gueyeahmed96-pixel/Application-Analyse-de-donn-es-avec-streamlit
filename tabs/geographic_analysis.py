import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_geographic_analysis_tab(df_filtered, df_original):
    """Affiche l'onglet Analyse Géographique"""
    
    # Création d'onglets pour organiser les différentes vues géographiques
    tab_geo1, tab_geo2, tab_geo3 = st.tabs(["📊 Carte Mondiale", "📈 Top Pays", "🔍 Détails par Ville"])
    
    with tab_geo1:
        _render_world_map(df_filtered)
    
    with tab_geo2:
        _render_country_analysis(df_filtered)
    
    with tab_geo3:
        _render_city_analysis(df_filtered)

def _render_world_map(df_filtered):
    """Affiche la carte mondiale"""
    # --- Préparation des données pour la cartographie ---
    performance_pays = df_filtered.groupby('Pays').agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique',
        'Quantité_Commandée': 'sum'
    }).sort_values("Chiffre d'Affaires", ascending=False).reset_index()

    # Utiliser les données de Gapminder pour obtenir les codes ISO des pays
    try:
        gapminder = px.data.gapminder().query("year==2007")
        country_iso_map = gapminder.set_index('country')['iso_alpha'].to_dict()

        # Gérer les exceptions (noms différents entre les deux datasets)
        country_iso_map['USA'] = 'USA'
        country_iso_map['UK'] = 'GBR'

        # Appliquer le mapping pour créer la colonne de codes ISO
        performance_pays['iso_alpha'] = performance_pays['Pays'].map(country_iso_map)
    except:
        performance_pays['iso_alpha'] = performance_pays['Pays']
    
    # --- Affichage de la carte ---
    st.subheader("Répartition Mondiale du Chiffre d'Affaires")
    
    fig_map = px.scatter_geo(
        performance_pays,
        locations="iso_alpha",
        size="Chiffre d'Affaires",
        color="Chiffre d'Affaires",
        hover_name="Pays",
        hover_data={
            'iso_alpha': False,
            "Chiffre d'Affaires": ':,.0f €',
            'Numéro_Commande': True,
            'Nom_du_Client': True
        },
        projection="natural earth",
        title="Chiffre d'Affaires par Pays",
        color_continuous_scale="Viridis"
    )
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True, key="geo_map")

    st.markdown("""
    **Insights :**
    - Visualisation immédiate de la répartition géographique du chiffre d'affaires
    - Les bulles plus grandes et plus colorées indiquent les marchés les plus rentables
    - Permet d'identifier les zones géographiques sous-exploitées
    """)
    
    # Tableau récapitulatif - Performance par pays
    _render_country_summary(performance_pays)

def _render_country_summary(performance_pays):
    """Affiche le tableau récapitulatif des pays"""
    st.markdown("---")
    st.subheader("📊 CLASSEMENT MONDIAL DES PAYS")
    
    # Préparation des données pour le tableau
    tableau_pays = performance_pays[['Pays', "Chiffre d'Affaires", 'Numéro_Commande', 'Nom_du_Client', 'Quantité_Commandée']].copy()
    tableau_pays['CA_Moyen_Commande'] = (tableau_pays["Chiffre d'Affaires"] / tableau_pays['Numéro_Commande']).round(0)
    tableau_pays['Part_CA_Mondial'] = (tableau_pays["Chiffre d'Affaires"] / tableau_pays["Chiffre d'Affaires"].sum() * 100).round(1)
    tableau_pays['Rang_Mondial'] = range(1, len(tableau_pays) + 1)
    
    # Formatage pour l'affichage
    display_pays = tableau_pays.copy()
    display_pays["Chiffre d'Affaires"] = display_pays["Chiffre d'Affaires"].apply(lambda x: f"{x:,.0f} €")
    display_pays['CA_Moyen_Commande'] = display_pays['CA_Moyen_Commande'].apply(lambda x: f"{x:,.0f} €")
    display_pays['Part_CA_Mondial'] = display_pays['Part_CA_Mondial'].apply(lambda x: f"{x}%")
    
    # Affichage du tableau
    st.dataframe(display_pays, use_container_width=True, hide_index=True)
    
    # Indicateurs clés mondiaux
    _render_global_indicators(tableau_pays)

def _render_global_indicators(tableau_pays):
    """Affiche les indicateurs clés mondiaux"""
    st.markdown("**🌍 INDICATEURS CLÉS MONDAUX**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        concentration_top5 = tableau_pays.head(5)['Part_CA_Mondial'].sum()
        st.metric("Concentration Top 5", f"{concentration_top5:.1f}%")
    
    with col2:
        pays_actifs = len(tableau_pays)
        st.metric("Pays Actifs", f"{pays_actifs}")
    
    with col3:
        ca_moyen_par_pays = tableau_pays["Chiffre d'Affaires"].mean()
        st.metric("CA Moyen/Pays", f"{ca_moyen_par_pays:,.0f} €")
    
    with col4:
        diversite_geographique = (1 - (tableau_pays.head(3)["Chiffre d'Affaires"].sum() / tableau_pays["Chiffre d'Affaires"].sum())) * 100
        st.metric("Diversité Géographique", f"{diversite_geographique:.1f}%")

def _render_country_analysis(df_filtered):
    """Affiche l'analyse détaillée par pays"""
    # --- Analyse détaillée par pays ---
    st.subheader("Analyse Détaillée par Pays")
    
    performance_pays = df_filtered.groupby('Pays').agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique',
        'Quantité_Commandée': 'sum'
    }).sort_values("Chiffre d'Affaires", ascending=False).reset_index()
    
    col1, col2 = st.columns([3, 2])

    with col1:
        st.write("**Top 20 Pays par Chiffre d'Affaires**")
        fig_bar_pays = px.bar(
            performance_pays.head(20), 
            x='Pays', 
            y="Chiffre d'Affaires",
            color="Chiffre d'Affaires",
            color_continuous_scale="Viridis"
        )
        fig_bar_pays.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_bar_pays, use_container_width=True, key="geo_bar2")

    with col2:
        st.write("**Répartition du CA (Top 10)**")
        fig_pie_pays = px.pie(
            performance_pays.head(10), 
            names='Pays', 
            values="Chiffre d'Affaires",
            hole=0.3
        )
        st.plotly_chart(fig_pie_pays, use_container_width=True, key="geo_pie2")
    
    # Métriques clés
    _render_country_kpis(performance_pays)
    
    # Tableau détaillé top pays
    _render_detailed_country_table(performance_pays)

def _render_country_kpis(performance_pays):
    """Affiche les métriques clés par pays"""
    st.subheader("Métriques Clés par Pays")
    
    top_pays = performance_pays.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Pays Leader",
            value=top_pays['Pays'],
            delta=f"{top_pays['Chiffre d\'Affaires']:,.0f} €"
        )
    
    with col2:
        concentration = (performance_pays.head(3)["Chiffre d'Affaires"].sum() / 
                        performance_pays["Chiffre d'Affaires"].sum() * 100)
        st.metric(
            label="Concentration Top 3",
            value=f"{concentration:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Nombre de Pays Actifs",
            value=len(performance_pays)
        )
    
    with col4:
        avg_per_country = performance_pays["Chiffre d'Affaires"].mean()
        st.metric(
            label="CA Moyen par Pays",
            value=f"{avg_per_country:,.0f} €"
        )

def _render_detailed_country_table(performance_pays):
    """Affiche le tableau détaillé des top pays"""
    st.markdown("---")
    st.subheader("📈 ANALYSE DÉTAILLÉE DES TOP PAYS")
    
    # Analyse détaillée des top pays
    top_20_pays = performance_pays.head(20).copy()
    
    # Calculs supplémentaires
    top_20_pays['CA_Par_Client'] = (top_20_pays["Chiffre d'Affaires"] / top_20_pays['Nom_du_Client']).round(0)
    top_20_pays['Commandes_Par_Client'] = (top_20_pays['Numéro_Commande'] / top_20_pays['Nom_du_Client']).round(1)
    top_20_pays['Quantité_Par_Commande'] = (top_20_pays['Quantité_Commandée'] / top_20_pays['Numéro_Commande']).round(1)
    
    # Préparation affichage
    display_top_pays = top_20_pays[['Pays', "Chiffre d'Affaires", 'Nom_du_Client', 'Numéro_Commande', 
                                  'CA_Par_Client', 'Commandes_Par_Client', 'Quantité_Par_Commande']].copy()
    
    display_top_pays["Chiffre d'Affaires"] = display_top_pays["Chiffre d'Affaires"].apply(lambda x: f"{x:,.0f} €")
    display_top_pays['CA_Par_Client'] = display_top_pays['CA_Par_Client'].apply(lambda x: f"{x:,.0f} €")
    
    st.dataframe(display_top_pays, use_container_width=True, hide_index=True)
    
    # Analyse de performance par type de marché
    _render_market_type_analysis(top_20_pays)

def _render_market_type_analysis(top_20_pays):
    """Affiche l'analyse par type de marché"""
    st.markdown("**🎯 PERFORMANCE PAR TYPE DE MARCHÉ**")
    
    # Catégorisation des pays
    top_20_pays['Type_Marché'] = pd.cut(top_20_pays["Chiffre d'Affaires"], 
                                      bins=[0, 100000, 500000, float('inf')],
                                      labels=['Marché Émergent', 'Marché Moyen', 'Marché Mature'])
    
    analyse_marche = top_20_pays.groupby('Type_Marché').agg({
        'Pays': 'count',
        "Chiffre d'Affaires": 'sum',
        'Nom_du_Client': 'sum'
    })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marche_mature = analyse_marche.loc['Marché Mature'] if 'Marché Mature' in analyse_marche.index else {'Pays': 0, "Chiffre d'Affaires": 0}
        st.metric("Marchés Matures", f"{marche_mature['Pays']} pays", 
                 delta=f"{marche_mature['Chiffre d\'Affaires']:,.0f} €")
    
    with col2:
        marche_moyen = analyse_marche.loc['Marché Moyen'] if 'Marché Moyen' in analyse_marche.index else {'Pays': 0, "Chiffre d'Affaires": 0}
        st.metric("Marchés Moyens", f"{marche_moyen['Pays']} pays",
                 delta=f"{marche_moyen['Chiffre d\'Affaires']:,.0f} €")
    
    with col3:
        marche_emergent = analyse_marche.loc['Marché Émergent'] if 'Marché Émergent' in analyse_marche.index else {'Pays': 0, "Chiffre d'Affaires": 0}
        st.metric("Marchés Émergents", f"{marche_emergent['Pays']} pays",
                 delta=f"{marche_emergent['Chiffre d\'Affaires']:,.0f} €")

def _render_city_analysis(df_filtered):
    """Affiche l'analyse par ville"""
    st.subheader("Analyse par Ville")
    
    # Agréger les données par ville
    performance_ville = df_filtered.groupby(['Ville', 'Pays']).agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique'
    }).sort_values("Chiffre d'Affaires", ascending=False).reset_index()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Top 15 Villes par Chiffre d'Affaires**")
        fig_bar_ville = px.bar(
            performance_ville.head(15),
            x='Ville',
            y="Chiffre d'Affaires",
            color='Pays',
            hover_data=['Nom_du_Client']
        )
        fig_bar_ville.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar_ville, use_container_width=True, key="geo_bar_ville")
    
    with col2:
        st.write("**Villes par Pays**")
        villes_par_pays = performance_ville.groupby('Pays')['Ville'].count().sort_values(ascending=False)
        fig_pie_villes = px.pie(
            values=villes_par_pays.values,
            names=villes_par_pays.index,
            title="Répartition des Villes"
        )
        st.plotly_chart(fig_pie_villes, use_container_width=True, key="geo_pie_villes")
    
    # Tableau détaillé par ville
    _render_detailed_city_table(performance_ville)
    
    # Statistiques villes
    _render_city_statistics(performance_ville)
    
    # Villes stratégiques
    _render_strategic_cities(performance_ville)

def _render_detailed_city_table(performance_ville):
    """Affiche le tableau détaillé par ville"""
    st.markdown("---")
    st.subheader("🏙️ PERFORMANCE DÉTAILLÉE PAR VILLE")
    
    # Enrichissement des données villes
    performance_ville['CA_Par_Client'] = (performance_ville["Chiffre d'Affaires"] / performance_ville['Nom_du_Client']).round(0)
    performance_ville['Commandes_Par_Client'] = (performance_ville['Numéro_Commande'] / performance_ville['Nom_du_Client']).round(1)
    performance_ville['Part_CA_Pays'] = performance_ville.groupby('Pays')["Chiffre d'Affaires"].transform(
        lambda x: (x / x.sum() * 100).round(1)
    )
    
    # Classement
    performance_ville['Rang_National'] = performance_ville.groupby('Pays')["Chiffre d'Affaires"].rank(ascending=False, method='dense')
    performance_ville['Rang_Mondial'] = performance_ville["Chiffre d'Affaires"].rank(ascending=False, method='dense')
    
    # Top 30 villes pour le tableau
    top_villes = performance_ville.head(30).copy()
    
    # Formatage affichage
    display_villes = top_villes[[
        'Ville', 'Pays', 'Rang_Mondial', 'Rang_National', "Chiffre d'Affaires", 
        'Numéro_Commande', 'Nom_du_Client', 'CA_Par_Client', 'Part_CA_Pays'
    ]].copy()
    
    display_villes["Chiffre d'Affaires"] = display_villes["Chiffre d'Affaires"].apply(lambda x: f"{x:,.0f} €")
    display_villes['CA_Par_Client'] = display_villes['CA_Par_Client'].apply(lambda x: f"{x:,.0f} €")
    display_villes['Part_CA_Pays'] = display_villes['Part_CA_Pays'].apply(lambda x: f"{x}%")
    display_villes['Rang_National'] = display_villes['Rang_National'].apply(lambda x: f"#{int(x)}")
    display_villes['Rang_Mondial'] = display_villes['Rang_Mondial'].apply(lambda x: f"#{int(x)}")
    
    st.dataframe(display_villes, use_container_width=True, hide_index=True)

def _render_city_statistics(performance_ville):
    """Affiche les statistiques des villes"""
    st.markdown("**📈 STATISTIQUES URBAINES**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        villes_actives = len(performance_ville)
        st.metric("Villes Actives", f"{villes_actives}")
    
    with col2:
        pays_avec_villes = performance_ville['Pays'].nunique()
        st.metric("Pays Représentés", f"{pays_avec_villes}")
    
    with col3:
        concentration_top10_villes = performance_ville.head(10)["Chiffre d'Affaires"].sum() / performance_ville["Chiffre d'Affaires"].sum() * 100
        st.metric("Concentration Top 10", f"{concentration_top10_villes:.1f}%")
    
    with col4:
        ca_moyen_par_ville = performance_ville["Chiffre d'Affaires"].mean()
        st.metric("CA Moyen/Ville", f"{ca_moyen_par_ville:,.0f} €")

def _render_strategic_cities(performance_ville):
    """Affiche les villes stratégiques par pays"""
    st.markdown("**🏆 VILLES STRATÉGIQUES PAR PAYS**")
    
    villes_strategiques = performance_ville.loc[performance_ville.groupby('Pays')["Chiffre d'Affaires"].idxmax()]
    top_villes_strategiques = villes_strategiques.nlargest(5, "Chiffre d'Affaires")[['Ville', 'Pays', "Chiffre d'Affaires", 'Part_CA_Pays']]
    
    for i, (idx, ville) in enumerate(top_villes_strategiques.iterrows(), 1):
        col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
        with col_v1:
            st.write(f"**#{i}**")
        with col_v2:
            st.write(f"**{ville['Ville']}** ({ville['Pays']})")
        with col_v3:
            st.write(f"{ville['Chiffre d\'Affaires']:,.0f} € ({ville['Part_CA_Pays']}% du pays)")