#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 3: Preprocesamiento y Limpieza de Datos

Objetivo:
- Auditoría rigurosa y resolución técnica de nulos, inconsistencias y datos atípicos.
- Generar el dataset limpio y preprocesado: 1-datamart-limpio.csv
- Generar un dataset complementario de anomalías extremas aisladas para contraste minero: 2-partidos-outliers-extremos.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATAMART_PATH = BASE_DIR / "Fase-2" / "1-datamart-partidos.csv"
CLEAN_DATAMART_PATH = SCRIPT_DIR / "1-datamart-limpio.csv"
OUTLIERS_PATH = SCRIPT_DIR / "2-partidos-outliers-extremos.csv"

def preprocess_data():
    print("[1/5] Cargando Data Mart de Fase 2...")
    df = pd.read_csv(DATAMART_PATH)
    initial_rows = len(df)
    print(f"  - Filas iniciales: {initial_rows:,}")

    # ==========================================================
    # 1. TRATAMIENTO DE NULOS Y CONSISTENCIA
    # ==========================================================
    print("[2/5] Aplicando reglas de tratamiento de nulos y consistencia...")
    
    # first_shooter: 414 nulos en penales -> Asignar categoría explícita 'Not_Recorded'
    df["shootout_first_shooter"] = df["shootout_first_shooter"].fillna("Not_Recorded")
    
    # shootout_winner: nulo si no hubo penales -> Asignar 'None'
    df["shootout_winner"] = df["shootout_winner"].fillna("None")

    # Normalización de caracteres y textos (strip de espacios invisibles)
    text_cols = ["home_team", "away_team", "tournament", "city", "country"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # ==========================================================
    # 2. IDENTIFICACIÓN ESTADÍSTICA DE OUTLIERS (GOLEADAS EXTREMAS)
    # ==========================================================
    print("[3/5] Evaluando datos atípicos (outliers) en total_goals...")
    q1 = df["total_goals"].quantile(0.25)
    q3 = df["total_goals"].quantile(0.75)
    iqr = q3 - q1
    mild_threshold = q3 + 1.5 * iqr    # 8.5 goles
    extreme_threshold = q3 + 3.0 * iqr # 13.0 goles

    # Banderas de auditoría técnica
    df["is_outlier_mild"] = df["total_goals"] > mild_threshold
    df["is_outlier_extreme"] = df["total_goals"] > extreme_threshold

    mild_count = df["is_outlier_mild"].sum()
    extreme_count = df["is_outlier_extreme"].sum()
    print(f"  - Outliers leves (> {mild_threshold} goles): {mild_count} ({mild_count/initial_rows*100:.2f}%)")
    print(f"  - Outliers extremos (> {extreme_threshold} goles): {extreme_count} ({extreme_count/initial_rows*100:.2f}%)")

    # ==========================================================
    # 3. EXPORTACIÓN DE DATASETS LIMPIOS Y DE AUDITORÍA
    # ==========================================================
    print("[4/5] Separando dataset de outliers extremos para análisis de contraste...")
    outliers_df = df[df["is_outlier_extreme"]].copy()
    outliers_df.to_csv(OUTLIERS_PATH, index=False)
    print(f"  - Guardado subconjunto de outliers extremos en: {OUTLIERS_PATH}")

    # Dataset limpio consolidado (mantiene el corpus íntegro con flags para filtrado selectivo según el algoritmo de Fase 6)
    print(f"[5/5] Exportando dataset limpio a {CLEAN_DATAMART_PATH}...")
    df.to_csv(CLEAN_DATAMART_PATH, index=False)
    print(f"✅ ¡Preprocesamiento completado con éxito! {len(df):,} filas exportadas.")

if __name__ == "__main__":
    preprocess_data()
