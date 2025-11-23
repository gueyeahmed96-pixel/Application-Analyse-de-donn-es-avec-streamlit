import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_pyramid_chart(ca_par_client, segments):
    """Crée un graphique pyramide pour la segmentation client"""
    fig_pyramide = go.Figure()
    
    segments_ordered = segments.loc[['VIP', 'Moyen', 'Base']]
    
    fig_pyramide.add_trace(go.Bar(
        y=['CLIENTS VIP', 'CLIENTÈLE MOYENNE', 'BASE CLIENTS'],
        x=segments_ordered['Part_CA'],
        orientation='h',
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
        text=segments_ordered['Part_CA'].apply(lambda x: f'{x}%'),
        textposition='auto',
    ))
    
    fig_pyramide.update_layout(
        title="Répartition du CA par Segment Client",
        xaxis_title="Part du Chiffre d'Affaires (%)",
        height=400,
        showlegend=False
    )
    return fig_pyramide

def create_strategic_matrix(df_filtered, top_pays_count=4, top_gammes_count=4):
    """Crée la matrice stratégique produits/marchés"""
    # Top pays et top gammes pour la matrice
    top_pays = df_filtered.groupby('Pays')["Chiffre d'Affaires"].sum().nlargest(top_pays_count).index
    top_gammes = df_filtered.groupby('Gamme_de_Produits')["Chiffre d'Affaires"].sum().nlargest(top_gammes_count).index
    
    # Création de la matrice
    matrice_data = []
    for gamme in top_gammes:
        row = []
        for pays in top_pays:
            ca_cellule = df_filtered[
                (df_filtered['Gamme_de_Produits'] == gamme) & 
                (df_filtered['Pays'] == pays)
            ]["Chiffre d'Affaires"].sum()
            row.append(ca_cellule)
        matrice_data.append(row)
    
    # Création de la heatmap
    fig_matrice = px.imshow(
        matrice_data,
        x=top_pays,
        y=top_gammes,
        aspect="auto",
        color_continuous_scale='Viridis',
        title="Performance CA par Produit/Marché (€)",
        labels=dict(x="Marché", y="Gamme Produit", color="CA (€)")
    )
    
    # Ajouter les valeurs dans les cellules
    for i in range(len(top_gammes)):
        for j in range(len(top_pays)):
            valeur = matrice_data[i][j]
            if valeur > 0:
                fig_matrice.add_annotation(
                    x=j, y=i,
                    text=f"{valeur:,.0f}€",
                    showarrow=False,
                    font=dict(color="white" if valeur > np.array(matrice_data).max()/2 else "black")
                )
    
    return fig_matrice

def create_radar_chart(scores):
    """Crée un graphique radar pour les scores de performance"""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Fermer le cercle
        theta=categories + [categories[0]],
        fill='toself',
        name='Performance',
        line=dict(color='#4ECDC4'),
        fillcolor='rgba(78, 205, 196, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Profil de Performance par Domaine Stratégique",
        height=400
    )
    
    return fig_radar

def create_temporal_evolution(df_filtered, period_type='trimestre'):
    """Crée un graphique d'évolution temporelle"""
    if period_type == 'trimestre':
        evolution_data = df_filtered.groupby(['Année', 'Trimestre_ID']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
        evolution_data['Période'] = 'T' + evolution_data['Trimestre_ID'].astype(str) + ' ' + evolution_data['Année'].astype(str)
        x_col = 'Période'
    else:  # mensuel
        evolution_data = df_filtered.groupby(['Année', 'Mois']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
        noms_mois = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin', 
                     7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
        evolution_data['Nom_Mois'] = evolution_data['Mois'].map(noms_mois)
        evolution_data['Période'] = evolution_data['Nom_Mois'] + ' ' + evolution_data['Année'].astype(str)
        x_col = 'Période'
    
    fig = px.line(evolution_data, x=x_col, y="Chiffre d'Affaires", 
                  labels={'Chiffre d\'Affaires': 'CA (€)'}, 
                  markers=True,
                  title=f"Évolution du Chiffre d'Affaires par {period_type.title()}")
    
    if period_type == 'trimestre':
        fig.update_layout(xaxis_tickangle=-45)
    
    return fig

def create_geo_map(df_filtered):
    """Crée la carte géographique mondiale"""
    performance_pays = df_filtered.groupby('Pays').agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique',
        'Quantité_Commandée': 'sum'
    }).sort_values("Chiffre d'Affaires", ascending=False).reset_index()

    # Gestion des codes ISO des pays
    try:
        gapminder = px.data.gapminder().query("year==2007")
        country_iso_map = gapminder.set_index('country')['iso_alpha'].to_dict()
        country_iso_map['USA'] = 'USA'
        country_iso_map['UK'] = 'GBR'
        performance_pays['iso_alpha'] = performance_pays['Pays'].map(country_iso_map)
    except:
        performance_pays['iso_alpha'] = performance_pays['Pays']
    
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
    return fig_map

def create_product_comparison(df_filtered, metric='quantité'):
    """Crée une comparaison des produits par quantité ou CA"""
    if metric == 'quantité':
        produits_data = df_filtered.groupby('Code_Produit').agg({
            'Quantité_Commandée':'sum',
            'Gamme_de_Produits':'first',
            'Prix Conseil':'first'
        }).nlargest(10, 'Quantité_Commandée')
        title_suffix = 'Quantité Vendue'
        color = 'lightblue'
    else:  # CA
        produits_data = df_filtered.groupby('Code_Produit').agg({
            'Chiffre d\'Affaires': 'sum',
            'Gamme_de_Produits': 'first',
            'Prix Conseil': 'first'
        }).nlargest(10, 'Chiffre d\'Affaires')
        title_suffix = 'Chiffre d\'Affaires'
        color = 'lightgreen'
    
    fig = px.bar(
        produits_data.reset_index(),
        x=produits_data.iloc[:, 0],  # Première colonne (quantité ou CA)
        y='Code_Produit',
        orientation='h',
        title=f'Top 10 Produits - {title_suffix}',
        color_discrete_sequence=[color]
    )
    
    return fig

def create_price_variability_chart(df_filtered, top_n=15):
    """Crée un graphique de variabilité des prix"""
    prix_par_produit = df_filtered.groupby(['Code_Produit', 'Gamme_de_Produits']).agg({
        'Prix_Unitaire': ['mean', 'std', 'min', 'max', 'count'],
        'Prix Conseil': 'first'
    }).round(2)
    
    prix_par_produit.columns = ['Prix_Moyen', 'Ecart_Type', 'Prix_Min', 'Prix_Max', 'Nb_Ventes', 'Prix_Conseil']
    
    fig = px.bar(
        prix_par_produit.nlargest(top_n, 'Ecart_Type').reset_index(),
        x='Code_Produit',
        y='Ecart_Type',
        title=f'Produits avec la Plus Grande Variabilité de Prix (Top {top_n})',
        labels={'Ecart_Type': 'Écart-Type des Prix (€)', 'Code_Produit': 'Produit'},
        color='Ecart_Type'
    )
    return fig

def create_behavior_charts(df_filtered, chart_type='ca'):
    """Crée les graphiques de comportement d'achat"""
    taille_transactions = df_filtered.groupby('Taille de Transaction').agg({
        'Chiffre d\'Affaires': 'sum', 
        'Numéro_Commande': 'nunique'
    }).reset_index()
    
    if chart_type == 'ca':
        fig = px.bar(
            taille_transactions,
            x='Taille de Transaction',
            y='Chiffre d\'Affaires',
            color='Taille de Transaction',
            color_discrete_map={
                'Small': '#1f77b4', 
                'Medium': '#2ca02c', 
                'Large': '#d62728'
            },
            text=[f'{x:,.0f} €' for x in taille_transactions['Chiffre d\'Affaires']],
            labels={'Chiffre d\'Affaires': 'CA (€)', 'Taille de Transaction': ''}
        )
        fig.update_layout(
            showlegend=False,
            yaxis_title="Chiffre d'Affaires (€)",
            height=400
        )
        fig.update_traces(textposition='outside')
    
    elif chart_type == 'commandes':
        fig = px.bar(
            taille_transactions,
            x='Taille de Transaction',
            y='Numéro_Commande',
            color='Taille de Transaction',
            color_discrete_map={
                'Small': '#1f77b4', 
                'Medium': '#2ca02c', 
                'Large': '#d62728'
            },
            text=taille_transactions['Numéro_Commande'],
            labels={'Numéro_Commande': 'Nombre de Commandes', 'Taille de Transaction': ''}
        )
        fig.update_layout(
            showlegend=False,
            yaxis_title="Nombre de Commandes",
            height=400
        )
        fig.update_traces(textposition='outside')
    
    else:  # pie chart
        fig = px.pie(
            taille_transactions,
            names='Taille de Transaction',
            values='Chiffre d\'Affaires',
            color='Taille de Transaction',
            color_discrete_map={
                'Small': '#1f77b4', 
                'Medium': '#2ca02c', 
                'Large': '#d62728'
            },
            hole=0.3
        )
        fig.update_layout(height=400)
    
    return fig