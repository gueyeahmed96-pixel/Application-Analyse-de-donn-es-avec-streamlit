import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_behavior_analysis_tab(df_filtered, df_original):
    """Affiche l'onglet Comportements d'Achat & Indicateurs Opérationnels"""
    
    st.header("🛒 Comportements d'Achat & Indicateurs Opérationnels")
    
    # SECTION 1: COMPORTEMENTS D'ACHAT
    st.subheader("📊 Comportements d'Achat")
    _render_purchase_behavior(df_filtered)
    
    st.markdown("---")
    
    # SECTION 2: INDICATEURS OPÉRATIONNELS
    st.subheader("⚡ Indicateurs Opérationnels")
    _render_operational_indicators(df_filtered)
    
    # SECTION 3: ANALYSE DES PROBLÈMES
    st.subheader("🔍 Analyse des Commandes Problématiques")
    _render_problem_analysis(df_filtered, df_original)

def _render_purchase_behavior(df_filtered):
    """Affiche les comportements d'achat"""
    taille_transactions = df_filtered.groupby('Taille de Transaction').agg({
        'Chiffre d\'Affaires': 'sum', 
        'Numéro_Commande': 'nunique'
    }).reset_index()
    
    # GRAPHIQUES SÉPARÉS POUR MEILLEURE LISIBILITÉ
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📈 Chiffre d'Affaires par Taille de Transaction**")
        fig_ca = px.bar(
            taille_transactions,
            x='Taille de Transaction',
            y='Chiffre d\'Affaires',
            color='Taille de Transaction',
            color_discrete_map={
                'Small': '#1f77b4', 
                'Medium': '#2ca02c', 
                'Large': '#d62728'
            },
            # text=[f'{x:,.0f} €' for x in taille_transactions['Chiffre d\'Affaires']],
            labels={'Chiffre d\'Affaires': 'CA (€)', 'Taille de Transaction': ''}
        )
        fig_ca.update_layout(
            showlegend=False,
            yaxis_title="Chiffre d'Affaires (€)",
            height=400
        )
        fig_ca.update_traces(textposition='outside')
        st.plotly_chart(fig_ca, use_container_width=True)
    
    with col2:
        st.markdown("**📦 Nombre de Commandes par Taille de Transaction**")
        fig_cmd = px.bar(
            taille_transactions,
            x='Taille de Transaction',
            y='Numéro_Commande',
            color='Taille de Transaction',
            color_discrete_map={
                'Small': '#1f77b4', 
                'Medium': '#2ca02c', 
                'Large': '#d62728'
            },
            # text=taille_transactions['Numéro_Commande'],
            labels={'Numéro_Commande': 'Nombre de Commandes', 'Taille de Transaction': ''}
        )
        fig_cmd.update_layout(
            showlegend=False,
            yaxis_title="Nombre de Commandes",
            height=400
        )
        fig_cmd.update_traces(textposition='outside')
        st.plotly_chart(fig_cmd, use_container_width=True)
    
    # Camembert pour la répartition
    st.markdown("**🥧 Répartition du CA par Taille de Transaction**")
    fig_pie = px.pie(
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
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Insights comportements
    _render_behavior_insights(taille_transactions)

def _render_behavior_insights(taille_transactions):
    """Affiche les insights des comportements d'achat"""
    ca_medium = taille_transactions[taille_transactions['Taille de Transaction'] == 'Medium']['Chiffre d\'Affaires'].sum()
    total_ca_comportement = taille_transactions['Chiffre d\'Affaires'].sum()
    pourcentage_medium = (ca_medium / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    
    # Calcul des pourcentages pour chaque taille
    ca_small = taille_transactions[taille_transactions['Taille de Transaction'] == 'Small']['Chiffre d\'Affaires'].sum()
    ca_large = taille_transactions[taille_transactions['Taille de Transaction'] == 'Large']['Chiffre d\'Affaires'].sum()
    
    pourcentage_small = (ca_small / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    pourcentage_large = (ca_large / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    
    # KPIs détaillés
    st.subheader("📋 Résumé des Comportements d'Achat")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💰 CA - Transactions Medium",
            f"{ca_medium:,.0f} €",
            f"{pourcentage_medium:.1f}% du total"
        )
    
    with col2:
        st.metric(
            "💰 CA - Transactions Small", 
            f"{ca_small:,.0f} €",
            f"{pourcentage_small:.1f}% du total"
        )
    
    with col3:
        st.metric(
            "💰 CA - Transactions Large",
            f"{ca_large:,.0f} €", 
            f"{pourcentage_large:.1f}% du total"
        )
    
    # Tableau récapitulatif
    _render_behavior_summary_table(taille_transactions, ca_small, ca_medium, ca_large, total_ca_comportement, pourcentage_small, pourcentage_medium, pourcentage_large)

def _render_behavior_summary_table(taille_transactions, ca_small, ca_medium, ca_large, total_ca_comportement, pourcentage_small, pourcentage_medium, pourcentage_large):
    """Affiche le tableau récapitulatif des comportements"""
    st.markdown("**📊 Tableau Récapitulatif**")
    recap_data = {
        'Taille': ['Small', 'Medium', 'Large', 'Total'],
        'Chiffre d\'Affaires (€)': [
            f"{ca_small:,.0f}",
            f"{ca_medium:,.0f}", 
            f"{ca_large:,.0f}",
            f"{total_ca_comportement:,.0f}"
        ],
        'Pourcentage CA': [
            f"{pourcentage_small:.1f}%",
            f"{pourcentage_medium:.1f}%",
            f"{pourcentage_large:.1f}%", 
            "100%"
        ],
        'Nombre de Commandes': [
            taille_transactions[taille_transactions['Taille de Transaction'] == 'Small']['Numéro_Commande'].sum(),
            taille_transactions[taille_transactions['Taille de Transaction'] == 'Medium']['Numéro_Commande'].sum(),
            taille_transactions[taille_transactions['Taille de Transaction'] == 'Large']['Numéro_Commande'].sum(),
            taille_transactions['Numéro_Commande'].sum()
        ]
    }
    
    recap_df = pd.DataFrame(recap_data)
    st.dataframe(recap_df, use_container_width=True, hide_index=True)
    
    st.info(f"""
    **💡 Insights Comportementaux :**
    - **Transactions Medium** : Principal moteur du CA ({pourcentage_medium:.1f}%) avec {taille_transactions[taille_transactions['Taille de Transaction'] == 'Medium']['Numéro_Commande'].sum()} commandes
    - **Transactions Small** : {taille_transactions[taille_transactions['Taille de Transaction'] == 'Small']['Numéro_Commande'].sum()} commandes mais seulement {pourcentage_small:.1f}% du CA
    - **Transactions Large** : {taille_transactions[taille_transactions['Taille de Transaction'] == 'Large']['Numéro_Commande'].sum()} commandes générant {pourcentage_large:.1f}% du CA
    """)

def _render_operational_indicators(df_filtered):
    """Affiche les indicateurs opérationnels"""
    # Statistiques des statuts
    statuts_commandes = df_filtered.groupby('Statut').agg({
        'Numéro_Commande': 'nunique', 
        "Chiffre d'Affaires": 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔄 Répartition des Commandes par Statut**")
        fig = px.pie(
            statuts_commandes, 
            names='Statut', 
            values='Numéro_Commande',
            color='Statut',
            color_discrete_map={
                'Shipped': '#00ff00',
                'In Process': '#ffa500', 
                'Disputed': '#ff0000',
                'Cancelled': '#808080',
                'Resolved': '#0000ff',
                'On Hold': '#ffff00'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**💰 Impact Financier par Statut**")
        fig = px.bar(
            statuts_commandes, 
            x='Statut', 
            y="Chiffre d'Affaires", 
            color='Statut',
            text_auto='.2s',
            color_discrete_map={
                'Shipped': '#00ff00',
                'In Process': '#ffa500', 
                'Disputed': '#ff0000',
                'Cancelled': '#808080',
                'Resolved': '#0000ff',
                'On Hold': '#ffff00'
            }
        )
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        fig.update_yaxes(tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)
    
    # KPIs opérationnels
    _render_operational_kpis(statuts_commandes)

def _render_operational_kpis(statuts_commandes):
    """Affiche les KPIs opérationnels"""
    commandes_shipped = statuts_commandes[statuts_commandes['Statut'] == 'Shipped']['Numéro_Commande'].sum()
    total_commandes = statuts_commandes['Numéro_Commande'].sum()
    taux_success = (commandes_shipped / total_commandes * 100) if total_commandes > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Commandes Expédiées", f"{commandes_shipped:,}")
    col2.metric("✅ Taux de Succès", f"{taux_success:.1f}%")
    col3.metric("🔄 Commandes en Cours", 
               f"{statuts_commandes[statuts_commandes['Statut'] == 'In Process']['Numéro_Commande'].sum():,}")

def _render_problem_analysis(df_filtered, df_original):
    """Affiche l'analyse des commandes problématiques"""
    commandes_problematiques = df_filtered[df_filtered['Statut'].isin(['Disputed', 'Cancelled'])]
    
    if not commandes_problematiques.empty:
        # Calcul des taux
        total_commandes_global = df_original['Numéro_Commande'].nunique()
        total_ca_global = df_original["Chiffre d'Affaires"].sum()
        
        analyse_problemes = commandes_problematiques.groupby('Statut').agg({
            'Numéro_Commande': 'nunique',
            'Chiffre d\'Affaires': 'sum'
        }).reset_index()
        
        analyse_problemes['Taux_Commandes'] = (analyse_problemes['Numéro_Commande'] / total_commandes_global * 100).round(2)
        analyse_problemes['Taux_CA'] = (analyse_problemes['Chiffre d\'Affaires'] / total_ca_global * 100).round(2)
        
        # KPIs problèmes
        _render_problem_kpis(analyse_problemes)
        
        # Graphique problèmes
        _render_problem_charts(analyse_problemes, commandes_problematiques)
        
        # Résumé final
        _render_final_summary(analyse_problemes)
    else:
        st.info("✅ Aucune commande problématique dans les données filtrées")

def _render_problem_kpis(analyse_problemes):
    """Affiche les KPIs des problèmes"""
    col1, col2, col3, col4 = st.columns(4)
    
    taux_litige = analyse_problemes[analyse_problemes['Statut'] == 'Disputed']['Taux_Commandes'].sum()
    taux_annulation = analyse_problemes[analyse_problemes['Statut'] == 'Cancelled']['Taux_Commandes'].sum()
    ca_litige = analyse_problemes[analyse_problemes['Statut'] == 'Disputed']['Chiffre d\'Affaires'].sum()
    ca_annulation = analyse_problemes[analyse_problemes['Statut'] == 'Cancelled']['Chiffre d\'Affaires'].sum()
    
    col1.metric("⚖️ Taux Litiges", f"{taux_litige}%")
    col2.metric("❌ Taux Annulations", f"{taux_annulation}%")
    col3.metric("💰 CA Litiges", f"{ca_litige:,.0f} €")
    col4.metric("💸 CA Annulations", f"{ca_annulation:,.0f} €")

def _render_problem_charts(analyse_problemes, commandes_problematiques):
    """Affiche les graphiques des problèmes"""
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            analyse_problemes, 
            names='Statut', 
            values='Chiffre d\'Affaires',
            title='Répartition du CA à Risque',
            color='Statut',
            color_discrete_map={
                'Disputed': '#ff4444', 
                'Cancelled': '#ff0000'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Évolution temporelle des problèmes
        problemes_temporel = commandes_problematiques.groupby(['Année', 'Statut']).agg({
            'Numéro_Commande': 'nunique'
        }).reset_index()
        
        fig = px.line(
            problemes_temporel,
            x='Année',
            y='Numéro_Commande',
            color='Statut',
            title='Évolution des Commandes Problématiques',
            markers=True,
            color_discrete_map={
                'Disputed': '#ff4444', 
                'Cancelled': '#ff0000'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

def _render_final_summary(analyse_problemes):
    """Affiche le résumé final"""
    taux_litige = analyse_problemes[analyse_problemes['Statut'] == 'Disputed']['Taux_Commandes'].sum()
    taux_annulation = analyse_problemes[analyse_problemes['Statut'] == 'Cancelled']['Taux_Commandes'].sum()
    
    st.success(f"""
    **✅ Performance Opérationnelle Excellente** 
    - **Taux de succès élevé** (calculé à partir des données filtrées)
    - Seulement **{(taux_litige + taux_annulation):.2f}%** de commandes problématiques
    - Processus de vente et livraison très efficaces
    """)