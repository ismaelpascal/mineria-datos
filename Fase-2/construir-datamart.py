#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 2: Construcción del Target Dataset (Data Mart Consolidado)

Objetivo:
- Integrar Match_Results.csv, Goal_Scorers.csv y Penalty_Shootouts.csv.
- Resolver la disparidad de granularidades:
    * Match_Results: 1 fila = 1 partido (granularidad partido)
    * Goal_Scorers: 1 fila = 1 gol individual (granularidad evento) -> agregamos a nivel partido
    * Penalty_Shootouts: 1 fila = 1 definición por penales -> agregamos a nivel partido
- Asignar una Clave Primaria Única Canónica (match_id).
- Producir el tablón analítico: 1-datamart-partidos.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Rutas absolutas dinámicas para poder ejecutar desde cualquier directorio
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
MATCHES_FILE = BASE_DIR / "Match_Results.csv"
SCORERS_FILE = BASE_DIR / "Goal_Scorers.csv"
PENALTIES_FILE = BASE_DIR / "Penalty_Shootouts.csv"
OUTPUT_FILE = SCRIPT_DIR / "1-datamart-partidos.csv"

def build_data_mart():
    print("[1/5] Cargando datasets crudos desde la raíz...")
    print(f"  - Match_Results: {MATCHES_FILE}")
    matches = pd.read_csv(MATCHES_FILE)
    scorers = pd.read_csv(SCORERS_FILE)
    penalties = pd.read_csv(PENALTIES_FILE)

    print(f"  - Matches crudos: {len(matches):,}")
    print(f"  - Goles crudos: {len(scorers):,}")
    print(f"  - Penales crudos: {len(penalties):,}")

    # 1. Desduplicación exacta de partidos en Match_Results (20 duplicados exactos detectados)
    matches = matches.drop_duplicates(subset=["date", "home_team", "away_team", "tournament"]).copy()
    matches.sort_values(by=["date", "home_team", "away_team"], inplace=True)
    matches.reset_index(drop=True, inplace=True)

    # 2. Generar Clave Primaria canónica (match_id)
    matches["match_id"] = [f"M_{i+1:06d}" for i in range(len(matches))]

    # 3. Agregación de Goal_Scorers a nivel de partido
    print("[2/5] Agregando Goal_Scorers a nivel de partido...")
    # Asegurar tipos booleanos
    scorers["own_goal"] = scorers["own_goal"].astype(str).str.upper() == "TRUE"
    scorers["penalty"] = scorers["penalty"].astype(str).str.upper() == "TRUE"

    # Clasificar temporalidad del gol
    scorers["goal_first_half"] = (scorers["minute"] <= 45).fillna(False)
    scorers["goal_second_half"] = ((scorers["minute"] > 45) & (scorers["minute"] <= 90)).fillna(False)
    scorers["goal_extra_time"] = (scorers["minute"] > 90).fillna(False)

    # Separar si el gol fue del local o del visitante
    scorers["is_home_goal"] = scorers["team"] == scorers["home_team"]
    scorers["is_away_goal"] = scorers["team"] == scorers["away_team"]

    # Métricas agregadas por partido
    agg_sc = scorers.groupby(["date", "home_team", "away_team"]).agg(
        total_recorded_goals=("team", "count"),
        home_recorded_goals=("is_home_goal", "sum"),
        away_recorded_goals=("is_away_goal", "sum"),
        penalty_goals=("penalty", "sum"),
        own_goals=("own_goal", "sum"),
        goals_first_half=("goal_first_half", "sum"),
        goals_second_half=("goal_second_half", "sum"),
        goals_extra_time=("goal_extra_time", "sum"),
        unique_scorers=("scorer", lambda s: s.dropna().nunique())
    ).reset_index()

    # 4. Procesamiento de Penalty_Shootouts
    print("[3/5] Procesando Penalty_Shootouts...")
    # Corregir discrepancias menores conocidas de nombres en penales para el join
    penalties_clean = penalties.copy()
    penalties_clean.loc[(penalties_clean["date"] == "2023-07-13") & (penalties_clean["home_team"] == "Åland"), "home_team"] = "Åland Islands"

    penalties_clean["has_penalty_shootout"] = True
    penalties_clean.rename(columns={
        "winner": "shootout_winner",
        "first_shooter": "shootout_first_shooter"
    }, inplace=True)

    # 5. Cruce de datos (LEFT JOIN desde matches hacia agregaciones)
    print("[4/5] Cruzando tablas en el Data Mart...")
    datamart = pd.merge(matches, agg_sc, on=["date", "home_team", "away_team"], how="left")
    datamart = pd.merge(datamart, penalties_clean, on=["date", "home_team", "away_team"], how="left")

    # Tratamiento de valores derivados del cruce
    datamart["has_penalty_shootout"] = datamart["has_penalty_shootout"].fillna(False)
    datamart["has_scorer_details"] = datamart["total_recorded_goals"].notna()

    # Imputar ceros en métricas de eventos cuando hay cobertura en Goal_Scorers
    metric_cols = [
        "total_recorded_goals", "home_recorded_goals", "away_recorded_goals",
        "penalty_goals", "own_goals", "goals_first_half", "goals_second_half",
        "goals_extra_time", "unique_scorers"
    ]
    for col in metric_cols:
        datamart[col] = datamart[col].fillna(0).astype(int)

    # Definir variables target básicas de negocio
    datamart["total_goals"] = datamart["home_score"] + datamart["away_score"]
    datamart["goal_difference"] = datamart["home_score"] - datamart["away_score"]

    # Target predictivo principal: resultado en 90 min
    conds = [
        datamart["home_score"] > datamart["away_score"],
        datamart["home_score"] == datamart["away_score"],
        datamart["home_score"] < datamart["away_score"]
    ]
    choices = ["HOME_WIN", "DRAW", "AWAY_WIN"]
    datamart["match_outcome"] = np.select(conds, choices, default="UNKNOWN")

    # Reordenar columnas lógicamente
    ordered_cols = [
        "match_id", "date", "home_team", "away_team",
        "home_score", "away_score", "total_goals", "goal_difference", "match_outcome",
        "tournament", "city", "country", "neutral",
        "has_scorer_details", "total_recorded_goals", "home_recorded_goals", "away_recorded_goals",
        "penalty_goals", "own_goals", "goals_first_half", "goals_second_half", "goals_extra_time", "unique_scorers",
        "has_penalty_shootout", "shootout_winner", "shootout_first_shooter"
    ]
    datamart = datamart[ordered_cols]

    print(f"[5/5] Exportando Data Mart consolidado a {OUTPUT_FILE}...")
    datamart.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ ¡Data Mart generado con éxito! Dimensiones: {datamart.shape[0]:,} filas x {datamart.shape[1]} columnas.")

if __name__ == "__main__":
    build_data_mart()
