#!/home/ddl/.local/share/kdd-venv/bin/python3
"""
Script exploratorio rápido (estilo VisiData) para la Fase 9.
Muestra el resumen ejecutivo de despliegue, SLAs y estrategia de monitoreo
a partir del archivo: 1-resumen-ejecutivo-despliegue.csv.
"""

from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "1-resumen-ejecutivo-despliegue.csv"

def main():
    if not CSV_PATH.exists():
        print("❌ Error: Ejecuta primero ./consolidar-despliegue.py")
        return

    df = pd.read_csv(CSV_PATH)

    print("\n" + "=" * 90)
    print("📊 TABLA RELEVANTE: PLAN EJECUTIVO DE DESPLIEGUE Y MONITORIZACIÓN KDD")
    print("📁 Archivo origen: 1-resumen-ejecutivo-despliegue.csv")
    print("💡 Para explorar en VisiData: vd Fase-9/1-resumen-ejecutivo-despliegue.csv")
    print("=" * 90)

    for _, r in df.iterrows():
        print(f"\n📌 {r['modulo']}: {r['kpi_componente']}")
        print(f"   ├─ Desempeño:        {r['desempeno_produccion']}")
        print(f"   ├─ Caso de Negocio:  {r['caso_de_uso']}")
        print(f"   ├─ SLA de Latencia:  {r['sla_latencia']}")
        print(f"   └─ Monitorización:   {r['estrategia_actualizacion']}")
    print("\n" + "=" * 90)

if __name__ == "__main__":
    main()
