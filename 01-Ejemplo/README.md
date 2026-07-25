# Guía Básica de Prolog

## Conceptos Fundamentales

**Átomos**
Son los nombres específicos, constantes o relaciones concretas de tu programa. Para que Prolog los reconozca como texto fijo, **siempre deben iniciar con letra minúscula** (ej. `juan`, `maria`, `padre`).

**Variables**
Representan incógnitas, es decir, elementos que Prolog debe buscar, resolver e instanciar en tiempo de ejecución. **Siempre deben iniciar con letra mayúscula** o un guion bajo (ej. `X`, `Y`, `_abuelo`).

**Hechos**
Son verdades absolutas declaradas explícitamente en tu base de conocimientos. Constituyen la información base sobre la cual trabaja Prolog. Siempre se formulan usando átomos y deben terminar con un punto.
Ejemplo: `padre(juan, maria).` se lee como "Es un hecho que Juan es padre de María".

**Reglas**
Son sentencias lógicas que enseñan a Prolog a inferir nueva información condicionada a los hechos existentes. Utilizan el operador `:-`, que se interpreta como un "SI" condicional.
Ejemplo: `abuelo(X, Y) :- padre(X, Z), padre(Z, Y).` establece que X es abuelo de Y, **si** X es padre de Z **y** (representado por la coma) Z es padre de Y.

---

## Cómo Ejecutar un Archivo Prolog

Para ejecutar el archivo, necesitas tener instalado un intérprete lógico como **SWI-Prolog** en tu sistema.

1. Abre tu terminal (como PowerShell o bash) en el directorio exacto donde guardaste tu archivo (por ejemplo, `familia.pl`).
2. Inicia el motor de SWI-Prolog escribiendo el siguiente comando:
```bash
swipl

```


3. Una vez en la consola interactiva de Prolog (identificada por el prompt `?-`), carga tu base de conocimientos. **Nota:** Toda instrucción en Prolog finaliza obligatoriamente con un punto `.`:
```prolog
?- consult('familia.pl').

% O utilizando la sintaxis abreviada:
?- ['familia'].

```



---

## Cómo Usarlo (Realizar Consultas)

Con el archivo en memoria, procedes a realizar consultas escribiéndolas directamente en el prompt `?-`. Prolog responderá basándose en la lógica definida.

**1. Consultas de Validación (Verdadero/Falso):**
Si envías una consulta formada solo por átomos, Prolog verificará si esa afirmación existe o se puede deducir, devolviendo `true.` o `false.`.

```prolog
?- padre(juan, maria).
true.

```

**2. Consultas de Búsqueda (Usando Variables):**
Si pasas una variable en la consulta, Prolog buscará en la base de conocimientos todos los átomos que hagan que la expresión sea verdadera y te los devolverá.

```prolog
?- ancestro_directo(X, maria).
X = juan 

```

**3. Navegar por Múltiples Resultados:**
Si tu consulta tiene más de una respuesta (por ejemplo, María tiene varios ancestros), Prolog mostrará la primera y pausará la ejecución.

* Presiona la tecla **espacio** o **punto y coma (`;`)** para forzar a Prolog a buscar la siguiente coincidencia.
* Presiona **punto (`.`)** o **Enter** si deseas detener la búsqueda y regresar al prompt inicial.