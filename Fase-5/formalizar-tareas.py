#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 5: Formalización y Preparación de Tareas de Minería de Datos

Objetivo:
- Formalizar técnicamente las dos tareas analíticas requeridas en KDD:
  1. Tarea Predictiva: Clasificación Supervisada Multiclase
     * Target: match_outcome ∈ {HOME_WIN, DRAW, AWAY_WIN}
     * Variables predictoras ex-ante (sin data leakage del transcurso del partido)
  2. Tarea Descriptiva: Segmentación y Agrupamiento No Supervisado (Clustering)
     * Entidad: Torneos y Eras históricas representativas
     * Variables de caracterización: promedio de goles, paridad, tasa de penales, ventaja de localía
- Generar el dataset analítico descriptivo a nivel de torneos:
  * 1-dataset-descriptivo-torneos.csv (para clustering en Fases 6 y 7)
"""

from pathlib import Path
import pandas as pd
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
INPUT_TRANSFORMED = BASE_DIR / "Fase-4" / "1-dataset-transformado.csv"
OUTPUT_DESCRIPTIVE_CSV = SCRIPT_DIR / "1-dataset-descriptivo-torneos.csv"

def formalize_mining_tasks():
    print("[1/3] Cargando dataset maestro transformado de Fase 4...")
    df = pd.read_csv(INPUT_TRANSFORMED)
    print(f"  - Partidos disponibles: {len(df):,}")

    # ==========================================================
    # 1. GENERACIÓN DEL DATASET DESCRIPTIVO A NIVEL TORNEO (CLUSTERING)
    # ==========================================================
    print("[2/3] Agregando métricas a nivel de torneo para Clustering descriptivo...")
    
    # Agrupamos por torneo (filtrando torneos con muestra representativa >= 30 partidos)
    tourney_stats = df.groupby("tournament").agg(
        total_matches=("match_id", "count"),
        avg_goals=("total_goals", "mean"),
        std_goals=("total_goals", "std"),
        home_win_rate=("match_outcome", lambda s: (s == "HOME_WIN").mean()),
        draw_rate=("match_outcome", lambda s: (s == "DRAW").mean()),
        away_win_rate=("match_outcome", lambda s: (s == "AWAY_WIN").mean()),
        penalty_shootout_rate=("has_penalty_shootout", lambda s: s.mean()),
        neutral_rate=("neutral", lambda s: s.mean()),
        intercontinental_rate=("is_intercontinental", lambda s: s.mean())
    ).reset_index()

    # Rellenar std_goals con 0 si hubiera un solo partido (aunque filtramos >= 30)
    tourney_stats["std_goals"] = tourney_stats["std_goals"].fillna(0)

    # Filtrar torneos representativos para un clustering estadísticamente robusto
    tourney_rep = tourney_stats[tourney_stats["total_matches"] >= 30].copy()
    tourney_rep.sort_values(by="total_matches", ascending=False, inplace=True)

    print(f"  - Torneos totales: {len(tourney_stats)} | Torneos representativos (>=30 partidos): {len(tourney_rep)}")
    tourney_rep.to_csv(OUTPUT_DESCRIPTIVE_CSV, index=False)
    print(f"  - Dataset descriptivo guardado en: {OUTPUT_DESCRIPTIVE_CSV}")

    print("[3/3] ✅ Formalización de tareas completada con éxito.")

if __name__ == "__main__":
    formalize_mining_tasks()
