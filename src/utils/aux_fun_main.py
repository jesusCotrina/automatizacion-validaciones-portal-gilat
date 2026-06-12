import json
import pkgutil
import importlib
import inspect
import os
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def discover_reportes():
    try:
        reportes = {}

        for root, _, files in os.walk("validaciones"):

            tipo_reporte = os.path.basename(root)

            for file in files:

                if not file.endswith(".py"):
                    continue

                if file == "__init__.py":
                    continue

                codigo_reporte = file.split("_", 1)[0]

                ruta = os.path.join(root, file)
                module_name = file[:-3]

                spec = importlib.util.spec_from_file_location(
                    module_name,
                    ruta
                )

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for _, obj in inspect.getmembers(
                    module,
                    inspect.isclass
                ):
                    if obj.__module__ == module.__name__:
                        codigo_tipo_reporte = str(tipo_reporte.split("_")[0])
                        if codigo_tipo_reporte not in reportes:
                            reportes[codigo_tipo_reporte] = []

                        reportes[codigo_tipo_reporte].append({
                            "codigo": codigo_reporte,
                            "Objeto_reporte": obj()
                        })

        return reportes
    
    except Exception as e:
        mensaje=f"Error explorando reportes \nError:{e}"
        logger.error(mensaje)
        raise RuntimeError(mensaje)

def crear_actualizar_resultados(resultados_totales,periodo):
    periodo_carpeta = periodo[:7]

    ruta_archivo = Path(
        f"../resultados/{periodo_carpeta}/control_resumen/resultados_totales.json"
    )

    if not ruta_archivo.exists():
        # Crea las carpetas si no existen
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

        # Crea el archivo
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(resultados_totales, f, ensure_ascii=False, indent=4)

        logger.info(f"Archivo creado: {ruta_archivo}")

    else:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos_existentes = json.load(f)

        # Actualizar solo las llaves recibidas
        for key, value in resultados_totales.items():
            datos_existentes[key] = value

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos_existentes, f, ensure_ascii=False, indent=4)

        logger.info(f"Archivo actualizado: {ruta_archivo}")

    return ruta_archivo

def generar_tabla_resumen (ruta_archivo,config):
    
    with open(ruta_archivo, encoding="utf-8") as f:
        resultados_totales = json.load(f)

    with open("./maestros/maestro_tipo_reporte.json", encoding="utf-8") as f:
        tipos_reporte = json.load(f)
    
    with open("./maestros/maestro_nombre_reportes.json", encoding="utf-8") as f:
        reportes_maestro = json.load(f)

    regiones = list(config["regiones"].keys())

    filas = {}

    for _, resultado in resultados_totales.items():

        tecnologia = resultado["tecnologia"]
        tipo_reporte = resultado["tipo_reporte"]
        codigo_reporte = resultado["codigo_reporte"]
        region = resultado["region"]

        key = (
            tecnologia,
            tipo_reporte,
            codigo_reporte
        )

        if key not in filas:

            filas[key] = {
                "Tecnologia": tecnologia,
                "Tipo Reporte": tipos_reporte.get(
                    tipo_reporte,
                    tipo_reporte
                ),
                "Nombre Reporte": reportes_maestro.get(
                    codigo_reporte,
                    {}
                ).get(
                    "nombre",
                    codigo_reporte
                ),
                "Comentarios": "",
                "Fecha Entrega": ""
            }

            for r in regiones:
                filas[key][r] = ""

        filas[key][region] = resultado["estado"]

        observaciones = resultado.get(
            "observaciones",
            []
        )

        if observaciones:

            texto_obs = " | ".join(
                str(x)
                for x in observaciones
            )

            if filas[key]["Comentarios"]:
                filas[key]["Comentarios"] += (
                    f"\n[{region}] {texto_obs}"
                )
            else:
                filas[key]["Comentarios"] = (
                    f"[{region}] {texto_obs}"
                )

    columnas = [
        "Tecnologia",
        "Tipo Reporte",
        "Nombre Reporte",
        *regiones,
        "Fecha Entrega",
        "Comentarios"
    ]

    df = pd.DataFrame(
        filas.values()
    )[columnas]

    return df

def generar_tabla_correo(resultados_totales):

    regiones = {}

    # Agrupar estados y tecnologías por región
    for resultado in resultados_totales.values():

        region = resultado["region"]
        estado = resultado["estado"]
        tecnologia = resultado["tecnologia"]

        if region not in regiones:
            regiones[region] = {
                "estados": [],
                "tecnologias": set()
            }

        regiones[region]["estados"].append(estado)
        regiones[region]["tecnologias"].add(tecnologia)

    resumen = []

    # Generar resultado final
    for region, data in regiones.items():

        estados = data["estados"]
        tecnologias_texto = ", ".join(
            sorted(data["tecnologias"])
        )

        # Prioridad: ERROR > OBSERVADO > VALIDADO
        if "ERROR" in estados:

            estado_final = "ERROR"

            mensaje = (
                f"Se ejecutó la validación de todos los reportes SSRA para las tecnologías "
                f"{tecnologias_texto}. "
                f"Hubo uno o más errores durante la validación. "
                f"Por favor revisar el archivo de resumen para obtener el detalle."
            )

        elif "OBSERVADO" in estados:

            estado_final = "OBSERVADO"

            mensaje = (
                f"Se ejecutó la validación de todos los reportes SSRA para las tecnologías "
                f"{tecnologias_texto}. "
                f"Se encontraron observaciones en algunos reportes. "
                f"Por favor revisar el archivo de resumen para obtener el detalle."
            )

        else:

            estado_final = "VALIDADO"

            mensaje = (
                f"Se ejecutó la validación de todos los reportes SSRA para las tecnologías "
                f"{tecnologias_texto}. "
                f"Todos los reportes fueron validados correctamente."
            )

        resumen.append({
            "region": region,
            "estado": estado_final,
            "mensaje": mensaje
        })

    return resumen