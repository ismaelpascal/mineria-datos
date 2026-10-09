# Bitácora de Preprocesamiento

**Proyecto:** Minería de Datos sobre resultados internacionales de fútbol  
**Fase KDD:** Preprocesamiento y limpieza de datos  
**Archivos fuente auditados:**

| Archivo | Descripción | Volumen auditado |
|---|---:|---:|
| `Match_Results.csv` | Resultados históricos de partidos internacionales | 47,396 partidos consolidados |
| `Goal_Scorers.csv` | Detalle de goles, minuto y jugador anotador | 44,362 goles registrados |
| `Penalty_Shootouts.csv` | Definiciones por penales | 644 tandas de penales |

**Archivo limpio generado:** `Fase-3/1-datamart-limpio.csv`  
**Archivo de auditoría de outliers:** `Fase-3/2-partidos-outliers-extremos.csv`

---

## 1. Objetivo de la limpieza

El objetivo del preprocesamiento fue transformar los tres archivos `.csv` originales en un corpus analítico confiable para minería de datos, conservando la mayor cantidad posible de información histórica y evitando eliminar registros válidos.

La regla general adoptada fue:

> Si un dato faltante no invalida el resultado deportivo del partido, se conserva el registro y se documenta la ausencia mediante una regla técnica explícita.

---

## 2. Resumen de hallazgos

| Problema detectado | Archivo de origen | Columna | Cantidad de registros | Regla técnica aplicada |
|---|---|---|---:|---|
| Minuto de gol faltante | `Goal_Scorers.csv` | `minute` | 259 | Se conserva el gol en el conteo total, pero no se asigna artificialmente a primer o segundo tiempo. |
| Nombre de goleador faltante | `Goal_Scorers.csv` | `scorer` | 49 | Se conserva el gol; el jugador no se contabiliza dentro de `unique_scorers`. |
| Primer ejecutor de penales faltante | `Penalty_Shootouts.csv` | `first_shooter` | 414 | Se imputa una categoría semántica de ausencia: `Not_Recorded`. |
| Partidos sin tanda de penales | Data Mart consolidado | `shootout_winner` | 46,753 | Se codifica como `None`, porque el partido no tuvo definición por penales. |
| Goleadas atípicas leves | Data Mart consolidado | `total_goals` | 807 | Se marcan con `is_outlier_mild = True`; no se eliminan. |
| Goleadas atípicas extremas | Data Mart consolidado | `total_goals` | 86 | Se marcan con `is_outlier_extreme = True` y se exportan a un archivo separado de auditoría. |

---

## 3. Tratamiento de valores nulos

### 3.1. Minutos de gol faltantes

**Tabla usada:** `Goal_Scorers.csv`  
**Columna auditada:** `minute`  
**Registros nulos encontrados:** **259**

Estos registros corresponden a goles reales donde la fuente histórica no registró el minuto exacto. La eliminación de estos goles habría alterado el resultado real de los partidos y habría reducido artificialmente el volumen de goles.

**Regla técnica aplicada:**

- No se elimina el gol.
- No se imputa con media ni mediana, porque eso concentraría artificialmente goles alrededor del minuto promedio.
- El gol se conserva en los conteos globales.
- No se asigna a variables temporales como `goals_first_half` o `goals_second_half` cuando el minuto es desconocido.

**Justificación:**  
La prioridad fue preservar la validez deportiva del resultado. Imputar todos los minutos faltantes con un valor central habría introducido un patrón falso en la distribución temporal de goles.

---

### 3.2. Nombres de goleadores faltantes

**Tabla usada:** `Goal_Scorers.csv`  
**Columna auditada:** `scorer`  
**Registros nulos encontrados:** **49**

Algunos partidos registran el resultado y los goles, pero no el nombre del jugador anotador.

**Regla técnica aplicada:**

- Se conserva el registro del gol.
- El gol sigue aportando al conteo total del partido.
- El valor nulo no se fuerza con una etiqueta artificial de jugador.
- En métricas de diversidad de goleadores, como `unique_scorers`, solo se cuentan nombres válidos no nulos.

**Justificación:**  
Inventar un nombre o una categoría de jugador alteraría las métricas de diversidad ofensiva. La ausencia del nombre no invalida el hecho deportivo del gol.

---

### 3.3. Primer ejecutor de penales faltante

**Tabla usada:** `Penalty_Shootouts.csv`  
**Columna auditada:** `first_shooter`  
**Registros nulos encontrados:** **414**

La columna indica qué selección pateó primero en la tanda de penales. En muchas tandas antiguas, la fuente no registra este detalle.

**Regla técnica aplicada:**

- Se conserva la tanda de penales.
- Cuando hubo tanda pero no se conoce el primer ejecutor, se usa la categoría `Not_Recorded`.

**Justificación:**  
La ausencia del primer pateador no impide analizar que el partido llegó a penales ni quién ganó la definición. Por eso se preserva el registro y se explicita la falta de cobertura histórica.

---

### 3.4. Partidos sin tanda de penales

**Tabla usada:** Data Mart consolidado desde `Match_Results.csv` + `Penalty_Shootouts.csv`  
**Columna auditada:** `shootout_winner`  
**Registros sin tanda de penales:** **46,753**

La mayoría de los partidos no terminó en tanda de penales. En esos casos, la ausencia de ganador por penales no representa un error, sino que el evento no ocurrió.

**Regla técnica aplicada:**

- Los partidos sin tanda se codifican como `None` en `shootout_winner`.
- Esta codificación separa conceptualmente la ausencia del evento de un dato faltante real.

**Justificación:**  
No debe confundirse “no hubo penales” con “hubo penales, pero falta el dato”. Esta distinción evita sesgos en el análisis de eliminatorias y torneos con definición por penales.

---

## 4. Tratamiento de datos atípicos

### 4.1. Variable auditada

**Tabla usada:** `Fase-3/1-datamart-limpio.csv`  
**Columna auditada:** `total_goals`  
**Definición:**

```text
total_goals = home_score + away_score
```

---

### 4.2. Regla estadística utilizada

Se aplicó el criterio de Tukey basado en rango intercuartílico:

```text
IQR = Q3 - Q1
Límite outlier leve = Q3 + 1.5 × IQR
Límite outlier extremo = Q3 + 3.0 × IQR
```

Con los datos observados:

| Estadístico | Valor |
|---|---:|
| Q1 | 1.0 gol |
| Mediana | 3.0 goles |
| Q3 | 4.0 goles |
| IQR | 3.0 goles |
| Límite outlier leve | 8.5 goles |
| Límite outlier extremo | 13.0 goles |

---

### 4.3. Outliers encontrados

| Tipo de outlier | Regla | Cantidad | Porcentaje aproximado |
|---|---|---:|---:|
| Outlier leve | `total_goals > 8.5` | 807 | 1.70% |
| Outlier extremo | `total_goals > 13.0` | 86 | 0.18% |

---

### 4.4. Decisión técnica

Los outliers no fueron eliminados del dataset principal porque representan partidos reales, no errores de captura. Por ejemplo, goleadas históricas en clasificatorias o torneos regionales reflejan diferencias reales de competitividad.

**Regla técnica aplicada:**

- Se conservan los partidos en `Fase-3/1-datamart-limpio.csv`.
- Se crean columnas de trazabilidad:
  - `is_outlier_mild`
  - `is_outlier_extreme`
- Se exportan los 86 casos extremos a `Fase-3/2-partidos-outliers-extremos.csv` para auditoría separada.

**Justificación:**  
Eliminar las goleadas extremas habría borrado conocimiento relevante sobre desigualdad competitiva entre selecciones y torneos. Marcarlas con flags permite que algoritmos sensibles a distancia, como K-Means, puedan tratarlas con cautela sin perder evidencia histórica.

---

## 5. Reglas de consistencia aplicadas

| Campo | Acción aplicada | Motivo |
|---|---|---|
| `home_team` | Limpieza de espacios con `.str.strip()` | Evitar duplicados por espacios invisibles. |
| `away_team` | Limpieza de espacios con `.str.strip()` | Evitar categorías espurias. |
| `tournament` | Limpieza de espacios con `.str.strip()` | Mantener consistencia en agrupamientos. |
| `city` | Limpieza de espacios con `.str.strip()` | Evitar duplicación geográfica artificial. |
| `country` | Limpieza de espacios con `.str.strip()` | Mantener consistencia territorial. |

---

## 6. Resultado final del preprocesamiento

| Archivo generado | Descripción | Filas |
|---|---|---:|
| `Fase-3/1-datamart-limpio.csv` | Dataset limpio principal con nulos tratados y flags de outliers. | 47,396 |
| `Fase-3/2-partidos-outliers-extremos.csv` | Subconjunto de goleadas extremas para auditoría. | 86 |

---

## 7. Conclusión de la bitácora

El preprocesamiento permitió conservar el valor histórico del corpus sin introducir imputaciones artificiales que distorsionaran los patrones deportivos. Los nulos fueron tratados según su significado semántico y los valores atípicos fueron preservados con trazabilidad explícita.

La decisión principal fue no eliminar información válida: los goles sin minuto, los goleadores no identificados y las goleadas extremas siguen siendo parte del fenómeno deportivo analizado. Esta estrategia mantiene la integridad del proceso KDD y deja evidencia técnica suficiente para auditoría posterior.
