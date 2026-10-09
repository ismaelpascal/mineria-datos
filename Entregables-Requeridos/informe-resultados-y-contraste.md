# Informe de Resultados y Contraste

**Proyecto:** Minería de Datos sobre resultados internacionales de fútbol  
**Fase KDD:** Interpretación, evaluación y contraste de patrones  
**Objetivo del informe:** Explicar en lenguaje de alto nivel qué patrones fueron descubiertos, qué tablas y columnas los respaldan, cómo se interpretan, y por qué el modelo elegido cumple con restricciones de eficiencia y privacidad dentro del proceso KDD.

---

## 1. Resumen ejecutivo

El análisis permitió descubrir tres patrones principales en el corpus histórico de partidos internacionales:

1. **La localía sigue siendo el patrón predictivo dominante.**  
   El Árbol de Decisión identifica con mucha fuerza los casos de victoria local (`HOME_WIN`), alcanzando un recall de **96.99%** para esa clase.

2. **Los empates aparecen asociados a contextos específicos de mayor paridad competitiva.**  
   Aunque el modelo predice pocos empates, cuando el Árbol de Decisión predice `DRAW`, lo hace con una precisión de **98.35%**.

3. **Los torneos no son homogéneos.**  
   El clustering con K-Means separa torneos regulares de torneos con perfiles más extremos, especialmente aquellos con mayor promedio de goles o mayor peso de penales.

El modelo elegido para la tarea predictiva principal es el **Árbol de Decisión**, porque ofrece mejor desempeño que Gaussian Naive Bayes, es interpretable, eficiente y no requiere datos personales sensibles.

---

## 2. Tabla principal usada para evaluación predictiva

| Elemento | Detalle |
|---|---|
| Tabla / archivo usado | `Fase-8/1-metricas-clasificacion.csv` |
| Propósito | Comparar el desempeño de los modelos de clasificación. |
| Modelos evaluados | `Decision_Tree` y `Gaussian_Naive_Bayes` |
| Variable objetivo | `match_outcome` |
| Clases de salida | `HOME_WIN`, `DRAW`, `AWAY_WIN` |
| Cantidad de casos evaluados | 9,480 partidos del conjunto de prueba |

Esta tabla resume las métricas obtenidas por cada modelo después de entrenar con el conjunto de entrenamiento y evaluar sobre partidos no vistos.

---

## 3. Columnas usadas e interpretación

### 3.1. Columnas de `Fase-8/1-metricas-clasificacion.csv`

| Columna | Qué representa | Interpretación en el proyecto |
|---|---|---|
| `modelo` | Algoritmo evaluado. | Permite comparar Árbol de Decisión contra Naive Bayes. |
| `clase` | Resultado real del partido que se está evaluando. | Puede ser victoria local, empate o victoria visitante. |
| `precision` | De todos los casos que el modelo predijo como una clase, cuántos fueron correctos. | Sirve para saber qué tan confiable es una predicción cuando el modelo la emite. |
| `recall` | De todos los casos reales de una clase, cuántos logró detectar el modelo. | Sirve para saber si el modelo deja escapar muchos casos de una clase. |
| `f1_score` | Balance entre precisión y recall. | Resume el rendimiento cuando hay desequilibrio entre clases. |
| `soporte` | Cantidad real de casos de esa clase en el test set. | Permite saber cuántos ejemplos reales había para evaluar cada resultado. |
| `accuracy_global` | Porcentaje total de aciertos del modelo. | Mide el rendimiento general, pero debe interpretarse junto con precision y recall. |

---

## 4. Resultados de clasificación

### 4.1. Comparación general de modelos

| Modelo | Accuracy global | Lectura general |
|---|---:|---|
| Árbol de Decisión | 50.57% | Mejor modelo general. Detecta muy bien la victoria local y mantiene interpretabilidad. |
| Gaussian Naive Bayes | 25.99% | Rendimiento bajo. Tiende a sobrepredecir empates por su supuesto de independencia. |

**Interpretación:**  
El Árbol de Decisión supera claramente a Gaussian Naive Bayes. Aunque su accuracy no es extremadamente alta, es el modelo más útil para el contexto KDD porque permite explicar reglas de decisión y evita funcionar como una caja negra.

---

### 4.2. Métricas por clase del Árbol de Decisión

| Clase | Precision | Recall | F1-score | Soporte | Interpretación |
|---|---:|---:|---:|---:|---|
| `HOME_WIN` | 50.30% | 96.99% | 66.24% | 4,648 | El modelo detecta casi todas las victorias locales, confirmando la fuerza histórica de la localía. |
| `DRAW` | 98.35% | 5.52% | 10.45% | 2,156 | Predice pocos empates, pero cuando lo hace casi siempre acierta. |
| `AWAY_WIN` | 42.17% | 6.24% | 10.87% | 2,676 | Tiene dificultad para detectar victorias visitantes, porque el patrón dominante favorece al local. |

**Patrón descubierto:**  
La localía aparece como el factor dominante del corpus. El modelo reconoce que históricamente el equipo local concentra una parte importante de las victorias.

**Contraste crítico:**  
Este patrón es útil, pero no completamente novedoso. La ventaja de campo es conocida en el fútbol. Lo valioso es que el modelo la confirma cuantitativamente sobre un corpus histórico amplio de 47,396 partidos.

---

### 4.3. Métricas por clase de Gaussian Naive Bayes

| Clase | Precision | Recall | F1-score | Soporte | Interpretación |
|---|---:|---:|---:|---:|---|
| `HOME_WIN` | 69.10% | 3.46% | 6.60% | 4,648 | Aunque cuando predice local puede acertar, casi no detecta victorias locales reales. |
| `DRAW` | 23.99% | 92.53% | 38.10% | 2,156 | Predice demasiados empates, capturando muchos reales pero generando muchos falsos positivos. |
| `AWAY_WIN` | 33.12% | 11.51% | 17.08% | 2,676 | Detecta pocas victorias visitantes. |

**Interpretación:**  
Naive Bayes se comporta peor porque asume independencia entre variables que en el fútbol están relacionadas. Por ejemplo, torneo, confederación, neutralidad y era histórica no son factores completamente independientes.

**Contraste crítico:**  
El modelo bayesiano no fue seleccionado porque genera un patrón espurio: tiende a llevar demasiados casos hacia `DRAW`, lo que reduce su utilidad práctica.

---

## 5. Tabla de matriz de confusión

| Elemento | Detalle |
|---|---|
| Tabla / archivo usado | `Fase-8/2-matriz-confusion.csv` |
| Propósito | Observar los aciertos y errores de cada modelo por clase real. |
| Columnas principales | `clase_real`, `pred_HOME_WIN`, `pred_DRAW`, `pred_AWAY_WIN`, `total_real` |

### 5.1. Interpretación de columnas

| Columna | Interpretación |
|---|---|
| `modelo` | Modelo al que pertenece la matriz. |
| `clase_real` | Resultado verdadero del partido. |
| `pred_HOME_WIN` | Cantidad de partidos clasificados como victoria local. |
| `pred_DRAW` | Cantidad de partidos clasificados como empate. |
| `pred_AWAY_WIN` | Cantidad de partidos clasificados como victoria visitante. |
| `total_real` | Total de partidos reales de esa clase. |

### 5.2. Lectura del Árbol de Decisión

| Clase real | Predijo `HOME_WIN` | Predijo `DRAW` | Predijo `AWAY_WIN` | Total real | Interpretación |
|---|---:|---:|---:|---:|---|
| `HOME_WIN` | 4,508 | 2 | 138 | 4,648 | Detecta correctamente la gran mayoría de victorias locales. |
| `DRAW` | 1,946 | 119 | 91 | 2,156 | Muchos empates son absorbidos por la clase local. |
| `AWAY_WIN` | 2,509 | 0 | 167 | 2,676 | Muchas victorias visitantes también son clasificadas como locales. |

**Conclusión del contraste:**  
El Árbol de Decisión es fuerte para capturar el patrón dominante de localía, pero débil para reconocer clases minoritarias o menos favorecidas históricamente, como la victoria visitante.

---

## 6. Tabla usada para clustering de torneos

| Elemento | Detalle |
|---|---|
| Tabla / archivo usado | `Fase-7/2-clusters-torneos.csv` |
| Propósito | Agrupar torneos según características históricas de juego. |
| Algoritmo usado | K-Means con `K = 3` |
| Unidad de análisis | Torneo |

### 6.1. Columnas usadas e interpretación

| Columna | Qué representa | Interpretación |
|---|---|---|
| `tournament` | Nombre del torneo. | Permite identificar la competencia analizada. |
| `total_matches` | Cantidad de partidos del torneo. | Mide el peso histórico del torneo en el corpus. |
| `avg_goals` | Promedio de goles por partido. | Indica si el torneo tiende a ser más ofensivo o más cerrado. |
| `std_goals` | Desviación estándar de goles. | Mide variabilidad: torneos más impredecibles tienen mayor dispersión. |
| `home_win_rate` | Proporción de victorias locales. | Evalúa el peso de la localía en ese torneo. |
| `draw_rate` | Proporción de empates. | Indica nivel de paridad competitiva. |
| `away_win_rate` | Proporción de victorias visitantes. | Permite contrastar contra la ventaja local. |
| `penalty_shootout_rate` | Proporción de partidos con penales. | Señala torneos con alta frecuencia de eliminación directa o paridad. |
| `neutral_rate` | Proporción de partidos en cancha neutral. | Ayuda a interpretar si la localía pierde fuerza. |
| `intercontinental_rate` | Proporción de partidos entre confederaciones distintas. | Mide diversidad competitiva internacional. |
| `cluster_id` | Grupo asignado por K-Means. | Clasificación numérica del torneo. |
| `cluster_profile` | Nombre interpretativo del clúster. | Traduce el grupo numérico a una lectura de negocio. |

---

## 7. Interpretación de patrones del clustering

El clustering permitió clasificar torneos en perfiles generales. Los nombres asignados a los grupos ayudan a interpretar el resultado sin depender únicamente del número de clúster.

| Perfil de clúster | Interpretación de alto nivel |
|---|---|
| `Torneos_Competitivos_Regulares` | Torneos con comportamiento estable, promedios de gol moderados y distribución competitiva cercana al fútbol internacional formal. |
| `Torneos_Hiper_Goleadores` | Torneos con promedios altos de gol y mayor probabilidad de marcadores extremos. Suelen representar contextos de desigualdad competitiva. |
| `Torneos_Tácticos_Penales` | Torneos donde la paridad y las definiciones por penales tienen mayor peso relativo. |

**Patrón descubierto:**  
No todos los torneos deben analizarse con el mismo criterio. Algunos torneos regionales o insulares pueden distorsionar métricas globales por tener promedios de gol mucho más altos que el fútbol internacional regular.

**Contraste:**  
El clustering no busca predecir un resultado individual, sino encontrar grupos de torneos con comportamiento similar. Por eso complementa al modelo de clasificación.

---

## 8. Espacios para capturas de histogramas

Usá esta sección para pegar las imágenes de los histogramas generados durante el análisis. Podés reemplazar las rutas entre paréntesis por el nombre real del archivo de imagen.

### 8.1. Histograma de goles totales por partido

| Elemento | Detalle |
|---|---|
| Tabla usada | `Fase-3/1-datamart-limpio.csv` |
| Columna usada | `total_goals` |
| Qué muestra | Distribución de cantidad de goles por partido. |
| Interpretación esperada | La mayoría de partidos se concentra entre pocos goles; las goleadas extremas aparecen como cola derecha de la distribución. |

**Imagen del histograma:**

![Histograma de goles totales](ruta/a/la/captura-histograma-total-goals.png)

**Comentario sobre la captura:**  
La distribución permite observar que los partidos con marcadores muy altos son poco frecuentes. Esto justifica el uso del criterio de Tukey para marcar outliers sin eliminarlos del dataset principal.

---

### 8.2. Histograma del promedio de goles por torneo

| Elemento | Detalle |
|---|---|
| Tabla usada | `Fase-7/2-clusters-torneos.csv` |
| Columna usada | `avg_goals` |
| Qué muestra | Distribución del promedio de goles por torneo. |
| Interpretación esperada | Algunos torneos tienen promedios de gol superiores al comportamiento regular, lo que ayuda a explicar los clústeres hiper-goleadores. |

**Imagen del histograma:**

![Histograma de promedio de goles por torneo](ruta/a/la/captura-histograma-avg-goals.png)

**Comentario sobre la captura:**  
Si el histograma muestra una cola hacia valores altos, eso respalda la existencia de torneos con comportamiento ofensivo extremo o con desigualdad competitiva marcada.

---

### 8.3. Histograma de tasa de empates por torneo

| Elemento | Detalle |
|---|---|
| Tabla usada | `Fase-7/2-clusters-torneos.csv` |
| Columna usada | `draw_rate` |
| Qué muestra | Distribución de la proporción de empates por torneo. |
| Interpretación esperada | Torneos con mayor tasa de empates pueden reflejar mayor paridad competitiva o formatos más cerrados. |

**Imagen del histograma:**

![Histograma de tasa de empates](ruta/a/la/captura-histograma-draw-rate.png)

**Comentario sobre la captura:**  
Una mayor concentración en tasas medias sugiere equilibrio competitivo; valores altos pueden asociarse con torneos más tácticos o de eliminación directa.

---

### 8.4. Histograma de tasa de penales por torneo

| Elemento | Detalle |
|---|---|
| Tabla usada | `Fase-7/2-clusters-torneos.csv` |
| Columna usada | `penalty_shootout_rate` |
| Qué muestra | Distribución de frecuencia de tandas de penales por torneo. |
| Interpretación esperada | Los torneos con mayor tasa de penales suelen tener más partidos eliminatorios o mayor paridad. |

**Imagen del histograma:**

![Histograma de tasa de penales](ruta/a/la/captura-histograma-penalty-shootout-rate.png)

**Comentario sobre la captura:**  
Esta variable ayuda a interpretar el perfil `Torneos_Tácticos_Penales`, donde la definición por penales pesa más que en torneos regulares.

---

## 9. Defensa del modelo elegido

### 9.1. Modelo seleccionado

El modelo elegido para la tarea predictiva principal es el **Árbol de Decisión**.

### 9.2. Por qué se elige sobre Gaussian Naive Bayes

| Criterio | Árbol de Decisión | Gaussian Naive Bayes | Decisión |
|---|---|---|---|
| Accuracy global | 50.57% | 25.99% | Gana Árbol de Decisión. |
| Interpretabilidad | Alta: reglas comprensibles. | Media: depende de supuestos probabilísticos. | Gana Árbol de Decisión. |
| Manejo de relaciones entre variables | Mejor para reglas no lineales. | Débil si las variables no son independientes. | Gana Árbol de Decisión. |
| Utilidad para explicar patrones | Alta. | Baja en este caso por sobrepredicción de empates. | Gana Árbol de Decisión. |

**Conclusión:**  
El Árbol de Decisión es más adecuado porque ofrece mejor desempeño y permite explicar por qué toma decisiones. Para un proyecto KDD, la interpretabilidad es importante porque el objetivo no es solo predecir, sino descubrir y comunicar conocimiento.

---

## 10. Eficiencia computacional

El Árbol de Decisión cumple con la restricción de eficiencia porque, una vez entrenado, clasificar un partido requiere recorrer una cantidad pequeña de reglas. No necesita recalcular distancias contra todos los datos ni ejecutar procedimientos costosos en cada predicción.

**Ventajas de eficiencia:**

- Inferencia rápida.
- Bajo consumo de memoria.
- No requiere infraestructura compleja.
- Es apto para tableros o reportes ejecutivos.
- Sus reglas pueden auditarse fácilmente.

Esto lo vuelve adecuado para un contexto KDD donde se necesita transformar datos históricos en conocimiento utilizable y explicable.

---

## 11. Privacidad y restricciones éticas del KDD

El proyecto cumple con restricciones de privacidad porque trabaja con datos deportivos históricos y públicos, agregados a nivel de partido, selección y torneo.

**Datos utilizados:**

- Resultado del partido.
- Fecha.
- Equipo local y visitante.
- Torneo.
- Ciudad y país.
- Goles y penales.
- Variables derivadas como era, confederación o tasa de empates.

**Datos no utilizados:**

- Información médica de jugadores.
- Datos biométricos.
- Datos financieros.
- Información privada o sensible.
- Identificadores personales protegidos.

**Conclusión de privacidad:**  
El modelo no depende de datos personales sensibles. Por lo tanto, el conocimiento descubierto puede usarse para análisis deportivo, tableros e informes sin comprometer privacidad individual.

---

## 12. Conclusión final

El análisis muestra que el corpus histórico permite extraer conocimiento útil sobre el fútbol internacional. El patrón más fuerte es la ventaja de localía, confirmado por el alto recall del Árbol de Decisión en `HOME_WIN`. También se detectan comportamientos específicos en empates, penales y torneos con perfiles goleadores extremos.

El contraste entre modelos demuestra que el Árbol de Decisión es la mejor opción para este proyecto porque combina desempeño, interpretabilidad, eficiencia y bajo riesgo de privacidad. K-Means complementa el análisis al mostrar que los torneos pueden agruparse en perfiles distintos, lo que permite interpretar mejor el contexto competitivo.

En conjunto, los resultados cumplen con el objetivo del proceso KDD: transformar datos históricos en conocimiento comprensible, auditable y útil para la toma de decisiones.
