#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 3.
Muestra las tablas de frecuencias de las columnas procesadas y de outliers:
- is_outlier_mild
- is_outlier_extreme
- shootout_first_shooter
- shootout_winner
- Top goleadas en 2-partidos-outliers-extremos.csv

Muestra como máximo los 5 primeros resultados por tabla.
"""

from pathlib import Path
import pandas as pd

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
CLEAN_DATAMART_PATH = SCRIPT_DIR / "1-datamart-limpio.csv"
OUTLIERS_PATH = SCRIPT_DIR / "2-partidos-outliers-extremos.csv"

def print_visidata_style(df: pd.DataFrame, col_name: str, title: str, source_file: str, top_n: int = 5):
    total = len(df)
    counts = df[col_name].value_counts(dropna=False).head(top_n)
    
    print("\n" + "=" * 70)
    print(f"📊 TABLA RELEVANTE: {col_name} ({title})")
    print(f"📁 Archivo origen: {source_file} (Total filas: {total:,})")
    print(f"💡 Para ver el histograma interactivo en VisiData:")
    print(f"   1. Abre: vd Fase-3/{source_file}")
    print(f"   2. Sitúate en la columna '{col_name}' y presiona Shift + F")
    print("-" * 70)
    print(f"{'VALOR':<25} | {'COUNT':>8} | {'PERCENT %':>10} | HISTOGRAMA")
    print("-" * 70)
    
    max_count = counts.iloc[0] if len(counts) > 0 else 1
    for val, count in counts.items():
        pct = (count / total) * 100
        val_str = str(val)[:24]
        bar_len = int((count / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_len
        print(f"{val_str:<25} | {count:>8,d} | {pct:>9.2f}% | {bar}")
    print("=" * 70)

def main():
    if not CLEAN_DATAMART_PATH.exists():
        print(f"❌ Error: No se encontró {CLEAN_DATAMART_PATH}. Ejecuta primero ./limpiar-datos.py")
        return

    df_clean = pd.read_csv(CLEAN_DATAMART_PATH)

    # 1. is_outlier_mild
    print_visidata_style(df_clean, "is_outlier_mild", "Outliers Leves de Goles (> 8.5 goles según IQR)", "1-datamart-limpio.csv", top_n=5)

    # 2. is_outlier_extreme
    print_visidata_style(df_clean, "is_outlier_extreme", "Outliers Extremos de Goles (> 13 goles según 3*IQR)", "1-datamart-limpio.csv", top_n=5)

    # 3. shootout_first_shooter
    print_visidata_style(df_clean, "shootout_first_shooter", "Primer Ejecutor en Penales (con Not_Recorded)", "1-datamart-limpio.csv", top_n=5)

    # 4. shootout_winner
    print_visidata_style(df_clean, "shootout_winner", "Ganador de Tanda de Penales (con None)", "1-datamart-limpio.csv", top_n=5)

    # 5. Exploración de partidos extremos en el archivo complementario
    if OUTLIERS_PATH.exists():
        df_out = pd.read_csv(OUTLIERS_PATH)
        print_visidata_style(df_out, "total_goals", "Distribución de Goles en Partidos Outliers Extremos", "2-partidos-outliers-extremos.csv", top_n=5)

if __name__ == "__main__":
    main()
