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
            return self.execute_ftth(region,tecnologia,ip1,maestro_x)

        
        elif region == "APURIMAC" and tecnologia == "FTTH":
            print("ejecutando APURIMAC FTTH",region,tecnologia)
            return self.execute_apurimac_ftth(region,tecnologia,ip3,maestro_z)

        else:
            return {}
    





    def execute_ftth(self,region, tecnologia):
        # ================================================================================================================================
        # LECTURA DE MAESTROS Y VARIABLES ==========================     
        # ================================================================================================================================
        A = open("/maestros/maestro_A.json", "r").read()    
        observaciones= ["observacion1","observacion2"]


        # ================================================================================================================================
        # LOGICA DE VALIDACION ==========================     
        # ================================================================================================================================
        observaion=funcion_1() 
        
        observaion = funcion_2()
        funcion_3()


        # ================================================================================================================================
        # JSON DE RESULTADOS ==========================     
        # ================================================================================================================================
        if observaciones is None:
            estado = VALIDADO
        else:  
            estado = OBSERVADO

        json_final = {"estado": estado,"observaciones":observaciones}
        return json_final


    def execute_rf(self,region, tecnologia):

        # Logica
        pass
    
    def execute_apurimac_ftth(self):

        # Logica
        pass