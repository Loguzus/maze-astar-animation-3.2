"""Главный модуль приложения для работы 3.2 (Генератор лабиринтов и Алгоритм A*)."""

import tkinter as tk
from typing import Generator, Optional
from src.models.animation_model import MazePathfinderModel
from src.renderers.renderer import MazeRenderer
from src.widgets.controls import MazeControlsPanel


class AnimationApp:
    """Главное окно приложения генерации лабиринтов и поиска пути A*."""

    def __init__(self) -> None:
        """Инициализирует окно, холст и обработчики мыши."""
        self.root = tk.Tk()
        self.root.title("Работа 3.2 (Вариант 24) — Генератор лабиринтов и Алгоритм A*")
        self.root.geometry("740x800")
        self.root.configure(bg="#0f172a")

        self.model = MazePathfinderModel(rows=21, cols=21)
        self.active_generator: Optional[Generator[str, None, None]] = None

        self.canvas = tk.Canvas(self.root, width=660, height=660, bg="#f8fafc", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.renderer = MazeRenderer(self.canvas, self.model)

        self.controls = MazeControlsPanel(
            self.root,
            self.model,
            on_start_generator=self.start_maze_generation,
            on_start_astar=self.start_astar,
            on_start_bfs=self.start_bfs,
            on_refresh=self.renderer.render,
        )
        self.controls.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.bind("<Button-1>", self._toggle_wall)
        self.canvas.bind("<Configure>", lambda _e: self.renderer.render())

        self.start_maze_generation()

    def _toggle_wall(self, event: tk.Event) -> None:
        """Позволяет вручную ставить и убирать стены кликом мыши."""
        r, c = self.renderer.screen_to_cell(event.x, event.y)
        if (r, c) not in (self.model.start, self.model.goal):
            self.model.grid[r][c] = 1 - self.model.grid[r][c]
            self.renderer.render()

    def start_maze_generation(self) -> None:
        """Запускает анимированную генерацию лабиринта."""
        self.active_generator = self.model.generate_maze_steps()

    def start_astar(self) -> None:
        """Запускает анимированный поиск кратчайшего пути алгоритмом A*."""
        self.active_generator = self.model.solve_astar_steps()

    def start_bfs(self) -> None:
        """Запускает анимированный поиск пути алгоритмом BFS."""
        self.active_generator = self.model.solve_bfs_steps()

    def animate(self) -> None:
        """Продвигает активный генератор на один шаг и перерисовывает холст."""
        if self.active_generator is not None:
            try:
                next(self.active_generator)
                self.renderer.render()
            except StopIteration:
                self.active_generator = None
        self.root.after(20, self.animate)

    def run(self) -> None:
        """Запускает главный цикл приложения."""
        self.animate()
        self.root.mainloop()
