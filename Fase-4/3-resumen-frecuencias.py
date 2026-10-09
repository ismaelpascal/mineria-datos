#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 4.
Muestra las tablas de frecuencias, conteos, porcentajes y barras de histograma
para las variables transformadas:
- era (Eras históricas)
- home_confederation
- tournament_tier (Nivel del torneo)
- month (Estacionalidad mensual)
- is_intercontinental

Muestra como máximo los 5 primeros resultados por tabla.
"""

from pathlib import Path
import pandas as pd

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
TRANSFORMED_PATH = SCRIPT_DIR / "1-dataset-transformado.csv"

def print_visidata_style(df: pd.DataFrame, col_name: str, title: str, source_file: str, top_n: int = 5):
    total = len(df)
    counts = df[col_name].value_counts(dropna=False).head(top_n)
    
    print("\n" + "=" * 70)
    print(f"📊 TABLA RELEVANTE: {col_name} ({title})")
    print(f"📁 Archivo origen: {source_file} (Total filas: {total:,})")
    print(f"💡 Para ver el histograma interactivo en VisiData:")
    print(f"   1. Abre: vd Fase-4/{source_file}")
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
    if not TRANSFORMED_PATH.exists():
        print(f"❌ Error: No se encontró {TRANSFORMED_PATH}. Ejecuta primero ./transformar-datos.py")
        return

    df = pd.read_csv(TRANSFORMED_PATH)

    # 1. era
    print_visidata_style(df, "era", "Distribución de Partidos por Eras Históricas", "1-dataset-transformado.csv", top_n=5)

    # 2. home_confederation
    print_visidata_style(df, "home_confederation", "Confederaciones de Selecciones Locales", "1-dataset-transformado.csv", top_n=5)

    # 3. tournament_tier
    print_visidata_style(df, "tournament_tier", "Jerarquía del Torneo Disputado", "1-dataset-transformado.csv", top_n=5)

    # 4. month
    print_visidata_style(df, "month", "Estacionalidad por Mes del Año", "1-dataset-transformado.csv", top_n=5)

    # 5. is_intercontinental
    print_visidata_style(df, "is_intercontinental", "Encuentros Intercontinentales (Distintas Confederaciones)", "1-dataset-transformado.csv", top_n=5)

if __name__ == "__main__":
    main()
