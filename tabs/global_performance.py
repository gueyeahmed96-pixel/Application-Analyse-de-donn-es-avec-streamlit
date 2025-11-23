import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render_global_performance_tab(df_filtered, df_original):
    """Affiche l'onglet Performance Globale avec les données filtrées"""
    
    # ==============================================================================
    # SYNTHÈSE STRATÉGIQUE - KPIs CLÉS DE PERFORMANCE (AVEC FILTRES)
    # ==============================================================================
    st.subheader("🏆 SYNTHÈSE STRATÉGIQUE")
    
    # CALCUL DIRECT AVEC LES DONNÉES FILTRÉES
    ca_total = df_filtered["Chiffre d'Affaires"].sum()
    total_commandes = df_filtered['Numéro_Commande'].nunique()
    panier_moyen = ca_total / total_commandes if total_commandes > 0 else 0
    
    # Calcul croissance avec données filtrées
    annees = sorted(df_filtered['Année'].unique())
    if len(annees) >= 2:
        ca_derniere = df_filtered[df_filtered['Année'] == annees[-1]]["Chiffre d'Affaires"].sum()
        ca_precedente = df_filtered[df_filtered['Année'] == annees[-2]]["Chiffre d'Affaires"].sum()
        croissance = ((ca_derniere - ca_precedente) / ca_precedente * 100) if ca_precedente > 0 else 0
    else:
        croissance = 0
    
    # Concentration avec données filtrées
    if ca_total > 0:
        part_classic_cars = (df_filtered[df_filtered['Gamme_de_Produits'] == 'Classic Cars']["Chiffre d'Affaires"].sum() / ca_total) * 100
        part_usa = (df_filtered[df_filtered['Pays'] == 'USA']["Chiffre d'Affaires"].sum() / ca_total) * 100
        
        # Top client avec données filtrées
        top_clients = df_filtered.groupby('Nom_du_Client')["Chiffre d'Affaires"].sum()
        if not top_clients.empty:
            top_client = top_clients.nlargest(1)
            nom_top_client = top_client.index[0]
            part_top_client = (top_client.iloc[0] / ca_total) * 100
        else:
            nom_top_client = "Aucun"
            part_top_client = 0
    else:
        part_classic_cars = 0
        part_usa = 0
        part_top_client = 0
        nom_top_client = "Aucun"
    
    # KPIs opérationnels avec données filtrées
    commandes_problematiques = df_filtered[df_filtered['Statut'].isin(['Cancelled', 'Disputed'])]['Numéro_Commande'].nunique()
    taux_reussite = ((total_commandes - commandes_problematiques) / total_commandes * 100) if total_commandes > 0 else 0
    
    ca_a_risque = df_filtered[df_filtered['Statut'].isin(['Cancelled', 'Disputed'])]["Chiffre d'Affaires"].sum()
    part_ca_risque = (ca_a_risque / ca_total * 100) if ca_total > 0 else 0
    
    # AFFICHAGE DES INDICATEURS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💰 KPIs Financiers**")
        st.metric("Chiffre d'Affaires", f"{ca_total:,.0f} €")
        st.metric("Panier Moyen", f"{panier_moyen:,.0f} €")
        st.metric("Croissance", f"{croissance:+.1f} %", delta=f"{croissance:+.1f}%")
    
    with col2:
        st.markdown("**🎯 Concentration**")
        st.metric("Part Classic Cars", f"{part_classic_cars:.1f} %")
        st.metric("Part USA", f"{part_usa:.1f} %")
        st.metric(f"Part {nom_top_client[:12]}...", f"{part_top_client:.1f} %")
    
    with col3:
        st.markdown("**⚡ Opérationnel**")
        st.metric("Taux de Réussite", f"{taux_reussite:.1f} %")
        st.metric("CA à Risque", f"{part_ca_risque:.1f} %")
        st.metric("Commandes", f"{total_commandes:,}")
    
    # Analyse et Recommandations
    _render_strategic_analysis(ca_total, panier_moyen, croissance, part_classic_cars, part_usa, part_top_client, nom_top_client, taux_reussite, df_filtered)
    
    # ==============================================================================
    # PYRAMIDE DE RENTABILITÉ CLIENT (AVEC FILTRES)
    # ==============================================================================
    st.subheader("🏆 PYRAMIDE DE RENTABILITÉ CLIENT")
    
    if not df_filtered.empty:
        # Analyse des clients par segments avec données filtrées
        ca_par_client = df_filtered.groupby('Nom_du_Client').agg({
            "Chiffre d'Affaires": 'sum',
            'Numéro_Commande': 'nunique',
            'Pays': 'first'
        }).sort_values("Chiffre d'Affaires", ascending=False)
        
        if not ca_par_client.empty:
            # Segmentation des clients
            total_ca_clients = ca_par_client["Chiffre d'Affaires"].sum()
            ca_par_client['Part_CA'] = (ca_par_client["Chiffre d'Affaires"] / total_ca_clients * 100)
            ca_par_client['Segment'] = pd.cut(ca_par_client['Part_CA'], 
                                            bins=[0, 1, 5, 100], 
                                            labels=['Base', 'Moyen', 'VIP'])
            
            # Calculs par segment
            segments = ca_par_client.groupby('Segment').agg({
                "Chiffre d'Affaires": ['sum', 'count'],
                'Numéro_Commande': 'sum'
            }).round(0)
            
            segments.columns = ['CA_Total', 'Nb_Clients', 'Nb_Commandes']
            segments['Part_CA'] = (segments['CA_Total'] / total_ca_clients * 100).round(1)
            segments['CA_Moyen'] = (segments['CA_Total'] / segments['Nb_Clients']).round(0)
            
            # Affichage de la pyramide
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Graphique pyramide
                fig_pyramide = go.Figure()
                
                segments_ordered = segments.loc[['VIP', 'Moyen', 'Base']] if 'VIP' in segments.index else segments
                
                fig_pyramide.add_trace(go.Bar(
                    y=['CLIENTS VIP', 'CLIENTÈLE MOYENNE', 'BASE CLIENTS'],
                    x=segments_ordered['Part_CA'],
                    orientation='h',
                    marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                    text=segments_ordered['Part_CA'].apply(lambda x: f'{x}%'),
                    textposition='auto',
                ))
                
                fig_pyramide.update_layout(
                    title="Répartition du CA par Segment Client (AVEC FILTRES)",
                    xaxis_title="Part du Chiffre d'Affaires (%)",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_pyramide, use_container_width=True)
            
            with col2:
                st.markdown("**📊 CARACTÉRISTIQUES PAR SEGMENT**")
                for segment in ['VIP', 'Moyen', 'Base']:
                    if segment in segments.index:
                        data = segments.loc[segment]
                        st.metric(
                            label=f"**{segment}** ({data['Nb_Clients']} clients)",
                            value=f"{data['Part_CA']}% du CA",
                            delta=f"{data['CA_Moyen']:,.0f}€/client"
                        )
        else:
            st.info("Aucune donnée client disponible avec les filtres actuels")
    else:
        st.info("Aucune donnée disponible pour la pyramide client avec les filtres actuels")
    
    # Recommandations stratégiques
    _render_segment_strategies()
    
    # ==============================================================================
    # MATRICE PRODUIT/MARCHÉ STRATÉGIQUE (AVEC FILTRES)
    # ==============================================================================
    st.subheader("🎯 MATRICE STRATÉGIQUE PRODUITS/MARCHÉS")
    
    if not df_filtered.empty:
        # Top 4 pays et top 4 gammes pour la matrice AVEC DONNÉES FILTRÉES
        top_pays = df_filtered.groupby('Pays')["Chiffre d'Affaires"].sum().nlargest(4).index
        top_gammes = df_filtered.groupby('Gamme_de_Produits')["Chiffre d'Affaires"].sum().nlargest(4).index
        
        # Création de la matrice AVEC DONNÉES FILTRÉES
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
            title="Performance CA par Produit/Marché (AVEC FILTRES)",
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
        
        st.plotly_chart(fig_matrice, use_container_width=True)
        
        # Analyse des opportunités AVEC DONNÉES FILTRÉES
        _render_opportunity_analysis(df_filtered, top_gammes, top_pays)
    else:
        st.info("Aucune donnée disponible pour la matrice stratégique avec les filtres actuels")
    
    # ==============================================================================
    # TABLEAU RÉCAPITULATIF GLOBAL (AVEC FILTRES)
    # ==============================================================================
    st.markdown("---")
    st.markdown("### 📊 TABLEAU DE BORD EXÉCUTIF")
    
    if not df_filtered.empty:
        recap_df = _create_executive_dashboard(df_filtered, ca_total, panier_moyen, croissance, part_classic_cars, part_usa, part_top_client, nom_top_client, taux_reussite, part_ca_risque, total_commandes)
        st.dataframe(recap_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible pour le tableau exécutif avec les filtres actuels")
    
    # ==============================================================================
    # CARTE DE SCORE GLOBALE (AVEC FILTRES)
    # ==============================================================================
    if not df_filtered.empty:
        scores, score_global = _calculate_global_scores(df_filtered, ca_total, croissance, part_classic_cars, part_top_client, taux_reussite, df_original)
        
        # Affichage des scores
        col1, col2, col3, col4, col5, col6 = st.columns([2,1,1,1,1,1])
        
        with col1:
            st.metric(
                "🏆 SCORE GLOBAL", 
                f"{score_global:.0f}/100",
                delta="Excellente" if score_global > 80 else "Bonne" if score_global > 60 else "À améliorer",
                delta_color="normal" if score_global > 60 else "off"
            )
        
        with col2:
            st.metric("💰 Financier", f"{scores['Financier']:.0f}")
        
        with col3:
            st.metric("👥 Clientèle", f"{scores['Clientèle']:.0f}")
        
        with col4:
            st.metric("🏷️ Produits", f"{scores['Produits']:.0f}")
        
        with col5:
            st.metric("⚡ Opérationnel", f"{scores['Opérationnel']:.0f}")
        
        with col6:
            st.metric("🌍 Géographie", f"{scores['Géographie']:.0f}")
        
        # Graphique radar des scores
        fig_radar = _create_radar_chart(scores)
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour les scores avec les filtres actuels")
    
    # ==============================================================================
    # ALERTES STRATÉGIQUES INTELLIGENTES (AVEC FILTRES)
    # ==============================================================================
    st.markdown("---")
    st.markdown("### 🚨 ALERTES STRATÉGIQUES & RECOMMANDATIONS")
    
    if not df_filtered.empty:
        alertes_strategiques = _generate_strategic_alerts(croissance, part_classic_cars, part_top_client, taux_reussite, df_filtered)
        _render_strategic_alerts(alertes_strategiques)
    else:
        st.warning("⚠️ Aucune donnée disponible pour générer des alertes stratégiques")

# ==============================================================================
# FONCTIONS AUXILIAIRES
# ==============================================================================

def _render_strategic_analysis(ca_total, panier_moyen, croissance, part_classic_cars, part_usa, part_top_client, nom_top_client, taux_reussite, df_filtered):
    """Affiche l'analyse stratégique et les recommandations"""
    with st.expander("📋 ANALYSE STRATÉGIQUE ET RECOMMANDATIONS"):
        if df_filtered.empty:
            st.warning("Aucune donnée disponible pour l'analyse stratégique")
            return
            
        st.markdown(f"""
        **🎯 POINTS FORTS :**
        - **Performance financière** : {ca_total:,.0f} € de chiffre d'affaires
        - **Panier moyen élevé** : {panier_moyen:,.0f} € par commande
        - **Excellence opérationnelle** : {taux_reussite:.1f}% de taux de réussite
        
        **⚠️ POINTS DE VIGILANCE :**
        - **Dépendance produit** : {part_classic_cars:.1f}% du CA sur Classic Cars
        - **Concentration géographique** : {part_usa:.1f}% du CA sur le marché USA
        - **Dépendance client** : {part_top_client:.1f}% du CA avec {nom_top_client}
        - **Croissance** : {croissance:+.1f}% sur la période
        
        **💡 RECOMMANDATIONS STRATÉGIQUES :**
        1. **Diversification produits** : Réduire la dépendance aux Classic Cars
        2. **Expansion internationale** : Développer de nouveaux marchés
        3. **Fidélisation client** : Renforcer le portefeuille clients
        4. **Optimisation opérationnelle** : Maintenir le taux de réussite de {taux_reussite:.1f}%
        """)

def _render_segment_strategies():
    """Affiche les stratégies par segment client"""
    with st.expander("💡 STRATÉGIES PAR SEGMENT"):
        st.markdown("""
        **🎯 CLIENTS VIP (Top 20% du CA)**
        - **Stratégie** : Relation personnalisée, services premium
        - **Objectif** : Fidélisation maximale
        
        **📈 CLIENTÈLE MOYENNE (15-30% du CA)**  
        - **Stratégie** : Programmes de développement, upselling
        - **Objectif** : Conversion vers VIP
        
        **👥 BASE CLIENTS (Reste du CA)**
        - **Stratégie** : Automatisation, efficacité coûts
        - **Objectif** : Rentabilisation
        """)

def _render_opportunity_analysis(df_filtered, top_gammes, top_pays):
    """Affiche l'analyse des opportunités"""
    with st.expander("🔍 ANALYSE DES OPPORTUNITÉS"):
        # Trouver les meilleures combinaisons avec données filtrées
        meilleures_combinaisons = []
        for gamme in top_gammes:
            for pays in top_pays:
                ca = df_filtered[
                    (df_filtered['Gamme_de_Produits'] == gamme) & 
                    (df_filtered['Pays'] == pays)
                ]["Chiffre d'Affaires"].sum()
                if ca > 0:
                    meilleures_combinaisons.append((gamme, pays, ca))
        
        if meilleures_combinaisons:
            meilleures_combinaisons.sort(key=lambda x: x[2], reverse=True)
            
            st.markdown("**🚀 TOP 3 COMBINAISONS PRODUIT/MARCHÉ :**")
            for i, (gamme, pays, ca) in enumerate(meilleures_combinaisons[:3], 1):
                st.write(f"{i}. **{gamme}** en **{pays}** : {ca:,.0f} €")
        else:
            st.info("Aucune combinaison produit/marché significative")
        
        st.markdown("**💡 RECOMMANDATIONS :**")
        st.write("- **Développer** les combinaisons performantes")
        st.write("- **Explorer** les marchés sous-représentés")
        st.write("- **Adapter** l'offre produit par marché")

def _create_executive_dashboard(df_filtered, ca_total, panier_moyen, croissance, part_classic_cars, part_usa, part_top_client, nom_top_client, taux_reussite, part_ca_risque, total_commandes):
    """Crée le tableau de bord exécutif"""
    pays_couverts = df_filtered['Pays'].nunique()
    top_pays_nom = df_filtered.groupby('Pays')["Chiffre d'Affaires"].sum().idxmax() if not df_filtered.empty else "Aucun"
    
    recap_data = {
        'Domaine': ['💰 FINANCIER', '👥 CLIENTÈLE', '🏷️ PRODUITS', '⚡ OPÉRATIONNEL', '🌍 GÉOGRAPHIE'],
        'KPI Principal': [
            f"{ca_total:,.0f} €", 
            f"{df_filtered['Nom_du_Client'].nunique():,}",
            f"{df_filtered['Gamme_de_Produits'].nunique():,}",
            f"{taux_reussite:.1f}%",
            f"{pays_couverts}"
        ],
        'Indicateur Secondaire': [
            f"{panier_moyen:,.0f} €/cmd",
            f"{part_top_client:.1f}% top client", 
            f"{part_classic_cars:.1f}% leader",
            f"{total_commandes:,} commandes",
            f"{top_pays_nom}"
        ],
        'Performance': [
            f"📈 {croissance:+.1f}% vs N-1" if croissance != 0 else "➡️ Stable",
            f"📊 {(df_filtered['Quantité_Commandée'].sum() / total_commandes):.1f} unités/cmd" if total_commandes > 0 else "N/A",
            f"🎯 {df_filtered['Code_Produit'].nunique():,} ref. actives", 
            f"⚠️ {part_ca_risque:.1f}% à risque",
            f"📍 {df_filtered['Ville'].nunique():,} villes"
        ],
        'Statut': [
            "🟢 Excellente" if ca_total > 0 else "🔴 Aucune donnée",
            "🟢 Diversifiée" if part_top_client < 15 else "🟡 Concentrée" if part_top_client < 30 else "🔴 Risquée",
            "🟢 Équilibré" if part_classic_cars < 40 else "🟡 Concentré" if part_classic_cars < 60 else "🔴 Dépendant",
            "🟢 Optimal" if taux_reussite > 95 else "🟡 Bon" if taux_reussite > 90 else "🔴 Critique",
            "🟢 Mondial" if pays_couverts > 10 else "🟡 Régional" if pays_couverts > 5 else "🔴 Local"
        ],
        'Action Prioritaire': [
            "Maintenir croissance" if croissance > 5 else "Stimuler ventes",
            "Fidéliser VIP" if part_top_client > 20 else "Développer base",
            "Diversifier offre" if part_classic_cars > 40 else "Renforcer leader",
            "Optimiser processus" if taux_reussite < 95 else "Maintenir excellence", 
            "Étendre marché" if pays_couverts < 10 else "Approfondir présence"
        ]
    }
    
    return pd.DataFrame(recap_data)

def _calculate_global_scores(df_filtered, ca_total, croissance, part_classic_cars, part_top_client, taux_reussite, df_original):
    """Calcule les scores globaux de performance"""
    base_financier = 50
    ajustement_croissance = min(25, max(-25, croissance * 0.4))
    ajustement_ca = min(25, max(0, (ca_total / df_original["Chiffre d'Affaires"].sum()) * 25)) if df_original["Chiffre d'Affaires"].sum() > 0 else 0
    
    scores = {
        'Financier': min(100, max(0, base_financier + ajustement_croissance + ajustement_ca)),
        'Clientèle': min(100, max(0, 80 if part_top_client < 15 else 60 if part_top_client < 25 else 40)),
        'Produits': min(100, max(0, 80 if part_classic_cars < 35 else 60 if part_classic_cars < 50 else 40)),
        'Opérationnel': min(100, max(0, taux_reussite)),
        'Géographie': min(100, max(0, df_filtered['Pays'].nunique() * 8))
    }
    score_global = sum(scores.values()) / len(scores)
    
    return scores, score_global

def _create_radar_chart(scores):
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
        title="Profil de Performance par Domaine Stratégique (AVEC FILTRES)",
        height=400
    )
    
    return fig_radar

def _generate_strategic_alerts(croissance, part_classic_cars, part_top_client, taux_reussite, df_filtered):
    """Génère les alertes stratégiques automatiques"""
    alertes_strategiques = []
    
    if croissance < -10:
        alertes_strategiques.append(("🔴 CRITIQUE", "Croissance fortement négative", "Revoir stratégie commerciale d'urgence"))
    elif croissance < 0:
        alertes_strategiques.append(("🟡 ATTENTION", "Croissance en recul", "Analyser causes et ajuster offre"))
    
    if part_classic_cars > 50:
        alertes_strategiques.append(("🔴 RISQUE ÉLEVÉ", "Dépendance excessive à Classic Cars", "Plan de diversification produits urgent"))
    elif part_classic_cars > 35:
        alertes_strategiques.append(("🟡 VIGILANCE", "Concentration produit élevée", "Développer autres gammes"))
    
    if part_top_client > 25:
        alertes_strategiques.append(("🔴 RISQUE CLIENT", "Top client trop important", "Programme de diversification clientèle"))
    
    if taux_reussite < 90:
        alertes_strategiques.append(("🔴 OPÉRATIONNEL", "Taux de réussite sous-optimal", "Audit processus commandes"))
    
    if df_filtered['Pays'].nunique() < 8:
        alertes_strategiques.append(("🟡 MARCHÉ", "Couverture géographique limitée", "Étude expansion marchés"))
    
    if not alertes_strategiques:
        alertes_strategiques.append(("🟢 EXCELLENT", "Performance globale optimale", "Maintenir la trajectoire"))
    
    return alertes_strategiques

def _render_strategic_alerts(alertes_strategiques):
    """Affiche les alertes stratégiques"""
    for niveau, titre, recommandation in alertes_strategiques:
        if niveau.startswith("🔴"):
            st.error(f"**{niveau} {titre}** - *{recommandation}*")
        elif niveau.startswith("🟡"):
            st.warning(f"**{niveau} {titre}** - *{recommandation}*")
        else:
            st.success(f"**{niveau} {titre}** - *{recommandation}*")