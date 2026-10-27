"""Панель управления генератором лабиринтов и алгоритмами поиска пути."""

from tkinter import filedialog, messagebox
import tkinter as tk
from typing import Callable
from src.models.animation_model import MazePathfinderModel


class MazeControlsPanel(tk.Frame):
    """Виджет кнопок управления генерацией, запуском A*/BFS и импортом/экспортом."""

    def __init__(
        self,
        parent: tk.Widget,
        model: MazePathfinderModel,
        on_start_generator: Callable[[], None],
        on_start_astar: Callable[[], None],
        on_start_bfs: Callable[[], None],
        on_refresh: Callable[[], None],
    ) -> None:
        """Создает элементы управления лабиринтом."""
        super().__init__(parent, bg="#1e293b", padx=10, pady=8)
        self.model = model
        self.on_refresh = on_refresh

        row1 = tk.Frame(self, bg="#1e293b")
        row1.pack(fill=tk.X, pady=2)

        self._btn(row1, "Сгенерировать лабиринт", on_start_generator)
        self._btn(row1, "Найти путь A*", on_start_astar)
        self._btn(row1, "Найти путь BFS", on_start_bfs)
        self._btn(row1, "Очистить поиск", self._clear_search)

        row2 = tk.Frame(self, bg="#1e293b")
        row2.pack(fill=tk.X, pady=2)

        self._btn(row2, "Размер 15x15", lambda: self._resize(15))
        self._btn(row2, "Размер 25x25", lambda: self._resize(25))
        self._btn(row2, "Размер 35x35", lambda: self._resize(35))
        self._btn(row2, "Экспорт в файл", self._export_maze)
        self._btn(row2, "Импорт из файла", self._import_maze)

    def _btn(self, parent: tk.Widget, text: str, cmd: Callable[[], None]) -> None:
        """Создает кнопку на панели инструментов."""
        tk.Button(
            parent,
            text=text,
            command=cmd,
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            relief=tk.FLAT,
            padx=8,
            pady=4,
        ).pack(side=tk.LEFT, padx=3)

    def _clear_search(self) -> None:
        """Сбрасывает посещенные клетки и перерисовывает поле."""
        self.model.clear_search_state()
        self.on_refresh()

    def _resize(self, size: int) -> None:
        """Меняет размер лабиринта и перерисовывает поле."""
        self.model.resize(size, size)
        self.on_refresh()

    def _export_maze(self) -> None:
        """Сохраняет лабиринт во внешний JSON-файл."""
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Maze", "*.json"), ("All Files", "*.*")],
            initialfile="maze.json",
        )
        if path:
            self.model.export_to_file(path)
            messagebox.showinfo("Экспорт", f"Лабиринт сохранен в файл:\n{path}")

    def _import_maze(self) -> None:
        """Загружает лабиринт из внешнего JSON-файла."""
        path = filedialog.askopenfilename(
            filetypes=[("JSON Maze", "*.json"), ("All Files", "*.*")]
        )
        if path:
            self.model.import_from_file(path)
            self.on_refresh()
