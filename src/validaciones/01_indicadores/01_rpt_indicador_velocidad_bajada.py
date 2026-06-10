# ================================================================================================================================
# IMPORTACION DE LIBRERIAS  ==========================     
# ================================================================================================================================
import pandas as pd



# ================================================================================================================================
# ================================================================================================================================

class RptIndicadorVelocidadBajada01():

    def __init__(self):
        #self.maestro_ips    = open ("/maestros/maestro_ips.json", "r").read()


        pass

    def execute(self, region, tecnologia):

        if tecnologia == "FTTH":
            print("ejecutando FTTH",region,tecnologia)
            return self.execute_ftth(region,tecnologia)
        
        elif tecnologia == "RF":
            print("ejecutando RF",region,tecnologia)
            return self.execute_rf(region,tecnologia)

        else:
            return {}
    

    def execute_ftth(self,region, tecnologia):
        # self.maestro_ips["region"]["tecnologia"]
        # # Logica
        # def cruce_maestro():
        #     a
        # observaciones = []

        # observacion = leer_maestro()
        # observaciones.append
        # observacion = cruce_maestro()
        # llamado_api()
        # verificar_duplicados()

        # # 
        # subir_sharepoint()

        return {"estado":"OBERVADO","observacion":"observaciones"}


    def execute_rf(self,region, tecnologia):

        # Logica
        pass
    
    def execute_apurimac_ftth(self):

        # Logica
        pass