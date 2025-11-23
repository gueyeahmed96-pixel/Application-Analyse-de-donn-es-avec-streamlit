import streamlit as st
import pandas as pd

def render_financial_kpis(ca_total, panier_moyen, croissance_yoy):
    """Affiche les KPIs financiers"""
    st.markdown("**💰 KPIs Financiers**")
    st.metric("Chiffre d'Affaires Total", f"{ca_total:,.0f} €")
    st.metric("Panier Moyen (AOV)", f"{panier_moyen:,.0f} €")
    st.metric("Croissance Annuelle", f"{croissance_yoy:+.1f} %", 
             delta=f"{croissance_yoy:+.1f}%" if croissance_yoy != 0 else None)

def render_concentration_kpis(part_classic_cars, part_usa, part_top_client, nom_top_client):
    """Affiche les KPIs de concentration"""
    st.markdown("**🎯 KPIs de Concentration**")
    st.metric("Part 'Classic Cars'", f"{part_classic_cars:.1f} %")
    st.metric("Part Marché USA", f"{part_usa:.1f} %")
    st.metric(f"Part {nom_top_client[:15]}...", f"{part_top_client:.1f} %")

def render_operational_kpis(taux_reussite, part_ca_risque, total_commandes):
    """Affiche les KPIs opérationnels"""
    st.markdown("**⚡ KPIs Opérationnels**")
    st.metric("Taux de Réussite", f"{taux_reussite:.1f} %")
    st.metric("CA à Risque", f"{part_ca_risque:.1f} %")
    st.metric("Commandes Traitées", f"{total_commandes:,}")

def render_segment_kpis(segments):
    """Affiche les KPIs par segment client"""
    for segment in ['VIP', 'Moyen', 'Base']:
        if segment in segments.index:
            data = segments.loc[segment]
            st.metric(
                label=f"**{segment}** ({data['Nb_Clients']} clients)",
                value=f"{data['Part_CA']}% du CA",
                delta=f"{data['CA_Moyen']:,.0f}€/client"
            )

def render_temporal_kpis(df_filtered):
    """Affiche les KPIs temporels"""
    # Meilleur trimestre
    performance_trimestre = df_filtered.groupby(['Année', 'Trimestre_ID']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    performance_trimestre['Période'] = 'T' + performance_trimestre['Trimestre_ID'].astype(str) + ' ' + performance_trimestre['Année'].astype(str)
    meilleur_trimestre = performance_trimestre.loc[performance_trimestre["Chiffre d'Affaires"].idxmax()]
    
    # Meilleur mois
    meilleur_mois_data = df_filtered.groupby(['Année', 'Mois']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    meilleur_mois_data = meilleur_mois_data.loc[meilleur_mois_data["Chiffre d'Affaires"].idxmax()]
    noms_mois = {1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin', 
                 7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'}
    
    # Saisonnalité
    ca_mensuel = df_filtered.groupby('Mois')["Chiffre d'Affaires"].sum()
    ratio_saisonnalite = ca_mensuel.max() / ca_mensuel.min() if ca_mensuel.min() > 0 else 0
    
    # Tendance
    performance_annuelle = df_filtered.groupby('Année').agg({"Chiffre d'Affaires": 'sum'})
    if len(performance_annuelle) >= 2:
        derniere_croissance = performance_annuelle.pct_change().iloc[-1].values[0] * 100
        tendance = "📈 Hausse" if derniere_croissance > 5 else "➡️ Stable" if derniere_croissance > -5 else "📉 Baisse"
    else:
        tendance = "➡️ Données insuffisantes"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🏆 Meilleur Trimestre",
            f"{meilleur_trimestre['Période']}",
            delta=f"{meilleur_trimestre['Chiffre d\'Affaires']:,.0f} €"
        )
    
    with col2:
        st.metric(
            "📈 Meilleur Mois",
            f"{noms_mois.get(meilleur_mois_data['Mois'], 'N/A')} {int(meilleur_mois_data['Année'])}",
            delta=f"{meilleur_mois_data['Chiffre d\'Affaires']:,.0f} €"
        )
    
    with col3:
        st.metric(
            "📊 Amplitude Saisonnière",
            f"{ratio_saisonnalite:.1f}x",
            delta="Élevée" if ratio_saisonnalite > 3 else "Modérée"
        )
    
    with col4:
        st.metric("🎯 Tendance Globale", tendance)

def render_geo_kpis(performance_pays):
    """Affiche les KPIs géographiques"""
    top_pays = performance_pays.iloc[0]
    concentration = (performance_pays.head(3)["Chiffre d'Affaires"].sum() / 
                    performance_pays["Chiffre d'Affaires"].sum() * 100)
    avg_per_country = performance_pays["Chiffre d'Affaires"].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Pays Leader",
            value=top_pays['Pays'],
            delta=f"{top_pays['Chiffre d\'Affaires']:,.0f} €"
        )
    
    with col2:
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
        st.metric(
            label="CA Moyen par Pays",
            value=f"{avg_per_country:,.0f} €"
        )

def render_product_kpis(performance_gammes):
    """Affiche les KPIs produits"""
    top_gamme = performance_gammes.iloc[0]
    concentration_top3 = performance_gammes.head(3)['Part_CA'].sum()
    ca_moyen_gamme = performance_gammes['CA_Total'].mean()
    nb_gammes_actives = len(performance_gammes)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🏆 Gamme Leader",
            top_gamme.name,
            delta=f"{top_gamme['Part_CA']}% du CA"
        )
    
    with col2:
        st.metric(
            "📊 Concentration Top 3",
            f"{concentration_top3:.1f}%"
        )
    
    with col3:
        st.metric(
            "💰 CA Moyen par Gamme",
            f"{ca_moyen_gamme:,.0f} €"
        )
    
    with col4:
        st.metric(
            "🏷️ Gammes Actives",
            f"{nb_gammes_actives}"
        )

def render_behavior_kpis(taille_transactions):
    """Affiche les KPIs de comportement d'achat"""
    ca_medium = taille_transactions[taille_transactions['Taille de Transaction'] == 'Medium']['Chiffre d\'Affaires'].sum()
    ca_small = taille_transactions[taille_transactions['Taille de Transaction'] == 'Small']['Chiffre d\'Affaires'].sum()
    ca_large = taille_transactions[taille_transactions['Taille de Transaction'] == 'Large']['Chiffre d\'Affaires'].sum()
    total_ca_comportement = taille_transactions['Chiffre d\'Affaires'].sum()
    
    pourcentage_medium = (ca_medium / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    pourcentage_small = (ca_small / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    pourcentage_large = (ca_large / total_ca_comportement * 100) if total_ca_comportement > 0 else 0
    
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

def render_operational_status_kpis(statuts_commandes):
    """Affiche les KPIs de statut opérationnel"""
    commandes_shipped = statuts_commandes[statuts_commandes['Statut'] == 'Shipped']['Numéro_Commande'].sum()
    total_commandes = statuts_commandes['Numéro_Commande'].sum()
    taux_success = (commandes_shipped / total_commandes * 100) if total_commandes > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Commandes Expédiées", f"{commandes_shipped:,}")
    col2.metric("✅ Taux de Succès", f"{taux_success:.1f}%")
    col3.metric("🔄 Commandes en Cours", 
               f"{statuts_commandes[statuts_commandes['Statut'] == 'In Process']['Numéro_Commande'].sum():,}")

def render_global_score_kpis(scores, score_global):
    """Affiche les KPIs de score global"""
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