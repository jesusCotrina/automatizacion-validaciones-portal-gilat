# ================================================================================================================================
# IMPORTACION DE LIBRERIAS  ==========================     
# ================================================================================================================================
import pandas as pd
from utils.aux_fun  import *


# ================================================================================================================================
# ================================================================================================================================

class RptIndicadorVelocidadBajada01():

    def __init__(self):
        #self.maestro_ips    = open ("/maestros/maestro_ips.json", "r").read()


        pass

    def execute(self, region, tecnologia):
        self.execute_ftth(region,tecnologia)
        
        if tecnologia == "FTTH":
            print("ejecutando FTTH",region,tecnologia)
            return self.execute_ftth(region,tecnologia)

        
        elif region == "APURIMAC" and tecnologia == "FTTH":
            print("ejecutando APURIMAC FTTH",region,tecnologia)
            return self.execute_apurimac_ftth(region,tecnologia)

        else:
            return {}
    

    def execute_ftth(self,region, tecnologia):
        # ================================================================================================================================
        # LECTURA DE MAESTROS Y VARIABLES ==========================     
        # ================================================================================================================================
        A = open("/maestros/maestro_A.json", "r").read()    
        observaciones= ["observacion1","observacion2"]

    def execute_rf(self,region, tecnologia):

        # Logica
        pass
    
    def execute_apurimac_ftth(self):

        # Logica
        pass