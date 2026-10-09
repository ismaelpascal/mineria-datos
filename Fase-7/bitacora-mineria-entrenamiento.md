# Bitácora de Ejecución de Minería de Datos (Fase 7)

**Fase KDD:** Fase 7 (Data Mining Execution)  
**Corpus de datos:** 47,396 partidos internacionales y 78 torneos representativos.

---

## 1. Tarea Predictiva: Clasificación Supervisada Tri-clase

### A. Partición Estricta Train / Test (Control de Overfitting)
Para evitar el sobreajuste (*overfitting*), uno de los principales retos destacados en la teoría de Minería de Datos, se implementó una partición estricta **80% Entrenamiento y 20% Prueba**, estratificada por la variable objetivo (`match_outcome`):

- **Conjunto de Entrenamiento (Train):** 37,916 partidos.
- **Conjunto de Prueba no visto (Test):** 9,480 partidos.
- **Distribución de Clases en Test:**
  - `HOME_WIN`: 4,648 partidos (49.03%)
  - `AWAY_WIN`: 2,676 partidos (28.23%)
  - `DRAW`: 2,156 partidos (22.74%)

### B. Modelos Entrenados y Ejecución
1. **Modelo 1: Árbol de Decisión (CART):**
   - Configuración: `max_depth=5`, `min_samples_leaf=20`, criterio Gini.
   - Entrenado exclusivamente con variables ex-ante (sin datos ocurridos durante el partido).
2. **Modelo 2: Gaussian Naive Bayes:**
   - Estimación de probabilidades bayesianas continuas.
3. **Dataset Generado:** `1-predicciones-clasificacion.csv` con 9,480 filas que contienen:
   - Resultado real (`actual_outcome`).
   - Predicción de cada modelo (`pred_decision_tree`, `pred_naive_bayes`).
   - Probabilidades estimadas para cada clase (`proba_dt_*`, `proba_gnb_*`).

---

## 2. Tarea Descriptiva: Clustering No Supervisado con K-Means

### A. Metodología de Ejecución
- **Entidad:** 78 torneos internacionales representativos ($\ge 30$ partidos históricos).
- **Preprocesamiento:** Estandarización de variables ($Z$-Score) con `StandardScaler` sobre: promedio de goles, desviación de goles, tasa de victoria local, empates, victorias visitantes, tasa de tandas de penales y tasa de partidos neutrales.
- **Parámetros del Algoritmo:** $K=3$ clústeres, inicialización `k-means++`, `n_init=15`, semilla aleatoria 42.

### B. Clústeres Descubiertos e Interpretación de Negocio
- **Clúster 1: `Torneos_Competitivos_Regulares` (63 torneos, 80.77%):**
  - Ejemplos: Copa Mundial de la FIFA, Eliminatorias Mundialistas, Eurocopa, Copa América, Amistosos internacionales.
  - Perfil: Promedio de goles moderado (~2.4 a 3.0), alta paridad y estructuras de competencia estandarizadas.
- **Clúster 2: `Torneos_Hiper_Goleadores` (15 torneos, 19.23%):**
  - Ejemplos: *South Pacific Games* (5.91 goles), *Pacific Games* (5.57 goles), *Central American and Caribbean Games* (5.59 goles), *Island Games*, *Viva World Cup*.
  - Perfil: Competiciones regionales con enorme asimetría deportiva y amateurs, con promedios superiores a 4.5 goles por partido.
- **Dataset Generado:** `2-clusters-torneos.csv` con la asignación de cada torneo a su respectivo clúster y perfil de negocio.

---

## 3. Resumen de Archivos Generados en Fase 7

| Archivo | Tipo | Descripción |
| :--- | :--- | :--- |
| `1-predicciones-clasificacion.csv` | Dataset | 9,480 filas con el resultado real y predicciones/probabilidades de los 2 modelos sobre Test. |
| `2-clusters-torneos.csv` | Dataset | 78 torneos clasificados en sus clústeres por K-Means con perfiles deportivos asignados. |
| `entrenar-modelos.py` | Script Python | Código documentado de entrenamiento y partición Train/Test. |
| `3-resumen-frecuencias.py` | Script Terminal | Visualizador rápido estilo VisiData con frecuencias y barras de histograma. |
| `bitacora-mineria-entrenamiento.md` | Documentación | Bitácora técnica de ejecución de los modelos. |
