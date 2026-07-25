% Hechos: Son las afirmaciones iniciales que el sistema toma como verdaderas.
% Se escriben en minúsculas porque representan "átomos" (datos constantes específicos).
padre(juan, maria). % Juan es padre de María.
padre(juan, pedro). % Juan es padre de Pedro.
padre(carlos, juan). % Carlos es padre de Juan.

% Reglas simples: Enseñan a Prolog cómo deducir nueva información basada en los hechos.
% El símbolo ":-" significa "SI" (condición). Las letras mayúsculas (X, Y, Z) representan variables.

% X es progenitor de Y, SI (:-) se cumple el hecho de que X es padre de Y.
progenitor(X, Y) :- padre(X, Y).

% X es abuelo de Y, SI se cumplen las siguientes dos condiciones consecutivas:
% 1. X es padre de un intermediario (Z). La coma "," funciona como un "Y" lógico (conjunción).
% 2. Ese mismo intermediario (Z) es padre de Y.
abuelo(X, Y) :-
    padre(X, Z),
    padre(Z, Y).

% Si definimos un mismo nombre de regla varias veces, actúa como un "O" lógico (disyunción).
% Condición 1: X se considera ancestro directo de Y, SI X es padre de Y.
ancestro_directo(X, Y) :-
    padre(X, Y).

% Condición 2: O BIEN, X se considera ancestro directo de Y, SI X es abuelo de Y.
ancestro_directo(X, Y) :-
    abuelo(X, Y).