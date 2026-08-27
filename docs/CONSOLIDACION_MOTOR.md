# Virgin.IA — consolidación del motor

## Objetivo
Convertir problemas definidos por el usuario en formulaciones cuánticas y explorar automáticamente parámetros, arquitecturas y estrategias, conservando evidencia reproducible.

## Pipeline
`problema → formulación → candidatos → simulación → evaluación → selección/mutación → aprendizaje → circuito final`

## Capas
- Problemas y benchmarks.
- Formulación binaria/QUBO/Ising.
- Generación de circuitos.
- Búsqueda de arquitectura.
- Búsqueda de estrategias.
- Simulación y evaluación.
- Registro de experimentos.
- Coste/limitaciones del hardware.

## Regla científica
No declarar que un circuito es mejor solo por una ejecución. Registrar semilla, problema, circuito, parámetros, métrica, coste, número de ejecuciones y comparación con baseline.

## Interfaz futura
La interfaz debe mostrar: problema activo, formulación, experimentos ejecutados, mejores candidatos, evidencia, coste y siguiente experimento. Debe permitir entender qué está haciendo el motor sin obligar al usuario a leer código.

## Estado
La base v0.4 ya contiene búsqueda de parámetros, arquitectura, estrategias y una primera capa de formulación. Los siguientes bloques son conversión QUBO/Ising→Hamiltoniano, memoria de experimentos, política aprendida y evaluación hardware-aware.
