from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyswip import Prolog

app = FastAPI(title="API PROLOG")

# Uso de prolog en variable
prolog = Prolog()
prolog.consult("base.pl")

class NuevoSospechoso(BaseModel):
    nombre: str
    delito: str

# GET : Imprimir sospechoso
# Parametros: <nombre>
@app.get("/api/sospechosos/{nombre}")
def obtener_sospechoso(nombre: str):
    nombre = nombre.lower()
    consulta = f"buscar_sospechoso('{nombre}', Delito)"

    # Si falla al realizar la consulta del sospechos en prolog
    try:
        resultados = list(prolog.query(consulta))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error con sospechoso")

    # Si no fallo, pero no hay data
    if not resultados:
        raise HTTPException(status_code=404, detail=f"El sospechoso '{nombre}' no esta")

    # Obtener el nombre del sospechos posterior a la consulta
    delito_encontrado = str(resultados[0]["Delito"])

    return {
        "nombre": nombre,
        "delito": delito_encontrado
    }


# POST : Guarda sospechoso
# Body: <NuevoSospechoso>
@app.post("/api/sospechosos")
def agregar_sospechoso(datos: NuevoSospechoso):
    nombre = datos.nombre.lower()
    delito = datos.delito.lower()

    # Insercion en memoria (PROLOG)
    prolog.assertz(f"sospechoso({nombre}, {delito})")

    # Insercioin ordenada
    with open("base.pl", "r") as archivo:
        lineas = archivo.readlines()

    # Correccion por si ultima linea no tiene salto \n
    if lineas and not lineas[-1].endswith("\n"):
        lineas[-1] += "\n"

    indice_insercion = 0
    for i, linea in enumerate(lineas):

        # Validar en que parte estan los hechos y llevar el control
        if linea.startswith("sospechoso("):
            indice_insercion = i + 1

    # Validar si no hay hechos e ingresar despues del dynamic
    if indice_insercion == 0:
        for i, linea in enumerate(lineas):
            if "dynamic" in linea:
                indice_insercion = i + 1

    # Definir en donde se insertara el hecho nuevo
    hecho_linea = f"sospechoso({nombre}, {delito}).\n"
    lineas.insert(indice_insercion, hecho_linea)

    with open("base.pl", "w") as archivo:
        archivo.writelines(lineas)

    return {
        "mensaje" : f"Sospecho {nombre} registrado exitosamente",
        "hecho_agregado": f"sospechoso('{nombre}','{delito}')"
    }