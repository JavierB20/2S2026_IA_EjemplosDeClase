# Importamos la clase Prolog de la librería pyswip, la cual actúa como un puente entre Python y Prolog.
from pyswip import Prolog

# Iniciamos el motor de Prolog creando una instancia para poder ejecutar comandos.
prolog = Prolog()

# Cargamos el archivo "familia.pl" que contiene nuestros hechos y reglas lógicas (la base de conocimientos).
prolog.consult("familia.pl")

print("Abuelos de maria:")
# prolog.query ejecuta la consulta en Prolog. 'X' es una variable incógnita que Prolog intentará resolver.
# El bucle 'for' recorre todas las respuestas válidas encontradas por Prolog.
for abuelo in prolog.query("abuelo(X, maria)"):
    # Cada iteración devuelve un diccionario. Extraemos el valor de la clave 'X' y lo pasamos a mayúsculas.
    print(f"Abuelo: {abuelo['X'].upper()}")

print("Ancestros directos de pedro:")
# Hacemos una consulta para obtener a todos los ancestros de Pedro y los recorremos uno por uno.
for ancestro in prolog.query("ancestro_directo(X, pedro)"):
    print(f"Ancestro: {ancestro['X'].upper()}")

print("¿Carlos es ancestro directo de maria?")
# Al no haber una variable 'X' (ambos son nombres específicos), Prolog solo responde si es verdadero o falso.
# Convertimos el resultado a una lista. Si la regla se cumple, la lista tendrá datos; si no, estará vacía.
resultado = list(prolog.query("ancestro_directo(carlos, maria)"))    

# Evaluamos la lista: si contiene algo (True) imprime "Sí", si está vacía (False) imprime "No".
print("Sí" if resultado else "No")