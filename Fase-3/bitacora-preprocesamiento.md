# Bitácora Técnica de Preprocesamiento y Limpieza de Datos

**Fase KDD:** Fase 3 (Data Cleaning and Preprocessing)  
**Corpus de datos analizado:** 47,396 partidos consolidados, 44,362 goles registrados y 644 definiciones por penales.

---

## 1. Auditoría y Tratamiento de Valores Faltantes (Nulos)

### A. Minutos de Gol en `Goal_Scorers.csv`
* **Diagnóstico cuantitativo:** Se identificaron **259 registros con `minute = NaN`** (0.58% del corpus de goles), concentrados en torneos de los años 1960 a 1980 (ej. Copa Africana de Naciones 1963, Torneo de la Amistad 1980 en Oceanía).
* **Evaluación de impacto en varianza:**
  - Varianza / Desviación estándar original de minutos: $\sigma = 26.358$ min (media = 50.01 min, mediana = 51.0 min).
  - Si se imputara con la media/mediana: $\sigma = 26.281$ min (comprime artificialmente la varianza en torno al minuto 50).
  - Al consolidar en el Data Mart analítico a nivel partido, los minutos se utilizan para segmentar en variables estructurales (`goals_first_half` $\le 45$ y `goals_second_half` $> 45$).
* **Regla técnica adoptada:** **No descartar los goles** (para no falsear el resultado real del partido). Los 259 goles sin minuto se conservaron contabilizados en `total_recorded_goals`, asignando `False` a los tramos de tiempo específicos. Esta estrategia penaliza $0.0\%$ el volumen de goles y preserva la integridad del conteo global.

### B. Ejecutor Inicial en Penales (`first_shooter`)
* **Diagnóstico cuantitativo:** De 644 partidos con penales, **414 registros presentaban `first_shooter = NaN`** (64.28% de los shootouts), debido a falta de cobertura en las actas históricas previas a la década del 2000.
* **Regla técnica adoptada:** Imputación semántica de categoría explícita: `'Not_Recorded'`. Para los 46,753 partidos sin tanda de penales, el valor es `'None'` o ausente. Se evita la eliminación de filas para no sesgar las tasas de éxito en torneos eliminatorios.

### C. Nombres de Goleadores Faltantes (`scorer`)
* **Diagnóstico cuantitativo:** **49 registros** con `scorer = NaN` (goles de partidos regionales donde solo se asentó el resultado numérico, ej. Vanuatu vs. Papúa Nueva Guinea en 1980).
* **Regla técnica adoptada:** Preservación del registro del gol contabilizado numéricamente; al calcular `unique_scorers` se computa la cardinalidad de nombres no nulos presentes.

---

## 2. Consistencia y Estandarización de Cadenas de Texto

* **Normalización de entidades nacionales:**
  - En el dataset base, selecciones con continuidad jurídica o refundación geopolítica (como **Rusia** que abarca históricamente a la URSS en las fuentes deportivas oficiales) se encuentran unificadas bajo `Russia` (registros desde 1912), mientras que entidades con selecciones paralelas contemporáneas (como `German DR` y `Germany`, o `Yugoslavia` y `Serbia`) mantienen su autonomía estadística correcta.
  - Se corrigió la discrepancia detectada en penales para `Åland` $\rightarrow$ `Åland Islands`, logrando match exacto del 100% en las definiciones de torneos insulares.
* **Codificación y saneamiento de espacios:**
  - Se aplicó función `.str.strip()` en campos categóricos (`home_team`, `away_team`, `tournament`, `city`, `country`) para erradicar espacios en blanco residuales (*trailing/leading whitespaces*) que puedan provocar duplicación espuria de categorías en algoritmos de clustering y clasificación.

---

## 3. Identificación y Decisión sobre Datos Atípicos (Outliers)

Se realizó un análisis estadístico sobre la variable `total_goals` ($g = \text{home\_score} + \text{away\_score}$) en los 47,396 partidos:
* **Parámetros de distribución:**
  - Mínimo: 0 goles.
  - Máximo: 31 goles (Australia 31 - 0 American Samoa, 2001-04-11).
  - Media: 2.94 goles ($\sigma = 2.08$).
  - Cuartiles: $Q_1 = 1.0$, Mediana = 3.0, $Q_3 = 4.0$.
  - Rango Intercuartílico: $\text{IQR} = Q_3 - Q_1 = 3.0$ goles.
* **Umbrales Tukey:**
  - **Límite Outlier Leve:** $Q_3 + 1.5 \times \text{IQR} = 4.0 + 4.5 = \mathbf{8.5\text{ goles}}$.
    - Frecuencia: **807 partidos** (1.70% del dataset). Corresponden a goleadas amplias típicas en clasificatorias con selecciones emergentes.
  - **Límite Outlier Extremo:** $Q_3 + 3.0 \times \text{IQR} = 4.0 + 9.0 = \mathbf{13.0\text{ goles}}$.
    - Frecuencia: **86 partidos** (0.18% del dataset). Incluyen marcas históricas (31 goles en Australia vs. Samoa Americana, 30 goles en Tahití vs. Islas Cook 1971, etc.).

### Decisión Técnica Justificada para Minería:
1. **Preservación en el dataset principal (`1-datamart-limpio.csv`):** Los 86 partidos de goleada extrema son **hechos deportivos verídicos**, no errores de tipeo ni ruido de medición. Eliminarlos privaría al modelo del conocimiento de asimetría de fuerzas.
2. **Flag de trazabilidad:** Se crearon las columnas booleanas `is_outlier_mild` e `is_outlier_extreme` para permitir filtrado selectivo según el algoritmo:
   - Para algoritmos sensibles a distancias euclidianas (como **K-Means** o **Regresiones**), se podrán aislar o recortar para evitar distorsión de centroides.
   - Para algoritmos basados en particiones o probabilidades (como **Árboles de Decisión**, **Random Forest** o **Naive Bayes**), se mantienen íntegros ya que son inmunes a la escala de valores extremos.
3. **Dataset de Aislamiento (`2-partidos-outliers-extremos.csv`):** Se exportó un archivo independiente con los 86 encuentros extremos para auditoría y contraste analítico.

---

## 4. Archivos Generados en Fase 3

| Archivo | Descripción | Cantidad de Filas |
| :--- | :--- | :--- |
| `1-datamart-limpio.csv` | Dataset consolidado limpio con flags de auditoría y nulos resueltos. | 47,396 |
| `2-partidos-outliers-extremos.csv` | Corpus de partidos con goleadas históricas extremas (> 13 goles). | 86 |
| `limpiar-datos.py` | Script reproducible de limpieza y auditoría. | - |
| `3-resumen-frecuencias.py` | Visualizador rápido en terminal estilo VisiData. | - |
| `bitacora-preprocesamiento.md` | Este documento de bitácora técnica KDD. | - |
