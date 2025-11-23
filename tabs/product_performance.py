import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_product_performance_tab(df_filtered, df_original):
    """Affiche l'onglet Performance Produits"""
    
    st.subheader("Performance par Gamme de Produits")
    rentabilite_gammes = df_filtered.groupby('Gamme_de_Produits').agg({"Chiffre d'Affaires": 'sum'}).reset_index().sort_values("Chiffre d'Affaires", ascending=False)
    
    fig = px.bar(
        rentabilite_gammes, 
        x='Gamme_de_Produits', 
        y="Chiffre d'Affaires", 
        color="Chiffre d'Affaires",
        title="Chiffre d'Affaires par Gamme de Produits",
        labels={"Chiffre d'Affaires": "CA (€)", "Gamme_de_Produits": "Gamme de Produits"}
    )
    st.plotly_chart(fig, use_container_width=True, key="produit_gammes")
    
    # Produits les plus vendus en quantité
    st.subheader("Produits Quantité et Chiffre d'affaire")
    _render_product_quantity_vs_revenue(df_filtered)
    
    # Prix moyen des produits et variance des prix
    st.subheader("Prix moyen des produits et variance des prix")
    _render_price_analysis(df_filtered)
    
    # Tendance des gammes de produits par trimestre
    st.subheader("Tendance des gammes de produits par trimestre")
    _render_product_trends(df_filtered)
    
    # Croissance par gamme de produits
    st.subheader("Croissance par gamme de produits")
    _render_product_growth(df_filtered)
    
    # Tableau récapitulatif des performances par gamme
    _render_product_summary(df_filtered)

def _render_product_quantity_vs_revenue(df_filtered):
    """Affiche les produits par quantité et chiffre d'affaires"""
    produits_quantite = df_filtered.groupby('Code_Produit').agg({
        'Quantité_Commandée':'sum',
        'Gamme_de_Produits':'first',
        'Prix Conseil':'first'
    }).nlargest(10, 'Quantité_Commandée')
    
    # Produits générant le plus de CA
    produits_ca = df_filtered.groupby('Code_Produit').agg({
        'Chiffre d\'Affaires': 'sum',
        'Gamme_de_Produits': 'first',
        'Prix Conseil': 'first'
    }).nlargest(10, 'Chiffre d\'Affaires')
    
    # Visualisation
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Top 10 Produits - Quantité Vendue', 'Top 10 Produits - Chiffre d\'Affaires'),
        horizontal_spacing=0.1
    )
    
    # Graphique quantité
    fig.add_trace(
        go.Bar(
            x=produits_quantite['Quantité_Commandée'],
            y=produits_quantite.index,
            orientation='h',
            name='Quantité',
            marker_color='lightblue'
        ),
        row=1, col=1
    )
    
    # Graphique CA
    fig.add_trace(
        go.Bar(
            x=produits_ca['Chiffre d\'Affaires'],
            y=produits_ca.index,
            orientation='h',
            name='CA',
            marker_color='lightgreen'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Performance des Produits - Top 10",
        height=500,
        showlegend=False
    )
    fig.update_xaxes(title_text="Quantité Vendue", row=1, col=1)
    fig.update_xaxes(title_text="Chiffre d'Affaires (€)", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True, key="produit_top10")

def _render_price_analysis(df_filtered):
    """Affiche l'analyse des prix"""
    prix_par_produit = df_filtered.groupby(['Code_Produit', 'Gamme_de_Produits']).agg({
        'Prix_Unitaire': ['mean', 'std', 'min', 'max', 'count'],
        'Prix Conseil': 'first'
    }).round(2)
    
    # Aplatir les colonnes multi-niveaux
    prix_par_produit.columns = ['Prix_Moyen', 'Ecart_Type', 'Prix_Min', 'Prix_Max', 'Nb_Ventes', 'Prix_Conseil']
    
    # Trier par prix moyen décroissant
    prix_par_produit = prix_par_produit.sort_values('Prix_Moyen', ascending=False)
    
    # Graphique des écarts-types (variabilité des prix)
    fig2 = px.bar(
        prix_par_produit.nlargest(15, 'Ecart_Type').reset_index(),
        x='Code_Produit',
        y='Ecart_Type',
        title='Produits avec la Plus Grande Variabilité de Prix (Top 15)',
        labels={'Ecart_Type': 'Écart-Type des Prix (€)', 'Code_Produit': 'Produit'},
        color='Ecart_Type'
    )
    st.plotly_chart(fig2, use_container_width=True, key="produit_variabilite_prix")

def _render_product_trends(df_filtered):
    """Affiche les tendances des produits par trimestre"""
    tendance_gammes = df_filtered.groupby(['Année', 'Trimestre_ID', 'Gamme_de_Produits']).agg({
        'Chiffre d\'Affaires': 'sum',
        'Numéro_Commande': 'nunique',
        'Quantité_Commandée': 'sum'
    }).reset_index()
    
    # Créer une période pour l'affichage
    tendance_gammes['Période'] = 'T' + tendance_gammes['Trimestre_ID'].astype(str) + ' ' + tendance_gammes['Année'].astype(str)
    
    # Visualisation évolution temporelle
    fig = px.line(
        tendance_gammes,
        x='Période',
        y='Chiffre d\'Affaires',
        color='Gamme_de_Produits',
        title='Évolution du CA par Gamme de Produits',
        labels={'Chiffre d\'Affaires': 'CA (€)', 'Période': 'Trimestre'},
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True, key="produit_tendance_trimestre")

def _render_product_growth(df_filtered):
    """Affiche la croissance par gamme de produits"""
    tendance_gammes = df_filtered.groupby(['Année', 'Trimestre_ID', 'Gamme_de_Produits']).agg({
        'Chiffre d\'Affaires': 'sum',
        'Numéro_Commande': 'nunique',
        'Quantité_Commandée': 'sum'
    }).reset_index()
    
    tendance_gammes['Période'] = 'T' + tendance_gammes['Trimestre_ID'].astype(str) + ' ' + tendance_gammes['Année'].astype(str)
    
    # Graphique en barres empilées
    fig = px.bar(
        tendance_gammes,
        x='Période',
        y='Chiffre d\'Affaires',
        color='Gamme_de_Produits',
        title='Répartition du CA par Gamme et par Trimestre',
        labels={'Chiffre d\'Affaires': 'CA (€)', 'Période': 'Trimestre'},
        barmode='stack'
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True, key="produit_croissance_gamme")

def _render_product_summary(df_filtered):
    """Affiche le tableau récapitulatif des performances par gamme"""
    st.subheader("📋 TABLEAU RÉCAPITULATIF DES PERFORMANCES PAR GAMME")
    
    # Calcul des indicateurs par gamme
    performance_gammes = df_filtered.groupby('Gamme_de_Produits').agg({
        "Chiffre d'Affaires": ['sum', 'count'],
        'Quantité_Commandée': 'sum',
        'Numéro_Commande': 'nunique',
        'Prix_Unitaire': 'mean'
    }).round(2)
    
    # Aplatir les colonnes multi-niveaux
    performance_gammes.columns = ['CA_Total', 'Nb_Lignes', 'Quantité_Totale', 'Nb_Commandes', 'Prix_Moyen']
    
    # Calcul des indicateurs supplémentaires
    performance_gammes['CA_Moyen_Commande'] = (performance_gammes['CA_Total'] / performance_gammes['Nb_Commandes']).round(2)
    performance_gammes['Part_CA'] = (performance_gammes['CA_Total'] / performance_gammes['CA_Total'].sum() * 100).round(1)
    performance_gammes['Quantité_Moyenne_Ligne'] = (performance_gammes['Quantité_Totale'] / performance_gammes['Nb_Lignes']).round(1)
    
    # Trier par CA total décroissant
    performance_gammes = performance_gammes.sort_values('CA_Total', ascending=False)
    
    # Préparer l'affichage avec formatage
    display_gammes = performance_gammes.copy()
    display_gammes['CA_Total'] = display_gammes['CA_Total'].apply(lambda x: f"{x:,.0f} €")
    display_gammes['Prix_Moyen'] = display_gammes['Prix_Moyen'].apply(lambda x: f"{x:,.2f} €")
    display_gammes['CA_Moyen_Commande'] = display_gammes['CA_Moyen_Commande'].apply(lambda x: f"{x:,.0f} €")
    display_gammes['Part_CA'] = display_gammes['Part_CA'].apply(lambda x: f"{x} %")
    display_gammes['Nb_Lignes'] = display_gammes['Nb_Lignes'].apply(lambda x: f"{x:,}")
    display_gammes['Quantité_Totale'] = display_gammes['Quantité_Totale'].apply(lambda x: f"{x:,}")
    display_gammes['Nb_Commandes'] = display_gammes['Nb_Commandes'].apply(lambda x: f"{x:,}")
    
    # Afficher le tableau
    st.dataframe(
        display_gammes,
        use_container_width=True,
        column_config={
            "Gamme_de_Produits": "Gamme de Produits",
            "CA_Total": "CA Total",
            "Part_CA": "Part du CA",
            "Nb_Lignes": "Nb Lignes",
            "Quantité_Totale": "Quantité Totale",
            "Nb_Commandes": "Nb Commandes",
            "Prix_Moyen": "Prix Moyen",
            "CA_Moyen_Commande": "CA Moyen/Commande",
            "Quantité_Moyenne_Ligne": "Qté Moy/Ligne"
        }
    )
    
    # Métriques clés résumées
    _render_product_kpis(performance_gammes)

def _render_product_kpis(performance_gammes):
    """Affiche les indicateurs clés des gammes"""
    st.subheader("🎯 INDICATEURS CLÉS DES GAMMES")
    
    top_gamme = performance_gammes.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🏆 Gamme Leader",
            top_gamme.name,
            delta=f"{top_gamme['Part_CA']}% du CA"
        )
    
    with col2:
        concentration_top3 = performance_gammes.head(3)['Part_CA'].sum()
        st.metric(
            "📊 Concentration Top 3",
            f"{concentration_top3:.1f}%"
        )
    
    with col3:
        ca_moyen_gamme = performance_gammes['CA_Total'].mean()
        st.metric(
            "💰 CA Moyen par Gamme",
            f"{ca_moyen_gamme:,.0f} €"
        )
    
    with col4:
        nb_gammes_actives = len(performance_gammes)
        st.metric(
            "🏷️ Gammes Actives",
            f"{nb_gammes_actives}"
        )
    
    # Analyse des performances
    _render_product_performance_analysis(performance_gammes, top_gamme, concentration_top3, nb_gammes_actives)

def _render_product_performance_analysis(performance_gammes, top_gamme, concentration_top3, nb_gammes_actives):
    """Affiche l'analyse des performances par gamme"""
    with st.expander("📈 ANALYSE DES PERFORMANCES PAR GAMME"):
        st.markdown(f"""
        **📊 PERFORMANCE GÉNÉRALE :**
        - **Gamme dominante** : {top_gamme.name} ({top_gamme['Part_CA']}% du CA)
        - **Concentration** : Les 3 premières gammes représentent {concentration_top3:.1f}% du CA
        - **Diversité** : {nb_gammes_actives} gammes actives sur la période
        
        **💡 INSIGHTS :**
        - Les gammes à **fort CA moyen par commande** sont plus rentables
        - Les gammes avec **quantité moyenne élevée** ont une meilleure pénétration
        - La **diversification** du portefeuille réduit les risques
        """)