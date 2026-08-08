:- dynamic sospechoso/2.

sospechoso(juan, robo).
sospechoso(maria, fraude).
sospechoso('jose', 'robo').
sospechoso('mario', 'robo').
sospechoso(marta, robo).

buscar_sospechoso(Nombre, Delito) :-
    sospechoso(Nombre, Delito).
