import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_temporal_analysis_tab(df_filtered, df_original):
    """Affiche l'onglet Analyse Temporelle"""
    
    st.header("Analyse Temporelle des Ventes")
    
    # Évolution Trimestrielle du Chiffre d'Affaires
    st.subheader("Évolution Trimestrielle du Chiffre d'Affaires")
    evolution_temporelle = df_filtered.groupby(['Année', 'Trimestre_ID']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    evolution_temporelle['Période'] = 'T' + evolution_temporelle['Trimestre_ID'].astype(str) + ' ' + evolution_temporelle['Année'].astype(str)
    fig = px.line(evolution_temporelle, x='Période', y="Chiffre d'Affaires", 
                  labels={'Chiffre d\'Affaires': 'CA (€)', 'Période': 'Trimestre'}, 
                  markers=True,
                  title="Évolution du Chiffre d'Affaires par Trimestre")
    st.plotly_chart(fig, use_container_width=True, key="temporelle_trimestre")

    # Saisonnalité des Ventes par Mois
    st.subheader("Saisonnalité des Ventes par Mois")
    noms_mois = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin', 
                 7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
    
    saison_mois_annee = df_filtered.groupby(['Année', 'Mois']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    saison_mois_annee['Nom_Mois'] = saison_mois_annee['Mois'].map(noms_mois)
    saison_mois_annee['Nom_Mois'] = pd.Categorical(saison_mois_annee['Nom_Mois'], 
                                                   categories=noms_mois.values(), 
                                                   ordered=True)
    saison_mois_annee = saison_mois_annee.sort_values(['Année', 'Mois'])
    
    fig = px.line(saison_mois_annee, x='Nom_Mois', y="Chiffre d'Affaires", 
                  color='Année', markers=True,
                  title="Saisonnalité des Ventes par Mois et par Année")
    st.plotly_chart(fig, use_container_width=True, key="temporelle_saisonnalite")
    
    # Tableau récapitulatif temporel
    _render_temporal_summary(df_filtered)
    
    # Performance par trimestre
    _render_quarterly_performance(df_filtered)
    
    # Performance détaillée par mois
    _render_monthly_performance(df_filtered)
    
    # Analyse de saisonnalité
    _render_seasonality_analysis(df_filtered)
    
    # Indicateurs clés temporels
    _render_temporal_kpis(df_filtered)

def _render_temporal_summary(df_filtered):
    """Affiche le tableau récapitulatif temporel"""
    st.markdown("---")
    st.subheader("📈 TABLEAU RÉCAPITULATIF TEMPOREL")
    
    performance_annuelle = df_filtered.groupby('Année').agg({
        "Chiffre d'Affaires": ['sum', 'count'],
        'Quantité_Commandée': 'sum',
        'Numéro_Commande': 'nunique',
        'Nom_du_Client': 'nunique'
    }).round(0)
    
    performance_annuelle.columns = ['CA_Total', 'Nb_Lignes', 'Quantité_Totale', 'Nb_Commandes', 'Nb_Clients']
    performance_annuelle['CA_Moyen_Commande'] = (performance_annuelle['CA_Total'] / performance_annuelle['Nb_Commandes']).round(0)
    performance_annuelle['Quantité_Moyenne_Ligne'] = (performance_annuelle['Quantité_Totale'] / performance_annuelle['Nb_Lignes']).round(1)
    performance_annuelle['Croissance_CA'] = performance_annuelle['CA_Total'].pct_change() * 100
    performance_annuelle['Croissance_Commandes'] = performance_annuelle['Nb_Commandes'].pct_change() * 100
    
    # Formatage pour l'affichage
    display_annuel = performance_annuelle.copy()
    display_annuel['CA_Total'] = display_annuel['CA_Total'].apply(lambda x: f"{x:,.0f} €")
    display_annuel['CA_Moyen_Commande'] = display_annuel['CA_Moyen_Commande'].apply(lambda x: f"{x:,.0f} €")
    display_annuel['Croissance_CA'] = display_annuel['Croissance_CA'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    display_annuel['Croissance_Commandes'] = display_annuel['Croissance_Commandes'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    
    st.markdown("**📅 PERFORMANCE PAR ANNÉE**")
    st.dataframe(display_annuel, use_container_width=True)

def _render_quarterly_performance(df_filtered):
    """Affiche la performance par trimestre"""
    st.markdown("**📊 PERFORMANCE PAR TRIMESTRE**")
    
    performance_trimestre = df_filtered.groupby(['Année', 'Trimestre_ID']).agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Quantité_Commandée': 'sum'
    }).reset_index()
    
    performance_trimestre['Période'] = 'T' + performance_trimestre['Trimestre_ID'].astype(str) + ' ' + performance_trimestre['Année'].astype(str)
    performance_trimestre = performance_trimestre.sort_values(['Année', 'Trimestre_ID'])
    
    # Calcul croissance trimestrielle
    performance_trimestre['CA_Trimestre_Prec'] = performance_trimestre["Chiffre d'Affaires"].shift(1)
    performance_trimestre['Croissance_Trimestre'] = ((performance_trimestre["Chiffre d'Affaires"] - performance_trimestre['CA_Trimestre_Prec']) / performance_trimestre['CA_Trimestre_Prec']) * 100
    
    # Formatage affichage
    display_trimestre = performance_trimestre[['Période', "Chiffre d'Affaires", 'Numéro_Commande', 'Quantité_Commandée', 'Croissance_Trimestre']].copy()
    display_trimestre["Chiffre d'Affaires"] = display_trimestre["Chiffre d'Affaires"].apply(lambda x: f"{x:,.0f} €")
    display_trimestre['Quantité_Commandée'] = display_trimestre['Quantité_Commandée'].apply(lambda x: f"{x:,}")
    display_trimestre['Croissance_Trimestre'] = display_trimestre['Croissance_Trimestre'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A")
    
    st.dataframe(display_trimestre, use_container_width=True, hide_index=True)

def _render_monthly_performance(df_filtered):
    """Affiche la performance détaillée par mois"""
    st.markdown("---")
    st.subheader("📅 PERFORMANCE DÉTAILLÉE PAR MOIS")
    
    performance_mois = df_filtered.groupby(['Année', 'Mois']).agg({
        "Chiffre d'Affaires": 'sum',
        'Numéro_Commande': 'nunique',
        'Quantité_Commandée': 'sum',
        'Nom_du_Client': 'nunique',
        'Gamme_de_Produits': 'nunique'
    }).reset_index()
    
    noms_mois_complets = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin', 
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    
    performance_mois['Nom_Mois'] = performance_mois['Mois'].map(noms_mois_complets)
    performance_mois['Période'] = performance_mois['Nom_Mois'] + ' ' + performance_mois['Année'].astype(str)
    performance_mois = performance_mois.sort_values(['Année', 'Mois'])
    
    # Calculs des indicateurs
    performance_mois['CA_Moyen_Commande'] = (performance_mois["Chiffre d'Affaires"] / performance_mois['Numéro_Commande']).round(0)
    performance_mois['Quantité_Moyenne_Commande'] = (performance_mois['Quantité_Commandée'] / performance_mois['Numéro_Commande']).round(1)
    performance_mois['CA_Mois_Prec'] = performance_mois["Chiffre d'Affaires"].shift(1)
    performance_mois['Croissance_Mensuelle'] = ((performance_mois["Chiffre d'Affaires"] - performance_mois['CA_Mois_Prec']) / performance_mois['CA_Mois_Prec']) * 100
    
    moyenne_ca_mensuel = performance_mois["Chiffre d'Affaires"].mean()
    performance_mois['Performance_vs_Moyenne'] = ((performance_mois["Chiffre d'Affaires"] - moyenne_ca_mensuel) / moyenne_ca_mensuel * 100).round(1)
    performance_mois['Rang_Mois'] = performance_mois["Chiffre d'Affaires"].rank(ascending=False).astype(int)
    
    # Formatage pour l'affichage
    display_mois = performance_mois[[
        'Période', 'Rang_Mois', "Chiffre d'Affaires", 'Numéro_Commande', 
        'Quantité_Commandée', 'Nom_du_Client', 'CA_Moyen_Commande',
        'Croissance_Mensuelle', 'Performance_vs_Moyenne'
    ]].copy()
    
    display_mois["Chiffre d'Affaires"] = display_mois["Chiffre d'Affaires"].apply(lambda x: f"{x:,.0f} €")
    display_mois['Quantité_Commandée'] = display_mois['Quantité_Commandée'].apply(lambda x: f"{x:,}")
    display_mois['CA_Moyen_Commande'] = display_mois['CA_Moyen_Commande'].apply(lambda x: f"{x:,.0f} €")
    display_mois['Croissance_Mensuelle'] = display_mois['Croissance_Mensuelle'].apply(
        lambda x: f"{x:+.1f}%" if pd.notna(x) and abs(x) < 1000 else "N/A"
    )
    display_mois['Performance_vs_Moyenne'] = display_mois['Performance_vs_Moyenne'].apply(
        lambda x: f"{x:+.1f}%" if pd.notna(x) else "N/A"
    )
    
    st.dataframe(display_mois, use_container_width=True, hide_index=True)
    
    # Top 5 des meilleurs mois
    _render_top_months(performance_mois)

def _render_top_months(performance_mois):
    """Affiche le top 5 des meilleurs mois"""
    st.markdown("**🏆 TOP 5 DES MEILLEURS MOIS**")
    
    top_5_mois = performance_mois.nlargest(5, "Chiffre d'Affaires")[['Période', "Chiffre d'Affaires", 'Numéro_Commande', 'Performance_vs_Moyenne']]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    tops = [col1, col2, col3, col4, col5]
    
    for i, (idx, mois) in enumerate(top_5_mois.iterrows()):
        with tops[i]:
            st.metric(
                label=f"#{i+1} {mois['Période'].split(' ')[0]}",
                value=f"{mois['Chiffre d\'Affaires']:,.0f} €",
                delta=f"{mois['Performance_vs_Moyenne']:+.1f}% vs moyenne"
            )

def _render_seasonality_analysis(df_filtered):
    """Affiche l'analyse de saisonnalité"""
    st.markdown("**📊 ANALYSE DE SAISONNALITÉ**")
    
    noms_mois_complets = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin', 
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    
    saisonnalite_mensuelle = df_filtered.groupby('Mois').agg({
        "Chiffre d'Affaires": ['sum', 'mean', 'count'],
        'Numéro_Commande': 'nunique'
    }).round(0)
    
    saisonnalite_mensuelle.columns = ['CA_Total', 'CA_Moyen_Mois', 'Nb_Lignes', 'Nb_Commandes']
    saisonnalite_mensuelle['Nom_Mois'] = saisonnalite_mensuelle.index.map(noms_mois_complets)
    saisonnalite_mensuelle['Part_CA'] = (saisonnalite_mensuelle['CA_Total'] / saisonnalite_mensuelle['CA_Total'].sum() * 100).round(1)
    saisonnalite_mensuelle = saisonnalite_mensuelle.sort_index()
    
    col_saison1, col_saison2 = st.columns(2)
    
    with col_saison1:
        st.markdown("**Mois les plus forts :**")
        top_mois = saisonnalite_mensuelle.nlargest(3, 'CA_Total')
        for i, (mois, data) in enumerate(top_mois.iterrows(), 1):
            st.write(f"{i}. **{data['Nom_Mois']}** : {data['Part_CA']}% du CA annuel")
    
    with col_saison2:
        st.markdown("**Mois les plus faibles :**")
        bottom_mois = saisonnalite_mensuelle.nsmallest(3, 'CA_Total')
        for i, (mois, data) in enumerate(bottom_mois.iterrows(), 1):
            st.write(f"{i}. **{data['Nom_Mois']}** : {data['Part_CA']}% du CA annuel")
    
    _render_seasonal_recommendations(saisonnalite_mensuelle)

def _render_seasonal_recommendations(saisonnalite_mensuelle):
    """Affiche les recommandations saisonnières"""
    with st.expander("💡 RECOMMANDATIONS SAISONNIÈRES"):
        top_mois = saisonnalite_mensuelle.nlargest(3, 'CA_Total')
        bottom_mois = saisonnalite_mensuelle.nsmallest(3, 'CA_Total')
        ecart_saisonnalite = (top_mois['Part_CA'].max() - bottom_mois['Part_CA'].min())
        
        if ecart_saisonnalite > 15:
            st.warning("**🔴 FORTE SAISONNALITÉ DÉTECTÉE**")
            st.write("- Planifier les stocks selon les pics")
            st.write("- Renforcer le marketing en périodes creuses")
            st.write("- Anticiper les besoins en ressources")
        elif ecart_saisonnalite > 8:
            st.info("**🟡 SAISONNALITÉ MODÉRÉE**")
            st.write("- Optimiser les opérations selon la demande")
            st.write("- Développer des offres hors-saison")
        else:
            st.success("**🟢 ACTIVITÉ STABLE**")
            st.write("- Répartition équilibrée sur l'année")
            st.write("- Focus sur la croissance régulière")

def _render_temporal_kpis(df_filtered):
    """Affiche les indicateurs clés temporels"""
    st.markdown("---")
    st.subheader("🎯 INDICATEURS CLÉS TEMPORELS")
    
    # Calcul des meilleures périodes
    performance_trimestre = df_filtered.groupby(['Année', 'Trimestre_ID']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    performance_trimestre['Période'] = 'T' + performance_trimestre['Trimestre_ID'].astype(str) + ' ' + performance_trimestre['Année'].astype(str)
    meilleur_trimestre = performance_trimestre.loc[performance_trimestre["Chiffre d'Affaires"].idxmax()]
    
    meilleur_mois_data = df_filtered.groupby(['Année', 'Mois']).agg({"Chiffre d'Affaires": 'sum'}).reset_index()
    meilleur_mois_data = meilleur_mois_data.loc[meilleur_mois_data["Chiffre d'Affaires"].idxmax()]
    noms_mois = {1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin', 
                 7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'}
    
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
        ca_mensuel = df_filtered.groupby('Mois')["Chiffre d'Affaires"].sum()
        ratio_saisonnalite = ca_mensuel.max() / ca_mensuel.min() if ca_mensuel.min() > 0 else 0
        st.metric(
            "📊 Amplitude Saisonnière",
            f"{ratio_saisonnalite:.1f}x",
            delta="Élevée" if ratio_saisonnalite > 3 else "Modérée"
        )
    
    with col4:
        performance_annuelle = df_filtered.groupby('Année').agg({"Chiffre d'Affaires": 'sum'})
        if len(performance_annuelle) >= 2:
            derniere_croissance = performance_annuelle.pct_change().iloc[-1].values[0] * 100
            tendance = "📈 Hausse" if derniere_croissance > 5 else "➡️ Stable" if derniere_croissance > -5 else "📉 Baisse"
        else:
            tendance = "➡️ Données insuffisantes"
        
        st.metric("🎯 Tendance Globale", tendance)
    
    _render_temporal_recommendations(df_filtered)

def _render_temporal_recommendations(df_filtered):
    """Affiche les recommandations temporelles"""
    with st.expander("💡 ANALYSE ET RECOMMANDATIONS TEMPORELLES"):
        performance_annuelle = df_filtered.groupby('Année').agg({"Chiffre d'Affaires": 'sum'})
        
        if len(performance_annuelle) >= 2:
            derniere_croissance = performance_annuelle.pct_change().iloc[-1].values[0] * 100
            
            if derniere_croissance > 10:
                analyse = "**🟢 EXCELLENTE CROISSANCE** - Maintenir la dynamique"
            elif derniere_croissance > 0:
                analyse = "**🟡 CROISSANCE POSITIVE** - Renforcer les performances"
            elif derniere_croissance > -10:
                analyse = "**🟠 STAGNATION** - Identifier les freins à la croissance"
            else:
                analyse = "**🔴 DÉCLIN** - Plan d'action correctif urgent"
        else:
            analyse = "**⚪ DONNÉES INSUFFISANTES** - Période d'analyse trop courte"
        
        st.markdown(f"""
        **ANALYSE :** {analyse}
        
        **RECOMMANDATIONS :**
        - **Capitaliser** sur les trimestres forts
        - **Anticiper** la saisonnalité identifiée  
        - **Renforcer** les périodes creuses
        - **Planifier** selon la tendance annuelle
        """)