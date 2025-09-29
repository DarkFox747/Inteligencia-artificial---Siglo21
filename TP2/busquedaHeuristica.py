from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import heapq
import time
import argparse
import json

Coord = Tuple[int, int]

@dataclass
class SearchResult:
    name: str
    path: List[Coord]
    cost: float
    expanded: int
    runtime_ms: float

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from: Dict[Coord, Coord], current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def neighbors(p: Coord, grid: List[str]) -> List[Coord]:
    h, w = len(grid), len(grid[0])
    i, j = p
    cand = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
    out = []
    for x,y in cand:
        if 0 <= x < h and 0 <= y < w and grid[x][y] != '#':  # '#' = obstáculo
            out.append((x,y))
    return out

def greedy_best_first(grid: List[str], start: Coord, goal: Coord) -> SearchResult:
    t0 = time.perf_counter()
    pq: List[Tuple[int, int, Coord]] = []  # (h, tie, node)
    tie = 0
    heapq.heappush(pq, (manhattan(start, goal), tie, start))
    came_from: Dict[Coord, Coord] = {}
    visited = set()
    expanded = 0

    while pq:
        _, _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        expanded += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            dt = (time.perf_counter() - t0) * 1000
            return SearchResult("Greedy Best-First", path, cost=len(path)-1, expanded=expanded, runtime_ms=dt)

        for nb in neighbors(current, grid):
            if nb in visited: 
                continue
            if nb not in came_from:
                came_from[nb] = current
            tie += 1
            heapq.heappush(pq, (manhattan(nb, goal), tie, nb))

    dt = (time.perf_counter() - t0) * 1000
    return SearchResult("Greedy Best-First", [], cost=float("inf"), expanded=expanded, runtime_ms=dt)

def astar(grid: List[str], start: Coord, goal: Coord) -> SearchResult:
    t0 = time.perf_counter()
    pq: List[Tuple[int, int, Coord]] = []  # (f=g+h, tie, node)
    tie = 0
    g: Dict[Coord, int] = {start: 0}
    came_from: Dict[Coord, Coord] = {}
    heapq.heappush(pq, (manhattan(start, goal), tie, start))
    closed = set()
    expanded = 0

    while pq:
        f, _, current = heapq.heappop(pq)
        if current in closed:
            continue
        closed.add(current)
        expanded += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            dt = (time.perf_counter() - t0) * 1000
            return SearchResult("A*", path, cost=g[current], expanded=expanded, runtime_ms=dt)

        for nb in neighbors(current, grid):
            tentative_g = g[current] + 1  # costo unitario por movimiento
            if nb not in g or tentative_g < g[nb]:
                g[nb] = tentative_g
                came_from[nb] = current
                tie += 1
                f_nb = tentative_g + manhattan(nb, goal)
                heapq.heappush(pq, (f_nb, tie, nb))

    dt = (time.perf_counter() - t0) * 1000
    return SearchResult("A*", [], cost=float("inf"), expanded=expanded, runtime_ms=dt)

def render(grid: List[str], path: List[Coord], start: Coord, goal: Coord) -> List[str]:
    g = [list(r) for r in grid]
    for (i,j) in path:
        if (i,j) != start and (i,j) != goal:
            g[i][j] = '*'
    si, sj = start; gi, gj = goal
    g[si][sj] = 'S'
    g[gi][gj] = 'G'
    return [''.join(r) for r in g]

def run_demo(kind: str) -> Tuple[List[str], Coord, Coord]:
    """
    Dos escenarios:
      - 'corridor': un pasillo con rodeo donde Greedy suele desviarse
      - 'maze': laberinto simple con decisiones
    """
    if kind == "corridor":
        grid = [
            "..........",
            "#########.",
            "..........",
            ".#########",
            "..........",
        ]
        start, goal = (0, 0), (4, 9)
        return grid, start, goal
    else:
        grid = [
            ".#....#...",
            ".#.#..#.#.",
            ".#.#..#.#.",
            ".#.#..#.#.",
            "...#..#..G",
            "S..#......",
        ]
        # Marcamos S/G en render, aquí quedan como celdas libres.
        start, goal = (5,0), (4,9)
        return grid, start, goal

def compare_and_print(greedy_res: SearchResult, a_res: SearchResult, grid: List[str], start: Coord, goal: Coord, show_map: bool):
    def show(title: str, res: SearchResult):
        print(f"\n== {title} ==")
        print(f"  Encontrado: {bool(res.path)}")
        print(f"  Costo      : {res.cost}")
        print(f"  Longitud   : {len(res.path)}")
        print(f"  Expandidos : {res.expanded}")
        print(f"  Tiempo     : {res.runtime_ms:.3f} ms")
        if show_map and res.path:
            print("\n".join(render(grid, res.path, start, goal)))

    show(greedy_res.name, greedy_res)
    show(a_res.name, a_res)

    # Comparación
    if greedy_res.path and a_res.path:
        better = "A*" if a_res.cost <= greedy_res.cost else "Greedy"
        print("\n--- Comparación ---")
        print(f"  Método con menor costo: {better}")
        print(f"  ΔCosto = {greedy_res.cost - a_res.cost}")
        print(f"  ΔExpandidos = {greedy_res.expanded - a_res.expanded}")
    else:
        print("\n--- Comparación ---")
        print("  Al menos uno de los métodos no encontró solución.")

def main():
    parser = argparse.ArgumentParser(description="Greedy Best-First vs A* en un grid 2D (4-neigh).")
    parser.add_argument("--scenario", choices=["corridor","maze"], default="corridor", help="Escenario de prueba")
    parser.add_argument("--show-map", action="store_true", help="Imprime el grid con el camino")
    parser.add_argument("--json", action="store_true", help="Salida en JSON con ambas métricas")
    args = parser.parse_args()

    grid, start, goal = run_demo(args.scenario)

    gr = greedy_best_first(grid, start, goal)
    ar = astar(grid, start, goal)

    if args.json:
        print(json.dumps({
            "scenario": args.scenario,
            "start": start, "goal": goal,
            "greedy": gr.__dict__,
            "astar": ar.__dict__,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Escenario: {args.scenario}")
        print(f"Inicio: {start}  Meta: {goal}")
        compare_and_print(gr, ar, grid, start, goal, show_map=args.show_map)

if __name__ == "__main__":
    main()
