# 🏭 OCP Slurry Pipeline — Predictive Maintenance Platform

<div align="center">

![Phase 1](https://img.shields.io/badge/Phase%201-Complete-brightgreen?style=for-the-badge)
![Phase 2](https://img.shields.io/badge/Phase%202-In%20Progress-yellow?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Azure](https://img.shields.io/badge/Azure-ADLS%20Gen2-0078D4?style=for-the-badge&logo=microsoftazure)
![Databricks](https://img.shields.io/badge/Databricks-Spark%204.1-FF3621?style=for-the-badge&logo=databricks)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker)

**Plateforme de maintenance prédictive pour le pipeline slurry OCP Khouribga — Jorf Lasfar (235 km)**

*Prédiction des pannes 24–48h à l'avance · Stack Azure Enterprise · Lakehouse Medallion*

[Architecture](#architecture) • [Dataset](#dataset) • [Stack](#stack-technique) • [Progression](#progression) • [Lancer](#lancer-le-projet)

</div>

---

## Contexte Industriel

Le **Slurry Pipeline OCP** transporte un mélange eau + phosphate broyé sur 235 km entre Khouribga et Jorf Lasfar, via **8 stations de pompage** équipées de ~1 200 capteurs (pression, débit, température, vibrations, pH).

| Paramètre | Valeur |
|---|---|
| Longueur | 235 km |
| Débit nominal | 8 500 – 9 200 m³/h |
| Capteurs actifs | ~1 200 tags IoT |
| Coût panne non prévue | Plusieurs millions MAD/jour |
| **Objectif** | **Prédire les pannes 24–48h à l'avance** |

---

## Architecture

![Architecture Lakehouse](docs/architecture.png)

### Lakehouse Medallion — Bronze → Silver → Gold

```
[Kaggle Dataset]
      │
      ▼  upload_bronze.py (azure-storage SDK)
[ADLS Gen2 · datalakeocp2026 · swedencentral]
      │
      ├── bronse/sensors_raw/     ← Bronze : données brutes CSV
      ├── silver/                 ← Silver : données nettoyées Delta Lake
      └── gold/                   ← Gold : Star Schema Power BI
      │
      ▼  Databricks Spark 4.1
[Notebook 01_bronze_silver.ipynb]  → Nettoyage + Feature Engineering
[Notebook 02_silver_gold.ipynb]    → Star Schema + Data Marts
      │
      ▼  Azure Data Factory (trigger 02h00/nuit)
[FACT_SENSOR_EVENTS + DIM_STATION + DIM_EQUIPMENT + DIM_DATE]
      │
      ├──▶ [MLflow + XGBoost]  → API FastAPI + Docker + Azure ML
      └──▶ [Power BI Service]  → Dashboard 3 profils + RLS
```

---

## Dataset

| Dataset | Source | Lignes | Description |
|---|---|---|---|
| **AI4I 2020 Predictive Maintenance** | Kaggle | 10 000 | Capteurs industriels réels : température, RPM, torque, usure outil. Label panne inclus. |
| **Predictive Maintenance v3** | Kaggle | ~50 000 | Dataset complémentaire multi-capteurs avec anomalies étiquetées |

### Correspondance Colonnes → Nomenclature OCP

| Colonne Kaggle | Nom OCP Projet | Unité | Description |
|---|---|---|---|
| `Air temperature [K]` | `temperature_air` | K | Température ambiante |
| `Process temperature [K]` | `temperature_process` | K | Température process |
| `Rotational speed [rpm]` | `rotational_speed` | RPM | Vitesse rotation pompe |
| `Torque [Nm]` | `torque` | Nm | Couple mécanique |
| `Tool wear [min]` | `tool_wear` | min | Usure outil (proxy vibrations) |
| `Machine failure` | `label_panne` | 0/1 | **Cible ML** : 0=normal, 1=panne |

---

## Stack Technique

| Outil | Rôle | Pourquoi |
|---|---|---|
| **Azure ADLS Gen2** | Stockage Bronze/Silver/Gold | Standard Microsoft Big Data industriel |
| **Databricks Spark 4.1** | Transformation ETL + ML | Plateforme n°1 Data Engineering en entreprise |
| **Delta Lake** | Format stockage ACID | Transactions, Time Travel, Schema Evolution |
| **Azure Data Factory** | Orchestration pipeline | Trigger automatique 02h00 chaque nuit |
| **XGBoost + MLflow** | ML + Tracking expériences | F1 > 0.85 · AUC > 0.92 |
| **FastAPI + Docker** | API prédiction REST | POST /predict → probabilité panne < 200ms |
| **Azure ML** | Déploiement endpoint | Managed Online Endpoint production |
| **Power BI Service** | Dashboard + RLS | 3 profils : DG · Analyste · Data Scientist |
| **GitHub Actions** | CI/CD | Push → Tests → Rebuild → Redéploiement |

---

## Structure du Projet

```
ocp-slurry-pipeline/
│
├── README.md                        # Ce fichier
├── requirements.txt                 # Dépendances Python
├── generate_architecture.py         # Génère docs/architecture.png
│
├── Data/                            # Datasets bruts (gitignored)
│   ├── ai4i2020.csv
│   └── predictive_maintenance_v3.csv
│
├── infa/                            # Scripts infrastructure
│   └── upload_bronze.py             # Upload ADLS Gen2 sécurisé
│
├── notebooks/                       # Databricks notebooks exportés
│   ├── 01_bronze_silver.ipynb       # ETL nettoyage PySpark
│   ├── 02_silver_gold.ipynb         # Star Schema Gold
│   └── 03_eda_exploration.ipynb     # Analyse exploratoire
│
├── ml/                              # Machine Learning
│   ├── train.py                     # Entraînement XGBoost + MLflow
│   ├── evaluate.py                  # Évaluation modèles
│   ├── api/
│   │   └── app.py                   # FastAPI endpoint /predict
│   └── Dockerfile                   # Conteneurisation modèle
│
├── powerbi/
│   └── ocp_slurry_dashboard.pbix    # Dashboard Power BI
│
├── docs/
│   ├── architecture.png             # Schéma Lakehouse
│   ├── DATA_DICTIONARY.md           # Dictionnaire de données
│   ├── ADF_PIPELINE.md              # Documentation ADF
│   └── POWERBI_RLS.md               # Documentation RLS 3 profils
│
└── .github/
    └── workflows/
        └── retrain.yml              # CI/CD GitHub Actions
```

---

## Progression

| Phase | Métier | Statut | Livrables |
|---|---|---|---|
| **Phase 1** — Azure Setup + Bronze | Cloud / MLOps | ✅ **Terminé** | ADLS Gen2 · Databricks · données chargées |
| **Phase 2a** — Bronze → Silver | Data Analyst | 🔄 En cours | Notebook nettoyage PySpark |
| **Phase 2b** — Gold + ADF | Data Analyst | ⏳ À faire | Star Schema · pipeline auto |
| **Phase 3a** — ML + MLflow | Data Scientist | ⏳ À faire | 4 modèles · F1 > 0.85 |
| **Phase 3b** — FastAPI + Docker | Data Scientist + Cloud | ⏳ À faire | API déployée · badge CI/CD vert |
| **Phase 4** — Power BI + RLS | Data Analyst | ⏳ À faire | Dashboard 3 profils publié |
| **Portfolio** — README + LinkedIn | Tous | ⏳ À faire | Repo public · article publié |

### Métriques Cibles

| Modèle | Métrique | Cible |
|---|---|---|
| XGBoost Panne J+1 | F1-Score | > 0.85 |
| XGBoost Panne J+1 | AUC-ROC | > 0.92 |
| Isolation Forest Anomalies | Précision | > 88% |
| Prophet Débit | MAPE | < 8% |
| API /predict | Latence | < 200ms |

---

## Lancer le Projet

### Prérequis

```bash
pip install azure-storage-file-datalake azure-identity pandas pyarrow matplotlib
az login
```

### 1. Upload des données Bronze

```bash
cd infa/
python upload_bronze.py
```

### 2. Générer le schéma d'architecture

```bash
python generate_architecture.py
# → docs/architecture.png
```

### 3. Notebooks Databricks

Importer dans Databricks Community Edition :
- `notebooks/01_bronze_silver.ipynb`
- `notebooks/02_silver_gold.ipynb`

### 4. Lancer l'API localement (Phase 3)

```bash
docker build -t ocp-predictor:v1.0 ./ml/
docker run -p 8000:8000 ocp-predictor:v1.0
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 308.6, "rpm": 1551, "torque": 42.8, "tool_wear": 0}'
```

---

## Compétences Démontrées

Ce projet couvre les compétences les plus demandées en Data Engineering / Data Science au Maroc en 2026 :

- **Cloud Azure** — ADLS Gen2, ADF, Azure ML, Key Vault, IAM
- **Data Engineering** — PySpark, Delta Lake, Medallion Architecture, ETL
- **Machine Learning** — XGBoost, Isolation Forest, Prophet, SMOTE, split temporel
- **MLOps** — MLflow, Docker, FastAPI, GitHub Actions CI/CD
- **Business Intelligence** — Power BI, DAX, RLS, Star Schema
- **Gouvernance** — Data Lineage, Data Dictionary, SLA Qualité

---

## Auteur

**Meriem Merbouhi** — data engineer
Projet Portfolio · OCP Slurry Pipeline Predictive Maintenance · 2026

---

*Ce projet démontre la maîtrise d'une stack Data Enterprise complète,  
de l'ingestion cloud jusqu'au dashboard décisionnel sécurisé,  
en passant par le Machine Learning et le MLOps.*#   o c p - s l u r r y - p i p e l i n e  
 