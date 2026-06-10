import pandas as pd
import os
import inspect
import importlib.util
import json

carpeta_base = "validaciones"

def buscar_clase(cod_reporte):
    cod_reporte = str(cod_reporte)

    # Recorrer todas las carpetas dentro de validaciones
    for carpeta in os.listdir(carpeta_base):

        ruta_carpeta = os.path.join(carpeta_base, carpeta)

        if not os.path.isdir(ruta_carpeta):
            continue

        for archivo in os.listdir(ruta_carpeta):

            if (
                archivo.endswith(".py")
                and archivo.startswith(f"{cod_reporte}_")
            ):

                ruta_archivo = os.path.join(ruta_carpeta, archivo)

                # Importar módulo dinámicamente
                spec = importlib.util.spec_from_file_location(
                    archivo[:-3],
                    ruta_archivo
                )

                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)

                # Obtener la única clase definida en el archivo
                clases = [
                    obj
                    for _, obj in inspect.getmembers(modulo, inspect.isclass)
                    if obj.__module__ == modulo.__name__
                ]

                if len(clases) == 0:
                    raise Exception(
                        f"No se encontró ninguna clase en {ruta_archivo}"
                    )

                if len(clases) > 1:
                    raise Exception(
                        f"Se encontraron múltiples clases en {ruta_archivo}"
                    )

                return clases[0]()

    raise Exception(
        f"No se encontró ningún archivo para el código {cod_reporte}"
    )

def generar_correos(resultados):
    a=0



def main():
    config_manual = open ("../ejecucion manual/config_manual.json", "r").read()
    config_manual = json.loads(config_manual)
    print("Ejecutando main")
    try:
        if config_manual["codigo_reporte"] == "all":
            print("Ejecutando todos los reportes")
            # Lógica para ejecutar todos los reportes
            pass
        
        else:
            clase   =  buscar_clase(config_manual["codigo_reporte"])
            resultados= clase.execute(config_manual["region"], config_manual["tecnologia"])
            generar_correos(resultados)


    except Exception as e:
        print(f"Error en main: {e}")

if __name__ == "__main__":
    main()