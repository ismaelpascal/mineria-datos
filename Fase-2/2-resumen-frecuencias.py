#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 2.
Muestra las tablas de frecuencias, conteos, porcentajes y barras de histograma
para las columnas clave del archivo: 1-datamart-partidos.csv.

Muestra como máximo los 5 primeros resultados por tabla.
"""

from pathlib import Path
import pandas as pd

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
DATAMART_PATH = SCRIPT_DIR / "1-datamart-partidos.csv"

def print_visidata_style(df: pd.DataFrame, col_name: str, title: str, top_n: int = 5):
    total = len(df)
    counts = df[col_name].value_counts(dropna=False).head(top_n)
    
    print("\n" + "=" * 70)
    print(f"📊 TABLA RELEVANTE: {col_name} ({title})")
    print(f"📁 Archivo origen: 1-datamart-partidos.csv (Total filas: {total:,})")
    print(f"💡 Para ver el histograma interactivo en VisiData:")
    print(f"   1. Abre: vd Fase-2/1-datamart-partidos.csv")
    print(f"   2. Sitúate en la columna '{col_name}' y presiona Shift + F")
    print("-" * 70)
    print(f"{'VALOR':<25} | {'COUNT':>8} | {'PERCENT %':>10} | HISTOGRAMA")
    print("-" * 70)
    
    max_count = counts.iloc[0] if len(counts) > 0 else 1
    for val, count in counts.items():
        pct = (count / total) * 100
        val_str = str(val)[:24]
        # Barra gráfica proporcional de hasta 20 caracteres estilo VisiData
        bar_len = int((count / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_len
        print(f"{val_str:<25} | {count:>8,d} | {pct:>9.2f}% | {bar}")
    print("=" * 70)

def main():
    if not DATAMART_PATH.exists():
        print(f"❌ Error: No se encontró {DATAMART_PATH}. Ejecuta primero ./construir-datamart.py")
        return

    df = pd.read_csv(DATAMART_PATH)

    # 1. match_outcome
    print_visidata_style(df, "match_outcome", "Distribución de Resultados (Victoria Local, Empate, Visitante)", top_n=5)

    # 2. tournament
    print_visidata_style(df, "tournament", "Torneos más Frecuentes", top_n=5)

    # 3. home_score
    print_visidata_style(df, "home_score", "Distribución de Goles del Equipo Local", top_n=5)

    # 4. total_goals
    print_visidata_style(df, "total_goals", "Distribución de Goles Totales por Partido", top_n=5)

    # 5. neutral
    print_visidata_style(df, "neutral", "Condición de Cancha Neutral", top_n=5)

    # 6. has_penalty_shootout
    print_visidata_style(df, "has_penalty_shootout", "Definición por Tanda de Penales", top_n=5)

if __name__ == "__main__":
    main()
