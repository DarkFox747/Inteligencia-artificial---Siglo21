# Trabajo Práctico: Búsqueda en el Espacio de Estados

Este directorio contiene los archivos del **Trabajo Práctico de Búsqueda**, donde se implementan y comparan distintos métodos de resolución de problemas en inteligencia artificial.

## Contenido de la carpeta
- **bsquedaExhaustiva.py**: Script que implementa una búsqueda exhaustiva (no informada) en una línea 1D, simulando el palpado de un robot para localizar un objetivo.
- **busquedaHeuristica.py**: Script que implementa y compara dos métodos heurísticos en un grid 2D:
  - **Greedy Best-First Search** (Primero el Mejor).
  - **A\*** (A Star).

## Cómo usar los archivos

### 1. Búsqueda Exhaustiva
Ejecutar:
```bash
python bsquedaExhaustiva.py
```

Permite simular la búsqueda en un eje horizontal, configurando parámetros como paso de exploración, tolerancia y rango máximo.

**Parámetros disponibles:**
- `--start`: Posición inicial (default: 0.0)
- `--target`: Posición del objetivo (default: 0.35)
- `--tolerance`: Tolerancia de palpado (default: 0.05)
- `--step`: Paso de exploración (default: 0.1)
- `--max-range`: Rango máximo de búsqueda (default: 2.0)
- `--json`: Salida en formato JSON

### 2. Búsqueda Heurística
Ejecutar:
```bash
python busquedaHeuristica.py --scenario corridor --show-map
```

**Parámetros disponibles:**
- `--scenario`: Permite elegir distintos escenarios de prueba (`corridor` o `maze`)
- `--show-map`: Imprime el grid con el camino encontrado
- `--json`: Entrega la salida en formato JSON

## Descripción del trabajo

En este TP se analiza la búsqueda en el espacio de estados como estrategia para resolver problemas.
Se comparan las características, ventajas y limitaciones de:

Búsqueda Exhaustiva, que garantiza encontrar la solución pero con alto costo de recursos.

Búsqueda Heurística, que introduce una función de evaluación para guiar la exploración y lograr soluciones más eficientes.

Los resultados demuestran cómo una heurística bien diseñada puede reducir drásticamente el tiempo y la cantidad de nodos explorados, manteniendo la calidad de la solución.