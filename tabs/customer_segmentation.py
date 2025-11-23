import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_customer_segmentation_tab(df_filtered, df_original):
    """Affiche l'onglet Segmentation Clientèle"""
    
    st.header("🎯 SEGMENTATION CLIENTÈLE")
    
    # Top 10 Clients par Chiffre d'Affaires
    st.subheader("Top 10 Clients par Chiffre d'Affaires")
    
    # Calcul des indicateurs clients
    top_clients = df_filtered.groupby('Nom_du_Client').agg({
        "Chiffre d'Affaires": 'sum', 
        'Numéro_Commande': 'nunique', 
        'Pays': 'first'
    }).nlargest(10, "Chiffre d'Affaires").reset_index()
    
    # Calcul du CA moyen par commande
    top_clients['CA_moyen_commande'] = top_clients["Chiffre d'Affaires"] / top_clients['Numéro_Commande']
    
    # Graphique barres - Top clients
    fig_clients_top = px.bar(
        top_clients, 
        x='Nom_du_Client', 
        y="Chiffre d'Affaires", 
        color="Chiffre d'Affaires", 
        hover_data=['Pays', 'Numéro_Commande', 'CA_moyen_commande'], 
        labels={'Nom_du_Client': 'Client'},
        title="Top 10 Clients par Chiffre d'Affaires Total",
        color_continuous_scale='Viridis'
    )
    fig_clients_top.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_clients_top, use_container_width=True)
    
    # Graphique camembert - Répartition par pays
    fig_clients_pie = px.pie(
        top_clients,
        names='Pays',
        values='Chiffre d\'Affaires',
        title='Répartition du CA des Top 10 Clients par Pays',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_clients_pie, use_container_width=True)
    
    # Affichage du tableau détaillé
    st.subheader("Détail des Top 10 Clients")
    top_clients_display = top_clients.copy()
    top_clients_display["Chiffre d'Affaires"] = top_clients_display["Chiffre d'Affaires"].round(2)
    top_clients_display['CA_moyen_commande'] = top_clients_display['CA_moyen_commande'].round(2)
    st.dataframe(top_clients_display)
    
    # Clients fidèles des produits de haute valeur
    _render_premium_loyal_customers(df_filtered)
    
    # Performance par pays
    _render_country_performance(df_filtered)

def _render_premium_loyal_customers(df_filtered):
    """Affiche les clients fidèles premium"""
    st.subheader("🔍 Clients Fidèles des Produits de Haute Valeur")
    
    # Filtrage des transactions de haute valeur
    clients_haute_valeur = df_filtered[df_filtered['Taille de Transaction'].isin(['Large', 'Medium'])]
    
    # Agrégation des données clients premium
    clients_fideles_premium = clients_haute_valeur.groupby('Nom_du_Client').agg({
        'Numéro_Commande': 'nunique',
        'Chiffre d\'Affaires': 'sum',
        'Quantité_Commandée': 'sum',
        'Pays': 'first',
        'Taille de Transaction': lambda x: x.value_counts().to_dict()
    }).round(2)
    
    # Renommage des colonnes
    clients_fideles_premium.columns = ['Nb_Commandes', 'CA_Total', 'Quantité_Totale', 'Pays', 'Repartition_Tailles']
    
    # Filtrage des clients fidèles (au moins 2 commandes premium)
    clients_fideles_actifs = clients_fideles_premium[clients_fideles_premium['Nb_Commandes'] >= 2]\
                             .sort_values('CA_Total', ascending=False)
    
    # Graphique scatter - Analyse des clients fidèles premium
    if not clients_fideles_actifs.empty:
        fig_clients_fideles = px.scatter(
            clients_fideles_actifs.reset_index(),
            x='Nb_Commandes',
            y='CA_Total',
            size='Quantité_Totale',
            color='Pays',
            title='Clients Fidèles Premium : Nombre de Commandes vs CA Total',
            labels={
                'Nb_Commandes': 'Nombre de Commandes Premium', 
                'CA_Total': 'CA Total (€)',
                'Quantité_Totale': 'Quantité Totale Commandée'
            },
            hover_name='Nom_du_Client',
            hover_data=['Pays', 'Quantité_Totale'],
            log_y=True,  # Échelle logarithmique pour mieux visualiser les écarts
            size_max=60
        )
        
        fig_clients_fideles.update_layout(
            showlegend=True,
            xaxis_title="Nombre de Commandes Premium",
            yaxis_title="Chiffre d'Affaires Total (€ - échelle log)",
            legend_title="Pays"
        )
        
        st.plotly_chart(fig_clients_fideles, use_container_width=True)
        
        # Affichage du tableau des clients fidèles
        st.subheader("Liste des Clients Fidèles Premium")
        clients_fideles_display = clients_fideles_actifs.reset_index()
        clients_fideles_display['CA_Total'] = clients_fideles_display['CA_Total'].round(2)
        st.dataframe(clients_fideles_display[['Nom_du_Client', 'Pays', 'Nb_Commandes', 'CA_Total', 'Quantité_Totale']])
        
    else:
        st.info("Aucun client fidèle premium trouvé avec au moins 2 commandes de taille Medium ou Large.")

def _render_country_performance(df_filtered):
    """Affiche la performance clients par pays"""
    st.subheader("🌍 Performance Clients par Pays")
    
    ca_par_pays = df_filtered.groupby('Pays').agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique'
    }).round(2).sort_values("Chiffre d'Affaires", ascending=False)
    
    ca_par_pays.columns = ['CA_Total', 'Nb_Commandes', 'Nb_Clients_Uniques']
    ca_par_pays['CA_moyen_par_client'] = (ca_par_pays['CA_Total'] / ca_par_pays['Nb_Clients_Uniques']).round(2)
    
    st.dataframe(ca_par_pays.head(10))
    
    # Graphique de performance par pays
    fig_pays_perf = px.bar(
        ca_par_pays.head(10).reset_index(),
        x='Pays',
        y='CA_Total',
        title='Top 10 Pays par Chiffre d\'Affaires',
        color='CA_Total',
        color_continuous_scale='thermal'
    )
    st.plotly_chart(fig_pays_perf, use_container_width=True)