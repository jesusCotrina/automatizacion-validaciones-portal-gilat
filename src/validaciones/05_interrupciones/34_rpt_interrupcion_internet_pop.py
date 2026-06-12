# ================================================================================================================================
# 1 IMPORTACION DE LIBRERIAS  ==========================     
# ================================================================================================================================
import pandas as pd



# ================================================================================================================================
# ================================================================================================================================

class RptInterrupcionInternetPOP():

    def __init__(self):
        pass
    

    # ================================================================================================================================
    # 2 Logica de ejecucion  ==========================     
    # ================================================================================================================================

    def execute(self, region, tecnologia,periodo):
        # PARA LOS REPORTES QUE TIENEN RF Y FTTH SOLO CONSIDERAR LA TECNOLOGIA FTTH COMO SI ESTUVIERA HACIENDO EL CONSOLIDADO
        if tecnologia == "FTTH":
            return self.execute_default(region,tecnologia)
        else:
            return {}


    # ================================================================================================================================
    # 3 Logica de reportes  ==========================     
    # ================================================================================================================================

    def execute_cusco(self, region, tecnologia):

        # Logica
        pass

    def execute_ica(self, region, tecnologia):

        # Logica
        pass

    def execute_default(self, region, tecnologia):

        observaciones= []
        # Logica
        return {"observaciones":observaciones, "estado":"VALIDADO","tecnologia":"RF/FTTH"}

    def execute_apurimac_rf(self, region, tecnologia):

        observaciones= []
        # Logica
        return {"observaciones":observaciones, "estado":"VALIDADO","tecnologia":"RF/FTTH"}
    