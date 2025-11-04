#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
from pathlib import Path
import textwrap
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"


def run(cmd, cwd=None, exit_on_error=True):
    print(f"→ {cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=True, text=True)
    if result.returncode != 0:
        print(f"❌ Ошибка при выполнении: {cmd}")
        if exit_on_error:
            sys.exit(result.returncode)
    return result


def ensure_poetry_installed():
    """Проверяем, что poetry доступен."""
    try:
        subprocess.run(["poetry", "--version"], capture_output=True, text=True, check=True)
        print("✅ Poetry уже установлен.")
    except Exception:
        print("⚙️ Устанавливаю Poetry...")
        run("pip install poetry")


def write_valid_pyproject():
    """Создаёт корректный pyproject.toml (с резервной копией старого)."""
    if PYPROJECT_TOML.exists():
        backup = PYPROJECT_TOML.with_suffix(".toml.bak")
        shutil.copy(PYPROJECT_TOML, backup)
        print(f"📦 Старый pyproject.toml сохранён как {backup.name}")

    content = textwrap.dedent("""\
        [tool.poetry]
        name = "wheel_of_fortune"
        version = "0.1.0"
        description = "Python project automatically configured by setup_poetry_project.py"
        authors = ["Your Name <you@example.com>"]
        package-mode = false

        [tool.poetry.dependencies]
        python = ">=3.10,<3.14"

        [tool.poetry.group.dev.dependencies]
        black = "*"
        isort = "*"
        unimport = "*"
        pylint = "*"
        flake8 = "*"

        [build-system]
        requires = ["poetry-core"]
        build-backend = "poetry.core.masonry.api"
    """)
    PYPROJECT_TOML.write_text(content, encoding="utf-8")
    print("✅ Новый pyproject.toml создан.")


def configure_poetry_env():
    """Настраивает окружение Poetry."""
    print("⚙️ Настраиваю Poetry окружение...")
    run("poetry config virtualenvs.in-project true")
    run("poetry lock")
    run("poetry install --no-root")  # 👈 ключ решает твою проблему


def show_instructions():
    print("\n🎯 Настройка Poetry завершена успешно!\n")
    print("📦 Активировать окружение:")
    print("    poetry shell\n")
    print("🧹 Форматирование проекта:")
    print("    poetry run black . && poetry run isort . && poetry run unimport -r .\n")


def main():
    ensure_poetry_installed()
    write_valid_pyproject()
    configure_poetry_env()
    show_instructions()


if __name__ == "__main__":
    main()
