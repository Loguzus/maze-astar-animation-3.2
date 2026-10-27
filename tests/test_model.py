"""Модульные тесты для генератора лабиринтов и алгоритма A*."""

import unittest
from src.models.animation_model import MazePathfinderModel


class TestMazePathfinderModel(unittest.TestCase):
    """Проверка эвристики и нахождения кратчайшего пути."""

    def test_manhattan_distance(self) -> None:
        """Проверяет расчет манхэттенского расстояния."""
        self.assertEqual(MazePathfinderModel.manhattan((1, 1), (4, 5)), 7)

    def test_astar_finds_shortest_path_on_empty_grid(self) -> None:
        """Проверяет, что A* находит кратчайший путь на пустой сетке."""
        model = MazePathfinderModel(rows=7, cols=7)
        for _ in model.solve_astar_steps():
            pass
        self.assertTrue(len(model.path) > 0)
        self.assertEqual(model.path[0], model.start)
        self.assertEqual(model.path[-1], model.goal)


if __name__ == "__main__":
    unittest.main()
