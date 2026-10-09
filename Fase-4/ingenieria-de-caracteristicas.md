# Documentación de Transformación y Reducción de Datos (Feature Engineering)

**Fase KDD:** Fase 4 (Data Transformation and Reduction)  
**Corpus procesado:** 47,396 partidos internacionales limpios.

---

## 1. Justificación de la Transformación
Los algoritmos de minería de datos (clasificación supervisada, agrupamiento k-means, árboles de decisión) requieren representaciones numéricas estructuradas y no pueden procesar directamente texto no acotado o cadenas de fechas (`1998-07-12`).

En esta fase se transformó el corpus transaccional en un **espacio de características multidimensional (Feature Space)** con información temporal, geográfica, jerárquica y métricas estructurales de rendimiento.

---

## 2. Ingeniería de Características Implementada

### A. Derivación Temporal y Segmentación por "Eras Históricas"
Se descompuso la fecha (`date`) en componentes temporales (`year`, `month`, `day_of_week`, `decade`) y se creó la variable categórica clave **`era`** basada en la evolución del reglamento y el contexto histórico del fútbol:

| Era Histórica | Período | Hito Reglamentario / Contexto | Partidos | % del Corpus |
| :--- | :--- | :--- | :--- | :--- |
| **`Pre_Guerra`** | 1872 – 1944 | Fútbol formativo, entreguerras y primeros 3 Mundiales. | 2,693 | 5.68% |
| **`Post_Guerra_Clasica`** | 1945 – 1969 | Reanudación de la Copa del Mundo, consolidación FIFA y era de Pelé. | 5,231 | 11.04% |
| **`Era_Moderna`** | 1970 – 1997 | Introducción de tarjetas amarillas/rojas (México 70), sustituciones y fútbol profesional total. | 14,563 | 30.73% |
| **`Era_Global_Digital`** | 1998 – 2017 | Expansión a 32 selecciones en Mundiales, ley Bosman y comercialización global. | 18,740 | 39.54% |
| **`Era_VAR`** | 2018 – 2024 | Implementación del Árbitro Asistente de Video (Rusia 2018), 5 cambios y mayor control de penales. | 6,169 | 13.02% |

### B. Mapeo Geográfico y Jerarquía de Confederaciones
Se clasificaron las 336 selecciones en sus **Confederaciones Oficiales FIFA**:
- **UEFA:** Europa (15,505 partidos como local, 32.71%).
- **CAF:** África (10,100 partidos como local, 21.31%).
- **AFC:** Asia (9,831 partidos como local, 20.74%).
- **CONCACAF:** Norte, Centroamérica y Caribe (6,116 partidos como local, 12.90%).
- **CONMEBOL:** Sudamérica (3,585 partidos como local, 7.56%).
- **OFC:** Oceanía.
- **Other/Regional:** Selecciones no afiliadas a FIFA o equipos regionales insulares.
- **Variable `is_intercontinental`:** Indicador booleano que detecta choques entre distintas confederaciones (15.29% de los partidos).

### C. Jerarquización de Torneos (`tournament_tier`)
De los 175 nombres textuales de torneos se redujo la cardinalidad a 5 estratos analíticos:
1. **`Friendly`:** Partidos amistosos (37.96%).
2. **`Qualifiers`:** Eliminatorias mundialistas y continentales (31.89%).
3. **`Regional_Tournament`:** Copas regionales (Island Games, CECAFA, etc.) (20.06%).
4. **`Continental_Championship`:** Fases finales de torneos continentales (Euro, Copa América, AFCON, etc.) (8.05%).
5. **`World_Cup_Finals`:** Fases finales de la Copa Mundial de la FIFA (2.03%).

### D. Métricas Estructurales del Partido
- `home_goal_share`: Proporción de goles convertidos por el local frente al total del partido.
- `abs_goal_diff`: Magnitud absoluta de la diferencia de goles (métrica de paridad/desigualdad).
- `first_half_ratio` y `second_half_ratio`: Proporción de goles anotados en el primer tiempo ($\le 45'$) vs. segundo tiempo ($> 45'$).
- `penalty_goal_ratio`: Dependencia del gol de penal respecto al total de goles registrados.

---

## 3. Reducción y Codificación para Minería

Para abastecer a las Fases 5, 6 y 7, se construyó una **matriz numérica pura**:
* **Archivo:** `2-matriz-mineria.csv` (47,396 filas x 42 columnas).
* **One-Hot Encoding (OHE):** Codificación binaria ($0/1$) de las variables categóricas de alta significancia:
  - `era_*` (5 columnas)
  - `tournament_tier_*` (5 columnas)
  - `home_confederation_*` (7 columnas)
  - `away_confederation_*` (7 columnas)
* **Variables numéricas escalables:** Goles, diferenciales, indicadores temporales y flags de outliers.
* **Target:** `match_outcome` (`HOME_WIN`, `DRAW`, `AWAY_WIN`).

---

## 4. Archivos Generados en Fase 4

| Archivo | Tipo | Descripción |
| :--- | :--- | :--- |
| `1-dataset-transformado.csv` | Dataset Enriquecido | Contiene las 47,396 filas con todas las variables originales más las derivadas (eras, confederaciones, ratios). |
| `2-matriz-mineria.csv` | Matriz Numérica KDD | Matriz codificada con One-Hot Encoding lista para entrenar algoritmos de Machine Learning. |
| `transformar-datos.py` | Script Python | Código reproducible de feature engineering y reducción. |
| `3-resumen-frecuencias.py` | Script Terminal | Visualizador estilo VisiData con los 5 primeros resultados de cada feature. |
| `ingenieria-de-caracteristicas.md` | Documentación | Justificación teórica y diccionario técnico de features. |
