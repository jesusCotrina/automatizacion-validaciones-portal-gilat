
import pandas as pd


def funcion_1():
    try:
        # logica
        pass

    except Exception as e:
        mensaje=f"Error en la funcion 1 \nError:{e}"
        print(mensaje)
        raise RuntimeError(mensaje)

def funcion_2():
    try:
        # logica
        pass
    except Exception as e:
        # logica
        mensaje=f"Error en la funcion 2 \nError:{e}"
        print(mensaje)
        raise RuntimeError(mensaje)

def funcion_3():
    try:
        # logica
        pass
    except Exception as e:
        mensaje=f"Error en la funcion 3 \nError:{e}"
        print(mensaje)
        raise RuntimeError(mensaje)

def main():
    print("Ejecutando main")
    try:
        # ================================================================================================================================
        # LECTURA DE MAESTROS Y VARIABLES ==========================     
        # ================================================================================================================================
        A = open("/maestros/maestro_A.json", "r").read()    
        observaciones= []


        # ================================================================================================================================
        # LOGICA DE VALIDACION ==========================     
        # ================================================================================================================================
        observacion=funcion_1() 
        if observacion is not None:
            observaciones.append(observacion)

        observacion = funcion_2()
        if observacion is not None:
            observaciones.append(observacion)

        observacion = funcion_3()
        if observacion is not None:
            observaciones.append(observacion)


        # ================================================================================================================================
        # JSON DE RESULTADOS ==========================     
        # ================================================================================================================================
        if observaciones is None:
            estado = "VALIDADO"
        else:  
            estado = "OBSERVADO"

        json_final = {"estado": estado,"observaciones":observaciones}
        return json_final

    except Exception as e:
        print(f"Error en main: {e}")
        
        json_final = {"estado": estado,"observaciones":observaciones}
        return {"estado": "ERROR", "observaciones": str(e)}


if __name__ == "__main__":
    main()