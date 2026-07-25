from pyswip import Prolog

# Crear la instancia de Prolog | el motor prolog
prolog = Prolog()

# Agregar hechos
prolog.assertz("padre(juan, maria)")
prolog.assertz("padre(juan, pedro)")
prolog.assertz("padre(carlos, juan)")

# Agregar regla
prolog.assertz("progenitor(X, Y) :- padre(X, Y)")

# Consulta simple a Base de conocimiento
print("Progenitores de Maria")
for soln in prolog.query("progenitor(juan, Y)"):
    print(f"Padre: juan hijo : {soln['Y'].upper()}")
