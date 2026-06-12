# ================================================================================================================================
# IMPORTACION DE LIBRERIAS  ==========================     
# ================================================================================================================================
import pandas as pd
from pathlib import Path


# ================================================================================================================================
# ================================================================================================================================

class RptIndicadorVelocidadSubida():

    def __init__(self):
        #self.maestro_ips    = open ("/../../maestros/maestro_ips.json", "r").read()

        pass

    def execute(self, region, tecnologia,periodo):

        if tecnologia == "FTTH":
            return self.execute_ftth(region,tecnologia)

        elif tecnologia == "RF":
            return self.execute_rf(region,tecnologia)

        else:
            return {}
    

    def execute_ftth(self,region, tecnologia):
        observaciones= ["observacion3","observacion4"]
        # Logica
        return {"observaciones":observaciones, "estado":"ERROR"}

    def execute_rf(self,region,tecnologia):

        # Logica
        pass
    
    def execute_apurimac(self):

        # Logica
        pass