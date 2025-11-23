# 📊 Dashboard d'Analyse des Ventes 2003-2005

Application web interactive conçue pour explorer, analyser et visualiser les données de ventes sur 3 années (2003-2005).
Cette application démontre la capacité à construire une solution analytique complète intégrant manipulation de données, architecture modulaire et visualisation interactive.

## 🎯 Objectifs de l'Application

Cette application permet aux analystes métier et aux décideurs de :

- **Explorer les tendances** : Identifier les patterns de ventes sur des périodes spécifiques et déterminer les saisons clés
- **Analyser la géographie** : Comparer les performances commerciales par région et identifier les marchés prometteurs
- **Segmenter les clients** : Classifier les comportements d'achat et identifier les profils clients prioritaires
- **Optimiser le portefeuille produits** : Évaluer la performance individuelle de chaque produit et les combinaisons de vente
- **Déceler les comportements** : Découvrir les patterns d'achat et les corrélations entre variables
- **Suivre les KPIs** : Disposer d'une vue synthétique des métriques clés en temps réel

## 🏗️ Architecture Technique

### Stack Technologique

| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Framework Web** | Streamlit 1.28.0 | Interface interactive et responsive |
| **Manipulation Données** | Pandas 2.1.0 | ETL, transformation et agrégation des données |
| **Calculs Numériques** | NumPy 1.24.0 | Opérations mathématiques et statistiques |
| **Visualisation** | Plotly 5.15.0 | Graphiques interactifs et exploratoires |

### Design Modulaire

L'application est organisée en **4 couches** :

1. **Composants UI** (`components/`) - Éléments réutilisables (cartes KPI, graphiques, sidebar)
2. **Onglets d'Analyse** (`tabs/`) - 6 modules analytiques indépendants
3. **Utilitaires Métier** (`utils/`) - Logique de chargement, filtrage et gestion d'état
4. **Configuration** (`config.py`) - Paramétrage centralisé## 📁 Structure du Projet

```text
dashboard_project/
├── app.py                          # Application principale
├── config.py                       # Configuration de l'application
├── requirements.txt                # Dépendances
├── debug_app.py                    # Utilitaire de débogage
│
├── components/                     # Composants réutilisables
│   ├── charts.py                   # Graphiques
│   ├── kpi_cards.py               # Cartes KPI
│   └── sidebar.py                  # Barre latérale avec filtres
│
├── data/                           # Données
│   └── sales_data_cleaned.csv      # Dataset principal
│
├── tabs/                           # Onglets de l'application
│   ├── global_performance.py       # KPIs et métriques globales
│   ├── temporal_analysis.py        # Analyse temporelle
│   ├── geographic_analysis.py      # Analyse géographique
│   ├── customer_segmentation.py    # Segmentation clients
│   ├── product_performance.py      # Performance des produits
│   └── behavior_analysis.py        # Comportements d'achat
│
└── utils/                          # Utilitaires
    ├── data_loader.py              # Chargement et validation des données
    ├── filters.py                  # Gestion des filtres
    └── session_manager.py          # Gestion de l'état de session
```

## 📊 Capacités Analytiques

### 6 Modules d'Analyse Complets

#### 1. **Performance Globale**

- Dashboard KPI synthétique : CA total, nombre de transactions, panier moyen
- Tendances générales et métriques d'efficacité
- Indicateurs de performance clés en temps réel

#### 2. **Analyse Temporelle**

- Série chronologique des ventes (jour/mois/année)
- Détection des patterns saisonniers
- Évolution des tendances avec comparaisons périodiques

#### 3. **Analyse Géographique**

- Répartition des ventes par région/pays
- Heatmaps de performance géographique
- Identification des zones de croissance et déclin

#### 4. **Segmentation Client**

- Classification automatique des profils clients
- Analyse RFM (Récence, Fréquence, Montant)
- Comportements et valeur client

#### 5. **Performance Produits**

- Analyse du portefeuille produits
- Identification des best-sellers et produits en déclin
- Correlations entre produits et zones géographiques

#### 6. **Analyse Comportementale**

- Patterns d'achat et comportements clients
- Corrélations entre variables
- Insights exploratoires

### Système de Filtrage Intégré

- Filtres multi-critères applicables globalement
- Mise à jour en temps réel des visualisations
- Gestion d'état session pour persistance utilisateur

## 🛠️ Implémentation Technique

### Points Forts de l'Architecture

- **Séparation des responsabilités** : Couche UI, logique métier et utilitaires clairement délimitées
- **Réutilisabilité** : Composants modulaires (cartes KPI, graphiques) utilisables across modules
- **Performance** : Système de cache (TTL 1h) pour optimiser les rechargements de données
- **State Management** : Gestion d'état session Streamlit pour expérience utilisateur fluide
- **Validation** : Pipeline complet de validation des données à chaque étape

### Flux de Données

```text
Données Brutes (CSV)
    ↓
[data_loader.py] - Chargement et validation
    ↓
[filters.py] - Application des critères de filtrage
    ↓
[session_manager.py] - Gestion d'état utilisateur
    ↓
[Components & Tabs] - Visualisation interactive
```

## 📈 Cas d'Usage

Cette application est adaptée pour :

- **Analystes BI/Data** : Exploration autonome des données sans dépendre d'une équipe IT
- **Responsables Ventes** : Suivi des performances commerciales et identification des opportunités
- **Direction Générale** : Vue d'ensemble stratégique et dashboarding exécutif
- **Data Scientists** : Prototypage rapide et validation d'hypothèses analytiques

## 🎓 Compétences Démontrées

- ✅ Python avancé (Pandas, NumPy)
- ✅ Développement d'applications web interactives (Streamlit)
- ✅ Conception d'architectures modulaires et maintenables
- ✅ Visualisation de données (Plotly)
- ✅ Data pipeline et ETL
- ✅ Gestion d'état et optimisation des performances
- ✅ Analyse de données exploratoires (EDA)
- ✅ Best practices de code (organisation, documentation, validation)

## 📁 Structure Complète du Projet

```text
dashboard_project/
├── app.py                          # Point d'entrée principal
├── config.py                       # Configuration centralisée
├── requirements.txt                # Dépendances
├── debug_app.py                    # Outils de débogage
│
├── components/                     # Composants UI réutilisables
│   ├── charts.py                   # Graphiques réutilisables
│   ├── kpi_cards.py               # Cartes KPI
│   └── sidebar.py                  # Barre latérale et filtres
│
├── data/                           # Dataset (2003-2005)
│   └── sales_data_cleaned.csv
│
├── tabs/                           # Modules analytiques
│   ├── global_performance.py
│   ├── temporal_analysis.py
│   ├── geographic_analysis.py
│   ├── customer_segmentation.py
│   ├── product_performance.py
│   └── behavior_analysis.py
│
└── utils/                          # Utilitaires techniques
    ├── data_loader.py
    ├── filters.py
    └── session_manager.py
```

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

L'application se lancera sur `http://localhost:8501`

## 👨‍💻 À Propos

Ce projet démontre la capacité à concevoir une solution analytique production-ready intégrant données, architecture logicielle et expérience utilisateur.

---
