import streamlit as st
import pandas as pd

# Configuration de base
st.set_page_config(page_title="Debug App", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data_cleaned.csv")
    df['Date_Commande'] = pd.to_datetime(df['Date_Commande'])
    return df

df = load_data()

# Initialisation session state
if 'selected_years' not in st.session_state:
    st.session_state.selected_years = sorted(df['Année'].unique())
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = sorted(df['Pays'].unique())
if 'selected_productlines' not in st.session_state:
    st.session_state.selected_productlines = sorted(df['Gamme_de_Produits'].unique())

st.title("🔧 APPLICATION DE DEBUG")

# Section 1: État des filtres
st.header("1. ÉTAT DES FILTRES DANS SESSION_STATE")
st.write(f"selected_years: {st.session_state.selected_years}")
st.write(f"selected_countries: {len(st.session_state.selected_countries)} pays")
st.write(f"selected_productlines: {len(st.session_state.selected_productlines)} gammes")

# Section 2: Filtres interactifs
st.header("2. FILTRES INTERACTIFS")

col1, col2, col3 = st.columns(3)

with col1:
    new_years = st.multiselect("Années", sorted(df['Année'].unique()), default=st.session_state.selected_years, key="debug_years")

with col2:
    new_countries = st.multiselect("Pays", sorted(df['Pays'].unique()), default=st.session_state.selected_countries, key="debug_countries")

with col3:
    new_productlines = st.multiselect("Gammes", sorted(df['Gamme_de_Produits'].unique()), default=st.session_state.selected_productlines, key="debug_productlines")

# Bouton d'application
if st.button("🔄 APPLIQUER LES FILTRES"):
    st.session_state.selected_years = new_years
    st.session_state.selected_countries = new_countries
    st.session_state.selected_productlines = new_productlines
    st.rerun()

# Section 3: Application des filtres
st.header("3. APPLICATION DES FILTRES")

# Filtrer les données
df_filtered = df[
    df['Année'].isin(st.session_state.selected_years) &
    df['Pays'].isin(st.session_state.selected_countries) &
    df['Gamme_de_Produits'].isin(st.session_state.selected_productlines)
]

st.write(f"Lignes originales: {len(df)}")
st.write(f"Lignes filtrées: {len(df_filtered)}")

# Section 4: Calcul des KPIs avec données filtrées
st.header("4. KPIs AVEC DONNÉES FILTRÉES")

if not df_filtered.empty:
    ca_total = df_filtered["Chiffre d'Affaires"].sum()
    total_commandes = df_filtered['Numéro_Commande'].nunique()
    panier_moyen = ca_total / total_commandes if total_commandes > 0 else 0
    
    st.metric("CA TOTAL FILTRÉ", f"{ca_total:,.0f} €")
    st.metric("NOMBRE DE COMMANDES FILTRÉ", f"{total_commandes:,}")
    st.metric("PANIER MOYEN FILTRÉ", f"{panier_moyen:,.0f} €")
    
    # Test de concentration
    if ca_total > 0:
        part_classic = (df_filtered[df_filtered['Gamme_de_Produits'] == 'Classic Cars']["Chiffre d'Affaires"].sum() / ca_total) * 100
        st.metric("PART CLASSIC CARS FILTRÉE", f"{part_classic:.1f}%")
else:
    st.warning("Aucune donnée filtrée")

# Section 5: Test de réactivité
st.header("5. TEST DE RÉACTIVITÉ")
st.info("Changez les filtres et cliquez sur 'Appliquer'. Les KPIs ci-dessus doivent changer immédiatement.")