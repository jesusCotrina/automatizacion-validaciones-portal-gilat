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
        pass

    def execute_rf(self,region,tecnologia):
        observaciones= ["observacion8","observacion10"]
        # Logica
        return {"observaciones":observaciones, "estado":"OBSERVADO"}
    
    def execute_apurimac(self):

        # Logica
        pass