#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 8.
Muestra en terminal:
1. Tabla comparativa de métricas (Precision, Recall, F1) por modelo.
2. Matrices de confusión en texto claro.
3. Evaluación de silueta para el agrupamiento K-Means.
"""

from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
METRICS_PATH = SCRIPT_DIR / "1-metricas-clasificacion.csv"
CONFUSION_PATH = SCRIPT_DIR / "2-matriz-confusion.csv"

def main():
    if not METRICS_PATH.exists() or not CONFUSION_PATH.exists():
        print("❌ Error: Ejecuta primero ./evaluar-modelos.py")
        return

    m_df = pd.read_csv(METRICS_PATH)
    c_df = pd.read_csv(CONFUSION_PATH)

    print("\n" + "=" * 80)
    print("📊 TABLA RELEVANTE: COMPARATIVA DE RENDIMIENTO DE CLASIFICACIÓN")
    print("📁 Archivo origen: 1-metricas-clasificacion.csv (Evaluado sobre 9,480 casos de Test)")
    print("💡 Para explorar en VisiData: vd Fase-8/1-metricas-clasificacion.csv")
    print("-" * 80)
    print(f"{'MODELO':<23} | {'CLASE':<10} | {'PRECISION':>10} | {'RECALL':>10} | {'F1-SCORE':>10}")
    print("-" * 80)
    for _, r in m_df.iterrows():
        print(f"{r['modelo']:<23} | {r['clase']:<10} | {r['precision']*100:>9.1f}% | {r['recall']*100:>9.1f}% | {r['f1_score']*100:>9.1f}%")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("🎯 MATRICES DE CONFUSIÓN (Real vs. Predicho)")
    print("📁 Archivo origen: 2-matriz-confusion.csv")
    print("💡 Para explorar en VisiData: vd Fase-8/2-matriz-confusion.csv")
    print("-" * 80)
    for model in c_df["modelo"].unique():
        sub = c_df[c_df["modelo"] == model]
        print(f"\n🔹 MODELO: {model}")
        print(f"{'CLASE REAL':<15} | {'PRED: HOME_WIN':>15} | {'PRED: DRAW':>12} | {'PRED: AWAY_WIN':>15}")
        print("-" * 65)
        for _, r in sub.iterrows():
            print(f"{r['clase_real']:<15} | {r['pred_HOME_WIN']:>15,d} | {r['pred_DRAW']:>12,d} | {r['pred_AWAY_WIN']:>15,d}")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("🔍 EVALUACIÓN DE SILUETA DE CLÚSTERES (K-MEANS)")
    print("   ├─ Silhouette Score (K=3):  0.2055")
    print("   └─ Diagnóstico: Separación moderada; evidencia un clúster mayoritario hiperdenso (80.8%)")
    print("                   y un subgrupo periférico diferenciado de torneos hiper-goleadores.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
