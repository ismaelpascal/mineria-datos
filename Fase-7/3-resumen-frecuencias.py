#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 7.
Muestra las tablas de frecuencias, conteos y porcentajes (top 5) para:
1. Distribución de predicciones del Árbol de Decisión en Test (1-predicciones-clasificacion.csv)
2. Distribución de predicciones de Naive Bayes en Test (1-predicciones-clasificacion.csv)
3. Distribución real en Test (actual_outcome)
4. Distribución de torneos por Clúster en K-Means (2-clusters-torneos.csv)
5. Muestra de torneos representativos por cada Clúster
"""

from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PRED_PATH = SCRIPT_DIR / "1-predicciones-clasificacion.csv"
CLUSTERS_PATH = SCRIPT_DIR / "2-clusters-torneos.csv"

def print_freq_table(df: pd.DataFrame, col_name: str, title: str, source_file: str, top_n: int = 5):
    total = len(df)
    counts = df[col_name].value_counts(dropna=False).head(top_n)
    
    print("\n" + "=" * 75)
    print(f"📊 TABLA RELEVANTE: {col_name} ({title})")
    print(f"📁 Archivo origen: {source_file} (Total filas: {total:,})")
    print(f"💡 Para ver el histograma interactivo en VisiData:")
    print(f"   1. Abre: vd Fase-7/{source_file}")
    print(f"   2. Sitúate en la columna '{col_name}' y presiona Shift + F")
    print("-" * 75)
    print(f"{'VALOR':<30} | {'COUNT':>8} | {'PERCENT %':>10} | HISTOGRAMA")
    print("-" * 75)
    
    max_count = counts.iloc[0] if len(counts) > 0 else 1
    for val, count in counts.items():
        pct = (count / total) * 100
        val_str = str(val)[:29]
        bar_len = int((count / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_len
        print(f"{val_str:<30} | {count:>8,d} | {pct:>9.2f}% | {bar}")
    print("=" * 75)

def main():
    if not PRED_PATH.exists() or not CLUSTERS_PATH.exists():
        print("❌ Error: No se encuentran los archivos. Ejecuta primero ./entrenar-modelos.py")
        return

    df_pred = pd.read_csv(PRED_PATH)
    df_clu = pd.read_csv(CLUSTERS_PATH)

    # 1. Resultados reales en el Test Set
    print_freq_table(df_pred, "actual_outcome", "Resultados Reales en Test Set (20% no visto)", "1-predicciones-clasificacion.csv")

    # 2. Predicciones Árbol de Decisión
    print_freq_table(df_pred, "pred_decision_tree", "Predicciones del Árbol de Decisión en Test", "1-predicciones-clasificacion.csv")

    # 3. Predicciones Naive Bayes
    print_freq_table(df_pred, "pred_naive_bayes", "Predicciones de Gaussian Naive Bayes en Test", "1-predicciones-clasificacion.csv")

    # 4. Distribución de Clústeres K-Means
    print_freq_table(df_clu, "cluster_profile", "Distribución de Torneos por Perfil Clúster (K-Means)", "2-clusters-torneos.csv")

    # 5. Muestra de torneos por clúster
    print("\n" + "=" * 75)
    print("📋 MUESTRA DE TORNEOS REPRESENTATIVOS POR CLÚSTER (Top torneos por volumen)")
    print("-" * 75)
    for profile in df_clu["cluster_profile"].unique():
        sub = df_clu[df_clu["cluster_profile"] == profile].head(3)
        tourneys_list = ", ".join(sub["tournament"].tolist())
        print(f"🔸 {profile} ({len(df_clu[df_clu['cluster_profile'] == profile])} torneos):")
        print(f"   └─ Ejemplos: {tourneys_list}")
    print("=" * 75)

if __name__ == "__main__":
    main()
