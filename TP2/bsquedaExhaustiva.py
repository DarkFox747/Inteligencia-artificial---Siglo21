from dataclasses import dataclass
from typing import Callable, List, Optional
import argparse
import json


@dataclass
class ScanResult:
    found: bool
    position: Optional[float]
    probes: int
    path_length: float
    visited: List[float]


def exhaustive_line_search(
    start: float,
    sense: Callable[[float], bool],
    step: float = 0.1,
    max_range: float = 2.0,
) -> ScanResult:
    """
    Búsqueda exhaustiva a lo largo de una línea 1D centrada en `start`.
    Patrón: start, +Δ, -Δ, +2Δ, -2Δ, ... hasta que k*Δ supere `max_range`.
    """
    visited: List[float] = []
    probes = 0
    path = 0.0
    last_x = start

    def palp(x: float) -> bool:
        nonlocal probes
        probes += 1
        visited.append(round(x, 6))
        return sense(x)

    # Palpado en la posición inicial
    if palp(start):
        return ScanResult(True, start, probes, path, visited)

    k = 1
    while k * step <= max_range:
        for direction in (+1, -1):
            x = start + direction * k * step
            path += abs(x - last_x)
            last_x = x
            if palp(x):
                return ScanResult(True, x, probes, path, visited)
        k += 1

    return ScanResult(False, None, probes, path, visited)


def make_sensor(target: float, tol: float) -> Callable[[float], bool]:
    """
    Sensor idealizado: devuelve True si |x - target| <= tol (palpado exitoso).
    """
    return lambda x: abs(x - target) <= tol


def main():
    parser = argparse.ArgumentParser(
        description="Búsqueda exhaustiva 1D para localizar un objetivo sobre el eje H."
    )
    parser.add_argument("--start", type=float, default=0.0, help="Posición inicial B (default: 0.0)")
    parser.add_argument("--target", type=float, default=0.35, help="Posición real A (para simular sensor)")
    parser.add_argument("--tolerance", type=float, default=0.05, help="Tolerancia de palpado ± (default: 0.05)")
    parser.add_argument("--step", type=float, default=0.1, help="Paso ΔH de exploración (default: 0.1)")
    parser.add_argument("--max-range", type=float, default=2.0, help="Rango máximo a explorar desde B (default: 2.0)")
    parser.add_argument("--json", action="store_true", help="Imprime la salida en JSON")
    args = parser.parse_args()

    sensor = make_sensor(args.target, args.tolerance)
    result = exhaustive_line_search(
        start=args.start,
        sense=sensor,
        step=args.step,
        max_range=args.max_range,
    )

    if args.json:
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    else:
        print("=== Resultado de la búsqueda exhaustiva 1D ===")
        print(f"  B (start)        : {args.start:.6f}")
        print(f"  A (target sim)   : {args.target:.6f}")
        print(f"  Tolerancia       : ±{args.tolerance:.6f}")
        print(f"  Paso ΔH          : {args.step:.6f}")
        print(f"  Rango máx.       : {args.max_range:.6f}")
        print("---------------------------------------------")
        print(f"  ¿Encontrado?     : {result.found}")
        print(f"  Posición detect. : {None if result.position is None else f'{result.position:.6f}'}")
        print(f"  Palpados (N)     : {result.probes}")
        print(f"  Recorrido total  : {result.path_length:.6f} (unidades de H)")
        print(f"  Visitados        : {result.visited}")


if __name__ == "__main__":
    main()
