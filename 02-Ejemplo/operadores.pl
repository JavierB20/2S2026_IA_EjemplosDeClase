% Operadores aritmeticos y de evaluacion

calcular_puntos(Evidencias, Testigos, Total) :-
    Base is Evidencias * 10, % Multiplicacion
    Bonus is Testigos + 5, % Suma
    Total is Base + Bonus. % Suma final

es_par(Numero) :-
    0 is Numero mod 2.


misma_cantidad(X, Y) :- X =:= Y.      % Verdadero si 2+2 =:= 4
diferente_cantidad(X, Y) :- X =\= Y.  % Verdadero si 5 =\= 3+1
mayor_sospecha(X, Y) :- X > Y.        % Verdadero si X es estrictamente mayor
limite_alcanzado(X, Y) :- X =< Y.     % Verdadero si X es menor o igual (nota: no es <=)


unificar_datos(X, Y) :- X = Y.        % Intenta hacer coincidir X con Y. Si X es variable, toma el valor de Y.
no_unifica(X, Y) :- X \= Y.           % Falla si X y Y pueden unificar.
identicos(X, Y) :- X == Y.            % Verdadero solo si son idénticos sin instanciar variables libres.
no_identicos(X, Y) :- X \== Y.        % Verdadero si no son estrictamente idénticos.