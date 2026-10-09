# FASE 1: Comprensión del Dominio y Definición del Problema

## 1. Contexto del Negocio y Rol Asumido
**Rol:** Equipo Analítico Senior de Ciencia de Datos y Minería Deportiva para una Federación Internacional de Fútbol y Cadena Mediática Deportiva Global (Broadcaster & Performance Analytics).

**Contexto del Dominio:**
El fútbol de selecciones nacionales cuenta con más de un siglo de historia documentada. Los organismos federativos y las cadenas audiovisuales requieren transformar registros históricos crudos en:
1. Inteligencia deportiva táctica y competitiva (para cuerpos técnicos, comités organizadores y selecciones).
2. Contenido enriquecido de alto impacto narrativo y predictivo para transmisiones en vivo, coberturas previas y análisis pospartido.

Disponemos de tres fuentes transaccionales clave:
- `Match_Results.csv`: Resultados a nivel de partido (fecha, contendientes, goles, torneo, sede, neutralidad).
- `Goal_Scorers.csv`: Eventos atómicos de gol (minuto, anotador, gol en contra, penal).
- `Penalty_Shootouts.csv`: Desenlace de partidos definidos por tiros desde el punto de penal.

---

## 2. Definición Formal de Objetivos de Negocio

### Objetivo de Negocio 1 (Predictivo)
* **Nombre:** Anticipación de Probabilidad de Victoria / Desenlace en Partidos Internacionales.
* **Declaración del Problema:** Predecir con antelación el desenlace de un enfrentamiento internacional (Victoria Local, Empate o Victoria Visitante / Desenlace en llaves eliminatorias directas) a partir del rendimiento histórico, métricas de gol, jerarquía reciente, estatus de localía y tipo de torneo.
* **Impacto y Valor de Negocio:**
  - **Para la Cadena Mediática:** Generación en tiempo real de "Win Probability" previa al encuentro, dinamización de la experiencia del espectador y diseño de cuotas analíticas/paneles informativos.
  - **Para la Federación/Cuerpos Técnicos:** Evaluación del riesgo y probabilidad esperada frente a rivales directos en torneos oficiales y preparación táctica.
* **Target / Variable Objetivo:** Resultado del encuentro (`home_win`, `draw`, `away_win`) o clasificación a la siguiente ronda en series definitorias.
* **Criterio de Éxito Técnico/Negocio:** Lograr un modelo predictivo con desempeño significativamente superior al baseline aleatorio/mayoritario (ej. Macro F1-score > 0.55 y Accuracy > 55-60% en clasificación tri-clase), evitando fugas de información (*data leakage*) de eventos que ocurren durante el partido mismo.

---

### Objetivo de Negocio 2 (Descriptivo)
* **Nombre:** Caracterización, Tipificación y Segmentación de Eras y Torneos según Perfiles de Competitividad y Efectividad Goleadora.
* **Declaración del Problema:** Descubrir agrupamientos naturales (clústeres) y patrones latentes entre torneos, confederaciones y épocas históricas en función de variables de intensidad goleadora, paridad competitiva, distribución temporal del gol (primer tiempo vs. segundo tiempo), dependencia de tiros penales y frecuencia de definiciones por tanda de penales.
* **Impacto y Valor de Negocio:**
  - **Para la Cadena Mediática:** Producir narrativas basadas en datos ("Storytelling Data-Driven") sobre cómo ha evolucionado el fútbol moderno frente a eras pasadas y qué torneos o rivalidades son objetivamente más disputados o espectaculares.
  - **Para la Federación:** Analizar el impacto de cambios de reglas históricas (ej. introducción de tarjetas, sustituciones, era del VAR, valor del gol de visitante) en el estilo y paridad del juego mundial.
* **Técnica Minera Asociada:** Agrupamiento no supervisado (Clustering K-Means / Jerárquico) y Reglas de Asociación.
* **Criterio de Éxito Técnico/Negocio:** Obtención de clústeres bien cohesionados y diferenciados (Silhouette Score validado), con interpretaciones claras y de valor analítico sustancial para el dominio futbolístico.

---

## 3. Matriz de Mapeo Dominio a KDD

| Dimensión | Objetivo Predictivo | Objetivo Descriptivo |
| :--- | :--- | :--- |
| **Pregunta de Negocio** | ¿Qué selección tiene mayor probabilidad de ganar un partido dadas sus métricas históricas y contexto de sede? | ¿Qué perfiles o arquetipos de competitividad existen entre las distintas eras y torneos del fútbol mundial? |
| **Tipo de Tarea KDD** | Supervisada (Clasificación Multiclase) | No Supervisada (Clustering / Segmentación y Reglas de Asociación) |
| **Entidad de Análisis** | Encuentro deportivo individual ($M_i$) con histórico acumulado previo. | Agrupaciones de torneos, eras históricas y selecciones. |
| **Métricas Clave** | Diferencial de gol previo, tasa de victorias histórica, localía, tipo de torneo, confederación. | Promedio de goles/partido, % penales, balance primer/segundo tiempo, índice de paridad, frecuencia de shootouts. |
| **Criterio de Evaluación** | Accuracy, Precision, Recall, Macro F1, Matriz de Confusión. | Coeficiente de Silueta, Inercia / Codo, Interpretabilidad temática de perfiles. |
