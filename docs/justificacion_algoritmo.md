# Justificación de la Elección del Algoritmo Inicial

En el desarrollo del agente para navegación de laberintos dinámicos, se ha seleccionado el algoritmo **A*** como opción predeterminada y inicial. Esta elección se basa en varios criterios fundamentales que lo hacen ideal para este tipo de problemas:

## Ventajas de A* como Algoritmo Inicial

1. **Balance entre completitud y eficiencia**: 
   - A* combina las ventajas de BFS (garantía de encontrar la solución óptima) con la eficiencia de una búsqueda guiada.
   - Utiliza una función heurística (en este caso, la distancia Manhattan) para dirigir la búsqueda hacia la meta de manera más eficiente.

2. **Adaptabilidad a diferentes entornos**:
   - En espacios abiertos, A* es extremadamente eficiente al evitar explorar nodos que están lejos de la meta.
   - En laberintos complejos, sigue garantizando el camino óptimo.
   - Funciona bien tanto en entornos simples como complejos, lo que lo hace versátil para un laberinto que puede cambiar dinámicamente.

3. **Comportamiento óptimo**:
   - Cuando se utiliza una heurística admisible (como la distancia Manhattan en una cuadrícula), A* garantiza encontrar el camino más corto.
   - Esto es importante en un entorno dinámico, donde queremos minimizar el tiempo que toma el agente para llegar a la meta.

4. **Eficiencia computacional**:
   - A* expande menos nodos que BFS en la mayoría de los casos, lo que resulta en un menor uso de memoria y tiempo de cálculo.
   - En un entorno dinámico donde necesitamos recalcular rutas frecuentemente, la eficiencia es crucial.

## Comparación con Alternativas

### BFS (Búsqueda en Amplitud)
- **Ventajas**: Garantiza el camino más corto, sencillo de implementar
- **Desventajas**: Explora en todas direcciones por igual, lo que puede ser ineficiente en espacios grandes
- **Cuándo usarlo**: Cuando el agente está en un laberinto complejo con muchas bifurcaciones

### DFS (Búsqueda en Profundidad)
- **Ventajas**: Memoria eficiente, bueno para explorar rápidamente caminos largos
- **Desventajas**: No garantiza el camino más corto, puede quedar atrapado en caminos sin salida
- **Cuándo usarlo**: Cuando el agente está potencialmente atrapado y necesita explorar profundamente para encontrar una salida

## Estrategia de Cambio Dinámico

Aunque A* es nuestra elección inicial, el agente está diseñado para cambiar de algoritmo según la situación:

1. Cuando se detecta que el agente está "atrapado" (con pocas opciones de movimiento), se cambia a DFS para explorar profundamente las posibles salidas.

2. En espacios abiertos con muchas opciones, se mantiene A* por su eficiencia y optimalidad.

3. En laberintos complejos con muchas bifurcaciones, se puede cambiar a BFS para garantizar el camino más corto.

Esta estrategia adaptativa permite al agente aprovechar las fortalezas de cada algoritmo según el contexto actual del laberinto, lo que es esencial en un entorno dinámico donde las condiciones cambian constantemente. 