# Proyecto KDD: Minería de Datos sobre Corpus Deportivo Histórico

Proyecto analítico completo que implementa las **9 etapas del proceso KDD (Knowledge Discovery in Databases)** sobre un corpus de datos deportivos internacionales históricos (1872 – 2024), abarcando más de 47,000 partidos, 44,000 goles y definiciones por penales.

---

## 📂 Estructura del Repositorio

El proyecto se encuentra organizado secuencialmente de acuerdo a las fases del estándar KDD:

```text
├── Fase-1/   # Comprensión del Dominio y Definición Formal del Problema
├── Fase-2/   # Selección y Creación del Target Dataset (Data Mart Consolidado)
├── Fase-3/   # Preprocesamiento y Limpieza (Tratamiento de Nulos y Outliers)
├── Fase-4/   # Transformación y Reducción (Feature Engineering, Eras, OHE)
├── Fase-5/   # Selección de Tareas de Minería (Clasificación y Clustering)
├── Fase-6/   # Selección y Justificación Técnica de Algoritmos (Mermaid)
├── Fase-7/   # Minería de Datos (Train/Test 80/20, Decision Tree, Naive Bayes, K-Means)
├── Fase-8/   # Interpretación y Evaluación de Patrones (Matrices de Confusión, Silueta)
└── Fase-9/   # Consolidación del Conocimiento y Despliegue (Dashboard, MLOps)
```

---

## 🚀 Requisitos y Entorno de Ejecución

Para ejecutar los scripts de Python:
- **Python 3.10+**
- Librerías: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`

Para explorar los datos de forma interactiva en terminal:
- **VisiData (`vd`)**: Cada fase incluye scripts `*-resumen-frecuencias.py` o archivos CSV directamente auditables mediante:
  ```bash
  vd Fase-X/archivo.csv
  ```

---

## 📊 Resumen de Resultados por Fase KDD

1. **Fase 1 (Dominio):** Formulación de objetivos de negocio (Win-Probability y tipificación de eras).
2. **Fase 2 (Target Dataset):** Integración relacional de `Match_Results.csv`, `Goal_Scorers.csv` y `Penalty_Shootouts.csv` en un Data Mart canónico (`match_id`).
3. **Fase 3 (Limpieza):** Imputación justificada de minutos de gol preservando la varianza, y detección de 86 goleadas extremas (>13 goles) mediante rango intercuartílico ($Q_3 + 3\times\text{IQR}$).
4. **Fase 4 (Transformación):** Creación de 5 Eras Históricas (`Pre_Guerra`, `Post_Guerra`, `Era_Moderna`, `Era_Global_Digital`, `Era_VAR`), 6 confederaciones FIFA y matriz numérica con One-Hot Encoding.
5. **Fase 5 (Tareas Mineras):** Formalización de Clasificación Multiclase ex-ante y dataset descriptivo de 78 torneos representativos.
6. **Fase 6 (Algoritmos):** Justificación de Árbol de Decisión vs. Gaussian Naive Bayes y K-Means mediante diagramas Mermaid.
7. **Fase 7 (Entrenamiento):** Partición estricta 80% Train y 20% Test (9,480 casos no vistos) y ajuste de K-Means ($K=3$).
8. **Fase 8 (Evaluación):** Auditoría crítica de matrices de confusión (97% recall en victorias locales y 98.4% precisión en empates en series de penales) y coeficiente de silueta de clústeres ($0.2055$).
9. **Fase 9 (Despliegue):** Diseño de Tablero Visual, protocolo de monitorización anual contra *concept drift* y gobernanza bajo normativas de privacidad RGPD.
