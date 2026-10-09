#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 8: Evaluación y Auditoría de Métricas de Minería de Datos

Objetivo:
- Calcular formalmente y exportar a CSV:
  * 1-metricas-clasificacion.csv: Accuracy, Precision, Recall y F1-Score por clase y globales para cada modelo.
  * 2-matriz-confusion.csv: Matrices de confusión comparadas para Árbol de Decisión y Gaussian Naive Bayes.
"""

from pathlib import Path
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
PRED_PATH = BASE_DIR / "Fase-7" / "1-predicciones-clasificacion.csv"

OUTPUT_METRICS = SCRIPT_DIR / "1-metricas-clasificacion.csv"
OUTPUT_CONFUSION = SCRIPT_DIR / "2-matriz-confusion.csv"

def evaluate_models():
    print("[1/3] Cargando predicciones de Fase 7...")
    df = pd.read_csv(PRED_PATH)
    y_true = df["actual_outcome"]
    y_dt = df["pred_decision_tree"]
    y_gnb = df["pred_naive_bayes"]
    classes = ["HOME_WIN", "DRAW", "AWAY_WIN"]

    # ==========================================================
    # 1. MÉTRICAS DETALLADAS (PRECISIÓN, RECALL, F1)
    # ==========================================================
    print("[2/3] Computando Precision, Recall, F1 y Accuracy...")
    metrics_records = []

    for model_name, y_pred in [("Decision_Tree", y_dt), ("Gaussian_Naive_Bayes", y_gnb)]:
        acc = accuracy_score(y_true, y_pred)
        prec, rec, f1, supp = precision_recall_fscore_support(y_true, y_pred, labels=classes, zero_division=0)
        
        for c, p, r, f, s in zip(classes, prec, rec, f1, supp):
            metrics_records.append({
                "modelo": model_name,
                "clase": c,
                "precision": round(p, 4),
                "recall": round(r, 4),
                "f1_score": round(f, 4),
                "soporte": int(s),
                "accuracy_global": round(acc, 4)
            })

    metrics_df = pd.DataFrame(metrics_records)
    metrics_df.to_csv(OUTPUT_METRICS, index=False)
    print(f"  - Guardado: {OUTPUT_METRICS}")

    # ==========================================================
    # 2. MATRIZ DE CONFUSIÓN
    # ==========================================================
    print("[3/3] Estructurando matrices de confusión...")
    conf_records = []
    
    for model_name, y_pred in [("Decision_Tree", y_dt), ("Gaussian_Naive_Bayes", y_gnb)]:
        cm = confusion_matrix(y_true, y_pred, labels=classes)
        for i, real_c in enumerate(classes):
            conf_records.append({
                "modelo": model_name,
                "clase_real": real_c,
                "pred_HOME_WIN": int(cm[i, 0]),
                "pred_DRAW": int(cm[i, 1]),
                "pred_AWAY_WIN": int(cm[i, 2]),
                "total_real": int(cm[i].sum())
            })

    conf_df = pd.DataFrame(conf_records)
    conf_df.to_csv(OUTPUT_CONFUSION, index=False)
    print(f"  - Guardado: {OUTPUT_CONFUSION}")
    print("✅ ¡Evaluación de métricas completada con éxito!")

if __name__ == "__main__":
    evaluate_models()
