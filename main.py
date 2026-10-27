"""Точка входа в приложение работы 3.2."""

from src.app import AnimationApp


def main() -> None:
    """Создает и запускает приложение."""
    app = AnimationApp()
    app.run()


if __name__ == "__main__":
    main()
