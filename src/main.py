import json
from validation import Validation

import pkgutil
import importlib
import inspect


## VARIABLES GLOBALES
path_config = "..\config.json"
package_name = "validaciones"

def discover_reportes():
    reportes = []
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.walk_packages(
        package.__path__,
        package.__name__ + "."
    ):

        module = importlib.import_module(module_name)

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass
        ):

            # Solo clases definidas en este módulo
            if obj.__module__ == module.__name__:
                reportes.append(obj())

    return reportes



def main ():
    with open(path_config) as f:
        config = json.load(f)

    resultados  = []
    reportes    =  discover_reportes()

    for region in config.keys():

        for tecnologia in region["tecnologias"]:

            for reporte in reportes:

                resultado = reporte.execute(
                    region,
                    tecnologia
                )

                if resultado:
                    resultados.append(resultado)