% Definiendo una lista
evidencias_escena([pistola, balas, casquillos, balas]).
evidencias_laboratorio([sangre, huellas]).

% Caso Base
registrar_evidencias_rec([]).

% Recursion - regla
registrar_evidencias_rec([Cabeza | Cola]) :-
    format("Evidencias: ~w~n", Cabeza),
    registrar_evidencias_rec(Cola).

% Fuciones Basicas de listas
analizar_evidencias(EvidenciaBuscada, TotalEvidencias, ListaInvertida, ListaOrdenadaSinDuplicidad, ListaOrdenadaDuplicados) :-
    % UNIFICACION
    evidencias_escena(Lista1),
    evidencias_laboratorio(Lista2),

    % Append/3
    append(Lista1, Lista2, ListaCombinada),

    % Length/2
    length(ListaCombinada, TotalEvidencias),

    % member/2
    member(EvidenciaBuscada, ListaCombinada),

    % reverse/2
    reverse(ListaCombinada, ListaInvertida),

    % Metodos extras
    % sort/2 <Lista>, <LstOrdenada> | A - Z Sin duplicidad
    sort(ListaCombinada, ListaOrdenadaSinDuplicidad),

    % msort/2 <Lista>, <LstOrdenada> | A - Z
    msort(ListaCombinada, ListaOrdenadaDuplicados),

    writeln('Mostrar Evidencias'),
    registrar_evidencias_rec(ListaCombinada).
