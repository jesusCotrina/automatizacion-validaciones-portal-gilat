import json
import pkgutil
import importlib
import inspect
import os

## VARIABLES GLOBALES
path_config = "../config.json"
package_name = "validaciones"

def discover_reportes():
    reportes = []

    for root, _, files in os.walk("validaciones"):

        for file in files:

            if not file.endswith(".py"):
                continue

            if file == "__init__.py":
                continue

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
                    reportes.append(obj())

    return reportes


def main ():
    with open(path_config) as f:
        config = json.load(f)

    resultados  = []
    reportes    =  discover_reportes()
    print(f"Reportes encontrados: {[type(reporte).__name__ for reporte in reportes]}")
    for region in config["regiones"].keys():
        for tecnologia in config["regiones"][region]["tecnologias"]:

            for reporte in reportes:

                resultado = reporte.execute(
                    region,
                    tecnologia
                )

                if resultado:
                    resultados.append(resultado)

if __name__ == "__main__":
    main()