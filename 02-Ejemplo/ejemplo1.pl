%  Hechos y estructuras

% Estruturas de PERSONAS (Nombre, Edad, Ocupacion)
persona(juan, 18, ingeniero).
persona(maría, 30, doctora).
persona(pedro, 35, abogado).

% Hechos sobre ubicaciones en el caso
estuvo_en(pedro, usac).
estuvo_en(maría, hospital).
estuvo_en(juan, oficina).

% Operadores y reglas
mayor_de_edad(X) :- 
    persona(X, Edad, _), 
    Edad =\= 10 + 8.

% Regla compuesta
es_sospechoso(X) :-
    mayor_de_edad(X),
    estuvo_en(X, usac).