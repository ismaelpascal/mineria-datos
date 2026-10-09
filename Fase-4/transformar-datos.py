#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script de la Fase 4: Transformación y Reducción de Datos (Feature Engineering)

Objetivo:
- Derivación temporal: Eras históricas, estacionalidad (mes, día, década).
- Mapeo geográfico de confederaciones FIFA (UEFA, CONMEBOL, CONCACAF, CAF, AFC, OFC, Regional/Non-FIFA).
- Agregación estructural de métricas futbolísticas por partido:
  * Ratios de efectividad: ratio 1° tiempo vs 2° tiempo, ratio penales/goles.
  * Dominancia local: home_goal_ratio.
  * Indicador de paridad: abs(goal_difference).
  * Clasificación de nivel de torneo (Mundial, Torneo Continental Oficial, Clasificatoria, Amistoso).
- Codificación y reducción de dimensionalidad:
  * Generar variables One-Hot Encoding para modelos lineales y de agrupamiento.
  * Generar matrices limpias preparadas para Minería (Fase 5, 6 y 7).
- Exportar:
  * 1-dataset-transformado.csv (dataset maestro transformado con todas las features)
  * 2-matriz-mineria.csv (matriz numérica codificada y normalizada lista para algoritmos)
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Rutas dinámicas
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
CLEAN_DATAMART_PATH = BASE_DIR / "Fase-3" / "1-datamart-limpio.csv"
OUTPUT_TRANSFORMED_PATH = SCRIPT_DIR / "1-dataset-transformado.csv"
OUTPUT_MATRIX_PATH = SCRIPT_DIR / "2-matriz-mineria.csv"

# Diccionarios de Confederaciones FIFA
UEFA = {'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina',
        'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Czechoslovakia', 'Denmark', 'England', 'Estonia',
        'Faroe Islands', 'Finland', 'France', 'Georgia', 'German DR', 'Germany', 'Gibraltar', 'Greece', 'Hungary',
        'Iceland', 'Israel', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
        'Malta', 'Moldova', 'Montenegro', 'Netherlands', 'North Macedonia', 'Northern Ireland', 'Norway', 'Poland',
        'Portugal', 'Republic of Ireland', 'Romania', 'Russia', 'San Marino', 'Scotland', 'Serbia', 'Slovakia',
        'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'Wales', 'Yugoslavia'}

CONMEBOL = {'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela'}

CONCACAF = {'Anguilla', 'Antigua and Barbuda', 'Aruba', 'Bahamas', 'Barbados', 'Belize', 'Bermuda', 'Bonaire',
            'British Virgin Islands', 'Canada', 'Cayman Islands', 'Costa Rica', 'Cuba', 'Curaçao', 'Dominica',
            'Dominican Republic', 'El Salvador', 'French Guyana', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guyana',
            'Haiti', 'Honduras', 'Jamaica', 'Martinique', 'Mexico', 'Montserrat', 'Nicaragua', 'Panama', 'Puerto Rico',
            'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Vincent and the Grenadines', 'Sint Maarten',
            'Suriname', 'Trinidad and Tobago', 'Turks and Caicos Islands', 'United States', 'US Virgin Islands'}

CAF = {'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde',
       'Central African Republic', 'Chad', 'Comoros', 'Congo', 'DR Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea',
       'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast',
       'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco',
       'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'São Tomé and Príncipe', 'Senegal', 'Seychelles',
       'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda',
       'Zambia', 'Zanzibar', 'Zimbabwe'}

AFC = {'Afghanistan', 'Australia', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Burma', 'Cambodia', 'China PR',
       'East Timor', 'Guam', 'Hong Kong', 'India', 'Indonesia', 'Iran', 'Iraq', 'Japan', 'Jordan', 'Kuwait',
       'Kyrgyzstan', 'Laos', 'Lebanon', 'Macau', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea',
       'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka',
       'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam',
       'Vietnam Republic', 'Yemen', 'Yemen DPR'}

OFC = {'American Samoa', 'Cook Islands', 'Fiji', 'Kiribati', 'New Caledonia', 'New Zealand', 'Papua New Guinea',
       'Samoa', 'Solomon Islands', 'Tahiti', 'Tonga', 'Tuvalu', 'Vanuatu'}

def get_confederation(team: str) -> str:
    if team in UEFA:
        return "UEFA"
    if team in CONMEBOL:
        return "CONMEBOL"
    if team in CONCACAF:
        return "CONCACAF"
    if team in CAF:
        return "CAF"
    if team in AFC:
        return "AFC"
    if team in OFC:
        return "OFC"
    return "Other/Regional"

def get_tournament_tier(tournament: str) -> str:
    t_lower = tournament.lower()
    if "fifa world cup" in t_lower and "qualification" not in t_lower:
        return "World_Cup_Finals"
    elif "qualification" in t_lower:
        return "Qualifiers"
    elif any(k in t_lower for k in ["copa américa", "uefa euro", "african cup of nations", "asian cup", "gold cup", "nations cup", "nations league"]):
        return "Continental_Championship"
    elif "friendly" in t_lower:
        return "Friendly"
    else:
        return "Regional_Tournament"

def transform_data():
    print("[1/5] Cargando dataset limpio de Fase 3...")
    df = pd.read_csv(CLEAN_DATAMART_PATH)
    print(f"  - Filas cargadas: {len(df):,}")

    # ==========================================================
    # 1. DERIVACIÓN TEMPORAL Y ERAS HISTÓRICAS
    # ==========================================================
    print("[2/5] Derivando variables temporales y Eras históricas...")
    dt = pd.to_datetime(df["date"])
    df["year"] = dt.dt.year
    df["month"] = dt.dt.month
    df["day_of_week"] = dt.dt.day_name()
    df["decade"] = (df["year"] // 10) * 10

    # Eras Históricas del Fútbol Internacional
    era_conditions = [
        df["year"] < 1945,
        (df["year"] >= 1945) & (df["year"] < 1970),
        (df["year"] >= 1970) & (df["year"] < 1998),
        (df["year"] >= 1998) & (df["year"] < 2018),
        df["year"] >= 2018
    ]
    era_labels = [
        "Pre_Guerra",           # 1872 - 1944: Inicios y entreguerras
        "Post_Guerra_Clasica",  # 1945 - 1969: Consolidación FIFA y Pelé
        "Era_Moderna",          # 1970 - 1997: Fútbol total y tarjetas amarillas/rojas
        "Era_Global_Digital",   # 1998 - 2017: Expansión de cupos y globalización
        "Era_VAR"               # 2018 - Presente: Tecnología y revisión en video
    ]
    df["era"] = np.select(era_conditions, era_labels, default="Unknown")

    # ==========================================================
    # 2. CONFEDERACIONES Y NIVELES DE TORNEO
    # ==========================================================
    print("[3/5] Mapeando confederaciones geográficas y jerarquía de torneo...")
    df["home_confederation"] = df["home_team"].apply(get_confederation)
    df["away_confederation"] = df["away_team"].apply(get_confederation)
    df["is_intercontinental"] = df["home_confederation"] != df["away_confederation"]
    df["tournament_tier"] = df["tournament"].apply(get_tournament_tier)

    # ==========================================================
    # 3. AGREGACIÓN ESTRUCTURAL Y MÉTRICAS DE RENDIMIENTO
    # ==========================================================
    print("[4/5] Computando métricas y ratios estructurales del partido...")
    # Dominio del gol local y visitante
    df["home_goal_share"] = np.where(df["total_goals"] > 0, df["home_score"] / df["total_goals"], 0.5)
    df["abs_goal_diff"] = df["goal_difference"].abs()
    
    # Ratios de distribución temporal de goles (cuando se dispone de Goal_Scorers)
    df["first_half_ratio"] = np.where(df["total_recorded_goals"] > 0, df["goals_first_half"] / df["total_recorded_goals"], 0.0)
    df["second_half_ratio"] = np.where(df["total_recorded_goals"] > 0, df["goals_second_half"] / df["total_recorded_goals"], 0.0)
    df["penalty_goal_ratio"] = np.where(df["total_recorded_goals"] > 0, df["penalty_goals"] / df["total_recorded_goals"], 0.0)

    # Exportar dataset enriquecido maestro
    df.to_csv(OUTPUT_TRANSFORMED_PATH, index=False)
    print(f"  - Dataset transformado guardado en: {OUTPUT_TRANSFORMED_PATH}")

    # ==========================================================
    # 4. CREACIÓN DE LA MATRIZ NUMÉRICA PARA MINERÍA (REDUCCIÓN Y CODIFICACIÓN)
    # ==========================================================
    print("[5/5] Construyendo matriz numérica codificada para algoritmos KDD...")
    
    # One-Hot Encoding de variables categóricas esenciales
    cat_cols = ["era", "tournament_tier", "home_confederation", "away_confederation"]
    ohe_df = pd.get_dummies(df[cat_cols], prefix=cat_cols, dtype=int)

    # Variables numéricas y booleanas directas
    num_cols = [
        "neutral", "is_intercontinental", "year", "month",
        "home_score", "away_score", "total_goals", "goal_difference", "abs_goal_diff",
        "has_penalty_shootout", "has_scorer_details",
        "goals_first_half", "goals_second_half", "penalty_goals",
        "is_outlier_mild", "is_outlier_extreme"
    ]
    numeric_part = df[num_cols].astype(int)

    # Target supervisado
    target_part = df[["match_id", "match_outcome"]]

    mining_matrix = pd.concat([target_part, numeric_part, ohe_df], axis=1)
    mining_matrix.to_csv(OUTPUT_MATRIX_PATH, index=False)
    print(f"  - Matriz analítica para minería guardada en: {OUTPUT_MATRIX_PATH}")
    print(f"✅ ¡Fase 4 finalizada! Matriz lista con {mining_matrix.shape[0]:,} filas y {mining_matrix.shape[1]} columnas.")

if __name__ == "__main__":
    transform_data()
