import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd

from utils.logger import *
from utils.email import *
from utils.aux_fun_main import * 
from utils.excel import *
# ======================================================
## VARIABLES GLOBALES
path_config     = "../config.json"
package_name    = "validaciones"

# ======================================================
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.dirname(BASE_DIR)
log_file_name=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logger = setup_logger(name="main",log_file=log_file_name,base_dir=BASE_DIR,log_path="logs")


def get_config_periodo():
    try:
        with open(path_config) as f:
                config = json.load(f)

        
        now = datetime.now()

        if now.month == 1:
            periodo = f"{now.year - 1}-12-01"
        else:
            periodo = f"{now.year}-{now.month - 1:02d}-01"

        return config,periodo
    
    except Exception as e:
        mensaje=f"Error obteniendo leyendo en alrchivo config y periodo \nError:{e}"
        logger.error(mensaje)
        raise RuntimeError(mensaje)

def main ():
    try:
        logger.info("INICIANDO NUEVO PROCESO DE VALIDACION ================================================================")
        logger.info("="*100)

        config,periodo  = get_config_periodo()
        reportes        = discover_reportes()

        resultados_totales={}
        for region in config["regiones"].keys():
            for tecnologia in config["regiones"][region]["tecnologias"]:

                for tipo_reporte, lista_reportes in reportes.items():
                    
                    for item in lista_reportes:
                        resultado_json=item["Objeto_reporte"].execute(region, tecnologia,periodo)

                        if resultado_json:
                            tecnologia= resultado_json.get("tecnologia",tecnologia)
                            codigo_reporte_row = f"{region}_{item["codigo"]}_{tecnologia}"
                            resultado_json.update({"region": region, "tecnologia": tecnologia, "tipo_reporte": tipo_reporte, "codigo_reporte": item["codigo"]})
                            resultados_totales[codigo_reporte_row] = resultado_json
                        

        ruta_archivo    = crear_actualizar_resultados(resultados_totales,periodo)
        tabla_resumen   = generar_tabla_resumen(ruta_archivo,config)
        path_resumen    = generar_excel_formato(tabla_resumen,periodo)
        
        destinatarios   = destinatarios = ",".join(config["destinatarios"])
        resumen_correo  = generar_tabla_correo(resultados_totales)
        estado          = enviar_correo(resultados=resumen_correo,asunto="Validacion de reportes SSRA",destinatarios=destinatarios,path_archivo=path_resumen)
        logger.info("PROCESO FINALIZADO ================================================================")
        logger.info("="*100)

    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()