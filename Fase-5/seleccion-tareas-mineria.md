# Formalización Técnica de las Tareas de Minería de Datos

**Fase KDD:** Fase 5 (Data Mining Task Selection)  
**Corpus de datos de entrada:** Matriz procesada de 47,396 partidos y agregaciones analíticas de torneos y eras.

En correspondencia directa con la formulación de objetivos de negocio de la **Fase 1**, se definen y formalizan matemáticamente las dos tareas mineras principales del proyecto KDD:

---

## 1. Tarea Predictiva: Clasificación Supervisada Multiclase

### A. Definición Formal
Dado un conjunto de entrenamiento $D_{train} = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$, donde $\mathbf{x}_i \in \mathbb{R}^d$ representa el vector de características contextuales y deportivas del partido $i$, se busca inducir una función de decisión (o estimador de probabilidades) $f: \mathcal{X} \rightarrow \mathcal{Y}$ que prediga el desenlace del partido.

* **Espacio de Clases (Target):**
  $$\mathcal{Y} = \{\text{HOME\_WIN}, \text{DRAW}, \text{AWAY\_WIN}\}$$
  - $\text{HOME\_WIN}$ ($49.03\%$ del corpus)
  - $\text{AWAY\_WIN}$ ($28.22\%$ del corpus)
  - $\text{DRAW}$ ($22.75\%$ del corpus)

* **Espacio de Características ($\mathbf{x}_i$):**
  Para evitar la **fuga de datos (data leakage)**, se exige que las variables predictoras correspondan a condiciones conocidas **antes de iniciar el encuentro o contextuales a su desarrollo**, tales como:
  - Condición de localía / neutralidad de campo (`neutral`).
  - Tipo y jerarquía de torneo (`tournament_tier_Friendly`, `tournament_tier_Qualifiers`, `tournament_tier_World_Cup_Finals`, etc.).
  - Confederación geográfica de las selecciones contendientes (`home_confederation_*`, `away_confederation_*`).
  - Carácter intercontinental del encuentro (`is_intercontinental`).
  - Época histórica y estacionalidad del partido (`era_*`, `month`).

* **Métricas Técnicas de Evaluación:**
  - Macro-Averaged F1-Score (para penalizar sesgos hacia la clase mayoritaria `HOME_WIN`).
  - Matriz de Confusión multiclase $3 \times 3$.
  - Accuracy global y Log-Loss multiclase.

---

## 2. Tarea Descriptiva: Agrupamiento No Supervisado (Clustering)

### A. Definición Formal
Dado un conjunto de entidades no etiquetadas $S = \{\mathbf{z}_k\}_{k=1}^{M}$ que representan los **78 torneos internacionales representativos** (con $\ge 30$ partidos históricos analizados), se busca encontrar una partición óptima $C = \{C_1, C_2, \dots, C_K\}$ tal que los torneos dentro del mismo clúster presenten máxima similitud interna (cohesión) y máxima separación respecto a otros clústeres.

* **Espacio de Atributos Descriptivos ($\mathbf{z}_k \in \mathbb{R}^p$):**
  1. `avg_goals`: Intensidad ofensiva media por partido.
  2. `std_goals`: Dispersión y volatilidad en el marcador.
  3. `home_win_rate`: Grado de ventaja por localía en el torneo.
  4. `draw_rate`: Nivel de paridad competitiva (tasa de empates).
  5. `away_win_rate`: Capacidad de resistencia visitante.
  6. `penalty_shootout_rate`: Propensión del torneo a resolverse por tandas de penales.
  7. `neutral_rate`: Proporción de partidos disputados en sede neutral.

* **Métricas Técnicas de Evaluación:**
  - **Silhouette Coefficient (Coeficiente de Silueta):** Mide qué tan cercano está cada punto a su propio clúster en comparación con el clúster vecino más próximo (rango $[-1, 1]$).
  - **Inercia / Suma de Cuadrados Intra-Clúster (WCSS):** Criterio del codo (*Elbow Method*) para determinar el número óptimo de agrupamientos $K$.

---

## 3. Matriz de Síntesis KDD

| Dimensión | Tarea Predictiva | Tarea Descriptiva |
| :--- | :--- | :--- |
| **Paradigma** | Supervisado | No Supervisado |
| **Algoritmos Candidatos (Fase 6)** | Árboles de Decisión / Random Forest vs. Naive Bayes Multinomial/Gaussiano | K-Means vs. Clustering Aglomerativo Jerárquico |
| **Unidad de Instancia** | Partido individual ($M_i$, $N=47,396$) | Torneo internacional consolidado ($T_k$, $M=78$) |
| **Dataset Insumo** | `Fase-4/2-matriz-mineria.csv` | `Fase-5/1-dataset-descriptivo-torneos.csv` |
| **Resultado Esperado** | Clasificador de probabilidades de victoria en tiempo real. | Taxonomía de torneos según competitividad y perfil goleador. |

---

## 4. Archivos Generados en Fase 5

| Archivo | Tipo | Descripción |
| :--- | :--- | :--- |
| `1-dataset-descriptivo-torneos.csv` | Dataset | Tablón descriptivo agregado por torneo con 78 entidades representativas y 9 métricas. |
| `formalizar-tareas.py` | Script Python | Código reproducible de extracción y cálculo de métricas de torneos. |
| `2-resumen-frecuencias.py` | Script Terminal | Visualizador estilo VisiData con los 5 torneos más goleadores, más paritarios y con más penales. |
| `seleccion-tareas-mineria.md` | Documentación | Formalización matemática y justificación de las dos tareas KDD. |
