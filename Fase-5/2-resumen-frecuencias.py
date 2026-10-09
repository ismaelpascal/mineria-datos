#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 5.
Muestra las tablas de frecuencias, promedios y rankings top 5 del archivo:
1-dataset-descriptivo-torneos.csv:
- Torneos con mayor cantidad de partidos
- Torneos con mayor promedio de gol
- Torneos con mayor tasa de definiciones por penales
- Torneos con mayor ventaja de localía (home_win_rate)
- Torneos con mayor tasa de empates (draw_rate)

Muestra como máximo los 5 primeros resultados por tabla.
"""

from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DESCRIPTIVE_PATH = SCRIPT_DIR / "1-dataset-descriptivo-torneos.csv"

def print_top_table(df: pd.DataFrame, sort_col: str, title: str, display_cols: list, ascending: bool = False, top_n: int = 5):
    sub = df.sort_values(by=sort_col, ascending=ascending).head(top_n)
    
    print("\n" + "=" * 80)
    print(f"📊 TABLA RELEVANTE: {sort_col} ({title})")
    print(f"📁 Archivo origen: 1-dataset-descriptivo-torneos.csv (Total torneos analizados: {len(df)})")
    print(f"💡 Para ver y ordenar en VisiData:")
    print(f"   1. Abre: vd Fase-5/1-dataset-descriptivo-torneos.csv")
    print(f"   2. Sitúate en la columna '{sort_col}', presiona '#' (entero) o '%' (decimal) y luego ']' para ordenar")
    print("-" * 80)
    
    header = f"{'TORNEO':<35} | " + " | ".join([f"{c:>12}" for c in display_cols])
    print(header)
    print("-" * 80)
    
    for _, r in sub.iterrows():
        t_name = str(r["tournament"])[:34]
        vals = []
        for c in display_cols:
            val = r[c]
            if isinstance(val, (float, int)):
                if "rate" in c:
                    vals.append(f"{val*100:>11.1f}%")
                elif "avg" in c:
                    vals.append(f"{val:>12.2f}")
                else:
                    vals.append(f"{int(val):>12,d}")
            else:
                vals.append(f"{str(val):>12}")
        print(f"{t_name:<35} | " + " | ".join(vals))
    print("=" * 80)

def main():
    if not DESCRIPTIVE_PATH.exists():
        print(f"❌ Error: No se encontró {DESCRIPTIVE_PATH}. Ejecuta primero ./formalizar-tareas.py")
        return

    df = pd.read_csv(DESCRIPTIVE_PATH)

    # 1. Torneos con mayor volumen
    print_top_table(df, "total_matches", "Torneos con Mayor Volumen de Partidos", ["total_matches", "avg_goals", "home_win_rate"], ascending=False)

    # 2. Torneos más goleadores
    print_top_table(df, "avg_goals", "Torneos con Mayor Promedio de Goles", ["avg_goals", "total_matches", "home_win_rate"], ascending=False)

    # 3. Torneos con más definiciones por penales
    print_top_table(df, "penalty_shootout_rate", "Torneos con Mayor Tasa de Penales (Shootouts)", ["penalty_shootout_rate", "draw_rate", "total_matches"], ascending=False)

    # 4. Torneos con mayor ventaja de localía
    print_top_table(df, "home_win_rate", "Torneos con Mayor Ventaja de Localía", ["home_win_rate", "draw_rate", "away_win_rate"], ascending=False)

    # 5. Torneos con mayor paridad (más empates)
    print_top_table(df, "draw_rate", "Torneos con Mayor Paridad y Empates", ["draw_rate", "avg_goals", "total_matches"], ascending=False)

if __name__ == "__main__":
    main()
