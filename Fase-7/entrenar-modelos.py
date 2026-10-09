#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 7: Minería de Datos (Entrenamiento y Ejecución de Modelos)

Objetivos:
1. Tarea Predictiva (Clasificación Supervisada Tri-clase):
   - Partición estricta 80% Train y 20% Test (estratificada por match_outcome) para evitar overfitting.
   - Entrenar Modelo 1: Decision Tree (Árbol de Decisión).
   - Entrenar Modelo 2: Gaussian Naive Bayes.
   - Generar predicciones y probabilidades sobre el Test set no visto.
   - Exportar archivo: 1-predicciones-clasificacion.csv

2. Tarea Descriptiva (Clustering No Supervisado con K-Means):
   - Tomar los 78 torneos representativos de Fase 5.
   - Estandarización de características numéricas con Z-Score (StandardScaler).
   - Entrenar K-Means con K=3 clústeres.
   - Asignar etiquetas de clúster e interpretar los centroides arquetípicos.
   - Exportar archivo: 2-clusters-torneos.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
MATRIX_PATH = BASE_DIR / "Fase-4" / "2-matriz-mineria.csv"
CLEAN_DATAMART_PATH = BASE_DIR / "Fase-3" / "1-datamart-limpio.csv"
DESCRIPTIVE_PATH = BASE_DIR / "Fase-5" / "1-dataset-descriptivo-torneos.csv"

OUTPUT_PRED_CSV = SCRIPT_DIR / "1-predicciones-clasificacion.csv"
OUTPUT_CLUSTERS_CSV = SCRIPT_DIR / "2-clusters-torneos.csv"

def train_and_execute_mining():
    print("=" * 70)
    print("🚀 EJECUCIÓN DE MINERÍA DE DATOS - FASE 7")
    print("=" * 70)

    # ==========================================================
    # PARTE 1: TAREA PREDICTIVA (CLASIFICACIÓN SUPERVISADA)
    # ==========================================================
    print("\n[1/4] Cargando datos y aplicando partición estricta Train / Test (80/20)...")
    matrix = pd.read_csv(MATRIX_PATH)
    clean_meta = pd.read_csv(CLEAN_DATAMART_PATH)[["match_id", "date", "home_team", "away_team", "tournament"]]

    # Features ex-ante (condiciones contextuales antes de iniciar el partido)
    forbidden_leakage = [
        "match_id", "match_outcome", "home_score", "away_score", "total_goals",
        "goal_difference", "abs_goal_diff", "goals_first_half", "goals_second_half",
        "penalty_goals", "has_scorer_details"
    ]
    feature_cols = [c for c in matrix.columns if c not in forbidden_leakage]
    
    X = matrix[feature_cols]
    y = matrix["match_outcome"]
    ids = matrix["match_id"]

    # Partición estratificada 80% Train, 20% Test
    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        X, y, ids, test_size=0.20, random_state=42, stratify=y
    )

    print(f"  - Total datos: {len(X):,} partidos")
    print(f"  - Conjunto de Entrenamiento (Train 80%): {len(X_train):,} registros")
    print(f"  - Conjunto de Prueba no visto (Test 20%): {len(X_test):,} registros")

    # Entrenamiento Modelo 1: Árbol de Decisión
    print("[2/4] Entrenando Modelo 1: Árbol de Decisión (CART)...")
    dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, random_state=42)
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    y_proba_dt = dt.predict_proba(X_test)

    # Entrenamiento Modelo 2: Gaussian Naive Bayes
    print("[2/4] Entrenando Modelo 2: Gaussian Naive Bayes...")
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    y_pred_gnb = gnb.predict(X_test)
    y_proba_gnb = gnb.predict_proba(X_test)

    # Consolidar resultados del conjunto de prueba
    classes = list(dt.classes_)
    test_results = pd.DataFrame({
        "match_id": ids_test,
        "actual_outcome": y_test,
        "pred_decision_tree": y_pred_dt,
        "pred_naive_bayes": y_pred_gnb,
    })
    # Añadir probabilidades
    for idx, c in enumerate(classes):
        test_results[f"proba_dt_{c}"] = y_proba_dt[:, idx].round(3)
        test_results[f"proba_gnb_{c}"] = y_proba_gnb[:, idx].round(3)

    # Enriquecer con metadatos del partido para interpretabilidad
    test_results = pd.merge(test_results, clean_meta, on="match_id", how="left")
    
    # Reordenar columnas clave
    cols_order = [
        "match_id", "date", "home_team", "away_team", "tournament",
        "actual_outcome", "pred_decision_tree", "pred_naive_bayes",
        "proba_dt_HOME_WIN", "proba_dt_DRAW", "proba_dt_AWAY_WIN",
        "proba_gnb_HOME_WIN", "proba_gnb_DRAW", "proba_gnb_AWAY_WIN"
    ]
    test_results = test_results[cols_order]
    test_results.to_csv(OUTPUT_PRED_CSV, index=False)
    print(f"  - ✅ Archivo exportado: {OUTPUT_PRED_CSV} ({len(test_results):,} filas)")

    # ==========================================================
    # PARTE 2: TAREA DESCRIPTIVA (CLUSTERING CON K-MEANS)
    # ==========================================================
    print("\n[3/4] Ejecutando Clustering No Supervisado (K-Means) sobre 78 torneos...")
    tourneys = pd.read_csv(DESCRIPTIVE_PATH)
    cluster_features = [
        "avg_goals", "std_goals", "home_win_rate", "draw_rate",
        "away_win_rate", "penalty_shootout_rate", "neutral_rate"
    ]

    scaler = StandardScaler()
    X_cluster_scaled = scaler.fit_transform(tourneys[cluster_features])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=15)
    tourneys["cluster_id"] = kmeans.fit_predict(X_cluster_scaled)

    # Asignar nombres semánticos de negocio a los clústeres según sus centroides
    cluster_centers = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=cluster_features)
    cluster_names = {}
    for c_id, row in cluster_centers.iterrows():
        if row["avg_goals"] > 4.5:
            cluster_names[c_id] = "Torneos_Hiper_Goleadores"
        elif row["penalty_shootout_rate"] > 0.08:
            cluster_names[c_id] = "Torneos_Tácticos_Penales"
        else:
            cluster_names[c_id] = "Torneos_Competitivos_Regulares"

    tourneys["cluster_profile"] = tourneys["cluster_id"].map(cluster_names)
    tourneys.sort_values(by=["cluster_id", "total_matches"], ascending=[True, False], inplace=True)
    tourneys.to_csv(OUTPUT_CLUSTERS_CSV, index=False)
    print(f"  - ✅ Archivo exportado: {OUTPUT_CLUSTERS_CSV} ({len(tourneys)} torneos asignados)")

    print("\n[4/4] ✅ ¡Minería de datos de la Fase 7 finalizada con éxito!")

if __name__ == "__main__":
    train_and_execute_mining()
