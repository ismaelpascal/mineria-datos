# Esquema del Target Dataset (Data Mart Consolidado)

## 1. Justificación y Necesidad del Dataset Consolidado
Los datos originales estaban distribuidos en tres archivos transaccionales con **diferentes niveles de granularidad**:
1. **`Match_Results.csv`**: Granularidad a nivel de encuentro (1 fila = 1 partido).
2. **`Goal_Scorers.csv`**: Granularidad a nivel de evento atómico (1 fila = 1 gol registrado).
3. **`Penalty_Shootouts.csv`**: Granularidad condicional (1 fila = 1 definición por penales en partidos empatados en fases de eliminación).

Para aplicar algoritmos de minería de datos supervisada y no supervisada (KDD), se requería un **Data Mart tabular unificado** a granularidad única de partido ($M_i$), enriquecido con las métricas derivadas de goles y definiciones por penales.

---

## 2. Llaves Primarias y Foráneas (Mapeo Relacional)

* **Clave Primaria Canónica Asignada:** `match_id` (identificador secuencial único con formato `M_000001`, `M_000002`, ...).
* **Clave Compuesta Natural de Enlace:** `[date, home_team, away_team]`
  - En `Goal_Scorers.csv`: Clave foránea referenciando el encuentro en el que ocurrió el gol.
  - En `Penalty_Shootouts.csv`: Clave foránea referenciando el partido que requirió desempate por penales.
* **Tratamiento de Duplicados en Matches:**
  - Se detectaron 20 registros duplicados en `Match_Results.csv` (partidos idénticos de torneos amistosos tempranos de la década de 1920-1930). Se aplicó desduplicación exacta conservando la primera ocurrencia representativa (quedando 47,396 partidos consolidados).

---

## 3. Diccionario de Datos del Archivo: `1-datamart-partidos.csv`

| Columna | Tipo de Dato | Origen / Regla de Creación | Descripción |
| :--- | :--- | :--- | :--- |
| `match_id` | Texto (PK) | Generado sintéticamente | Identificador unívoco del partido. |
| `date` | Fecha (`YYYY-MM-DD`) | `Match_Results.csv` | Fecha en la que se disputó el encuentro. |
| `home_team` | Texto | `Match_Results.csv` | Nombre de la selección local. |
| `away_team` | Texto | `Match_Results.csv` | Nombre de la selección visitante. |
| `home_score` | Entero | `Match_Results.csv` | Goles anotados por el equipo local. |
| `away_score` | Entero | `Match_Results.csv` | Goles anotados por el equipo visitante. |
| `total_goals` | Entero | Calculado (`home_score + away_score`) | Total de goles convertidos en el encuentro. |
| `goal_difference` | Entero | Calculado (`home_score - away_score`) | Diferencial de gol para el local. |
| `match_outcome` | Categórico | Regla condicional | Resultado: `HOME_WIN`, `DRAW`, `AWAY_WIN`. |
| `tournament` | Categórico | `Match_Results.csv` | Competición disputada (Mundial, Copa América, etc.). |
| `city` | Texto | `Match_Results.csv` | Ciudad donde se disputó. |
| `country` | Texto | `Match_Results.csv` | País anfitrión. |
| `neutral` | Booleano | `Match_Results.csv` | Si se jugó en campo neutral. |
| `has_scorer_details` | Booleano | Cruce con `Goal_Scorers.csv` | Indica si el partido cuenta con detalle de goles. |
| `total_recorded_goals` | Entero | Agregación de `Goal_Scorers` | Cantidad de goles registrados en el detalle. |
| `home_recorded_goals` | Entero | Agregación de `Goal_Scorers` | Goles registrados correspondientes al local. |
| `away_recorded_goals` | Entero | Agregación de `Goal_Scorers` | Goles registrados correspondientes al visitante. |
| `penalty_goals` | Entero | Agregación de `Goal_Scorers` | Goles convertidos de penal durante el juego. |
| `own_goals` | Entero | Agregación de `Goal_Scorers` | Autogoles registrados en el encuentro. |
| `goals_first_half` | Entero | Agregación de `Goal_Scorers` | Goles anotados en el primer tiempo ($\le$ 45 min). |
| `goals_second_half` | Entero | Agregación de `Goal_Scorers` | Goles anotados en el segundo tiempo (46 a 90 min). |
| `goals_extra_time` | Entero | Agregación de `Goal_Scorers` | Goles anotados en tiempo suplementario (> 90 min). |
| `unique_scorers` | Entero | Agregación de `Goal_Scorers` | Cantidad de jugadores distintos que anotaron. |
| `has_penalty_shootout` | Booleano | Cruce con `Penalty_Shootouts.csv` | Si el partido llegó a tanda de penales. |
| `shootout_winner` | Texto | `Penalty_Shootouts.csv` | Selección ganadora de la tanda de penales. |
| `shootout_first_shooter` | Texto | `Penalty_Shootouts.csv` | Equipo que ejecutó el primer penal. |

---

## 4. Instrucción para Visualización en VisiData (`vd`)
Para inspeccionar de forma interactiva y realizar filtros o cálculos rápidos sobre este Data Mart, ejecuta en tu terminal:

```bash
vd /home/ddl/Descargas/Datos/Fase-2/1-datamart-partidos.csv
```
*(Presiona `Shift + F` para frecuencias de columnas, `F` sobre una columna para histograma rápido, o `[` / `]` para ordenar).*
