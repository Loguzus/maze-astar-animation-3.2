"""Модель генерации лабиринтов и поиска кратчайшего пути (A* и BFS)."""

from collections import deque
import heapq
import json
import random
from typing import Dict, Generator, List, Optional, Set, Tuple

Coord = Tuple[int, int]


class MazePathfinderModel:
    """Класс модели сетки лабиринта, генератора и алгоритмов поиска пути."""

    EMPTY = 0
    WALL = 1

    def __init__(self, rows: int = 21, cols: int = 21) -> None:
        """Инициализирует сетку лабиринта нечетной размерности."""
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.grid: List[List[int]] = []
        self.start: Coord = (1, 1)
        self.goal: Coord = (self.rows - 2, self.cols - 2)

        self.visited_cells: Set[Coord] = set()
        self.frontier_cells: Set[Coord] = set()
        self.current_cell: Optional[Coord] = None
        self.path: List[Coord] = []
        self.reset_grid(fill_walls=False)

    def reset_grid(self, fill_walls: bool = False) -> None:
        """Очищает сетку и сбрасывает состояния визуализации."""
        val = self.WALL if fill_walls else self.EMPTY
        self.grid = [[val for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)
        self.grid[self.start[0]][self.start[1]] = self.EMPTY
        self.grid[self.goal[0]][self.goal[1]] = self.EMPTY
        self.clear_search_state()

    def clear_search_state(self) -> None:
        """Очищает только результаты поиска пути, сохраняя стены лабиринта."""
        self.visited_cells.clear()
        self.frontier_cells.clear()
        self.current_cell = None
        self.path.clear()

    def resize(self, rows: int, cols: int) -> None:
        """Изменяет размерность сетки лабиринта."""
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.reset_grid(fill_walls=False)

    def generate_maze_steps(self) -> Generator[str, None, None]:
        """Пошаговый генератор лабиринта на основе рандомизированного обхода."""
        self.reset_grid(fill_walls=True)
        visited: Set[Coord] = {self.start}
        self.grid[self.start[0]][self.start[1]] = self.EMPTY

        frontier: List[Tuple[Coord, Coord]] = []
        for nr, nc in self._unvisited_maze_neighbors(self.start, visited):
            mid = ((self.start[0] + nr) // 2, (self.start[1] + nc) // 2)
            frontier.append((mid, (nr, nc)))

        while frontier:
            idx = random.randint(max(0, len(frontier) - 6), len(frontier) - 1)
            wall_cell, target_cell = frontier.pop(idx)
            if target_cell not in visited:
                visited.add(target_cell)
                self.grid[wall_cell[0]][wall_cell[1]] = self.EMPTY
                self.grid[target_cell[0]][target_cell[1]] = self.EMPTY
                self.current_cell = target_cell
                for nr, nc in self._unvisited_maze_neighbors(target_cell, visited):
                    mid = ((target_cell[0] + nr) // 2, (target_cell[1] + nc) // 2)
                    frontier.append((mid, (nr, nc)))
                yield "generating"

        self.grid[self.goal[0]][self.goal[1]] = self.EMPTY
        self.current_cell = None
        yield "done"

    def _unvisited_maze_neighbors(self, cell: Coord, visited: Set[Coord]) -> List[Coord]:
        """Возвращает соседние клетки через одну стену (шаг = 2)."""
        r, c = cell
        neighbors: List[Coord] = []
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            nr, nc = r + dr, c + dc
            if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1 and (nr, nc) not in visited:
                neighbors.append((nr, nc))
        random.shuffle(neighbors)
        return neighbors

    @staticmethod
    def manhattan(a: Coord, b: Coord) -> int:
        """Вычисляет манхэттенскую эвристику h(n) = |r1 - r2| + |c1 - c2| для алгоритма A*."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve_astar_steps(self) -> Generator[str, None, None]:
        """Пошаговый генератор алгоритма A* для нахождения кратчайшего пути."""
        self.clear_search_state()
        open_heap: List[Tuple[int, int, Coord]] = []
        counter = 0
        g_score: Dict[Coord, int] = {self.start: 0}
        came_from: Dict[Coord, Coord] = {}

        heapq.heappush(open_heap, (self.manhattan(self.start, self.goal), counter, self.start))
        self.frontier_cells.add(self.start)

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current in self.visited_cells:
                continue

            self.frontier_cells.discard(current)
            self.visited_cells.add(current)
            self.current_cell = current
            yield "searching"

            if current == self.goal:
                self._reconstruct_path(came_from, current)
                self.current_cell = None
                yield "found"
                return

            for neighbor in self._passable_neighbors(current):
                if neighbor in self.visited_cells:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, 10**9):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.manhattan(neighbor, self.goal)
                    counter += 1
                    heapq.heappush(open_heap, (f_score, counter, neighbor))
                    self.frontier_cells.add(neighbor)

        self.current_cell = None
        yield "no_path"

    def solve_bfs_steps(self) -> Generator[str, None, None]:
        """Пошаговый генератор поиска в ширину (BFS) для сравнения с A*."""
        self.clear_search_state()
        queue: deque[Coord] = deque([self.start])
        came_from: Dict[Coord, Coord] = {}
        self.frontier_cells.add(self.start)

        while queue:
            current = queue.popleft()
            if current in self.visited_cells:
                continue

            self.frontier_cells.discard(current)
            self.visited_cells.add(current)
            self.current_cell = current
            yield "searching"

            if current == self.goal:
                self._reconstruct_path(came_from, current)
                self.current_cell = None
                yield "found"
                return

            for neighbor in self._passable_neighbors(current):
                if neighbor not in self.visited_cells and neighbor not in self.frontier_cells:
                    came_from[neighbor] = current
                    self.frontier_cells.add(neighbor)
                    queue.append(neighbor)

        self.current_cell = None
        yield "no_path"

    def _passable_neighbors(self, cell: Coord) -> List[Coord]:
        """Возвращает проходимых соседей клетки по 4 направлениям."""
        r, c = cell
        result: List[Coord] = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == self.EMPTY:
                result.append((nr, nc))
        return result

    def _reconstruct_path(self, came_from: Dict[Coord, Coord], current: Coord) -> None:
        """Восстанавливает кратчайший путь от финиша к старту."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        self.path = path

    def export_to_file(self, filepath: str) -> None:
        """Экспортирует лабиринт во внешний JSON-файл."""
        data = {
            "rows": self.rows,
            "cols": self.cols,
            "start": list(self.start),
            "goal": list(self.goal),
            "grid": self.grid,
        }
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def import_from_file(self, filepath: str) -> None:
        """Импортирует лабиринт из внешнего JSON-файла."""
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.rows = int(data["rows"])
        self.cols = int(data["cols"])
        self.start = (int(data["start"][0]), int(data["start"][1]))
        self.goal = (int(data["goal"][0]), int(data["goal"][1]))
        self.grid = data["grid"]
        self.clear_search_state()
