"""Модуль отрисовки сетки лабиринта, посещенных узлов и кратчайшего пути."""

import tkinter as tk
from src.models.animation_model import Coord, MazePathfinderModel


class MazeRenderer:
    """Класс отрисовки клеток лабиринта и шагов поиска пути на Canvas."""

    COLOR_EMPTY = "#f8fafc"
    COLOR_WALL = "#0f172a"
    COLOR_VISITED = "#93c5fd"
    COLOR_FRONTIER = "#fde047"
    COLOR_CURRENT = "#f97316"
    COLOR_PATH = "#10b981"
    COLOR_START = "#2563eb"
    COLOR_GOAL = "#ef4444"

    def __init__(self, canvas: tk.Canvas, model: MazePathfinderModel) -> None:
        """Инициализирует отрисовщик сетки."""
        self.canvas = canvas
        self.model = model

    def cell_size(self) -> float:
        """Вычисляет размер стороны одной клетки в пикселях."""
        w = int(self.canvas.winfo_width() or 660)
        h = int(self.canvas.winfo_height() or 660)
        return min(w / self.model.cols, h / self.model.rows)

    def screen_to_cell(self, x: int, y: int) -> Coord:
        """Преобразует координаты клика мыши в индексы (row, col) сетки."""
        size = self.cell_size()
        col = max(0, min(self.model.cols - 1, int(x // size)))
        row = max(0, min(self.model.rows - 1, int(y // size)))
        return row, col

    def render(self) -> None:
        """Отрисовывает сетку лабиринта и состояния клеток."""
        self.canvas.delete("all")
        size = self.cell_size()
        path_set = set(self.model.path)

        for r in range(self.model.rows):
            for c in range(self.model.cols):
                coord = (r, c)
                color = self.COLOR_WALL if self.model.grid[r][c] == self.model.WALL else self.COLOR_EMPTY

                if coord in self.model.visited_cells:
                    color = self.COLOR_VISITED
                if coord in self.model.frontier_cells:
                    color = self.COLOR_FRONTIER
                if coord in path_set:
                    color = self.COLOR_PATH
                if coord == self.model.current_cell:
                    color = self.COLOR_CURRENT
                if coord == self.model.start:
                    color = self.COLOR_START
                elif coord == self.model.goal:
                    color = self.COLOR_GOAL

                x1, y1 = c * size, r * size
                self.canvas.create_rectangle(
                    x1, y1, x1 + size, y1 + size, fill=color, outline="#cbd5e1", width=1
                )
