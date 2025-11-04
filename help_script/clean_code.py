#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import json
import logging
from pathlib import Path

HELPER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = HELPER_DIR.parent

DEFAULT_CONFIG = {
    "include_dirs": [],                 
    "include_files_pattern": [],        
    "exclude_dirs": ["venv", "__pycache__", ".git", "help_script"],
    "exclude_files_pattern": [],
    "enable_dry_run": False,
    "log_file": "clean_code.log"
}

CONFIG_FILE_JSON = HELPER_DIR / "clean_config.json"



def load_config():
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE_JSON.exists():
        try:
            with open(CONFIG_FILE_JSON, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                config.update(cfg)
        except Exception as e:
            print(f"⚠️ Не удалось прочитать {CONFIG_FILE_JSON}: {e}", file=sys.stderr)
    return config


def check_tool_installed(module_name):
    try:
        subprocess.run([sys.executable, "-m", module_name, "--version"],
                       capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ Модуль '{module_name}' не найден. Установите: pip install {module_name}")
        sys.exit(1)


def run_cmd(cmd, cwd=None, dry_run=False):
    print(f"→ Running: {' '.join(cmd)}")
    if dry_run:
        return
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Ошибка: {result.stderr}", file=sys.stderr)
    return result.stdout



def clean_file(filepath: Path, config):
    filepath = filepath.resolve()
    logging.info(f"Cleaning file: {filepath}")
    dry_run = config.get("enable_dry_run", False)

    run_cmd([sys.executable, "-m", "unimport", "-r", str(filepath)], dry_run=dry_run)

    run_cmd([sys.executable, "-m", "isort", str(filepath)], dry_run=dry_run)

    run_cmd([sys.executable, "-m", "black", str(filepath)], dry_run=dry_run)


def clean_project(root_dir: Path, config):
    exclude_dirs = set(config.get("exclude_dirs", []))
    include_dirs = config.get("include_dirs", [])
    include_patterns = config.get("include_files_pattern", [])
    dry_run = config.get("enable_dry_run", False)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        path_obj = Path(dirpath)

        if any(excl in path_obj.parts for excl in exclude_dirs):
            continue

        if include_dirs:
            if not any(str(path_obj).startswith(str(root_dir / inc)) for inc in include_dirs):
                continue

        for fname in filenames:
            if not fname.endswith(".py"):
                continue

            full = path_obj / fname

            # исключённые по шаблонам
            if any(full.match(pat) for pat in config.get("exclude_files_pattern", [])):
                continue

            # если есть include_patterns — фильтруем по ним
            if include_patterns and not any(full.match(pat) for pat in include_patterns):
                continue

            clean_file(full, config)


def main():
    config = load_config()
    log_path = HELPER_DIR / config.get("log_file", DEFAULT_CONFIG["log_file"])
    logging.basicConfig(filename=str(log_path), level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")
    logging.info("=== Start cleaning run ===")

    check_tool_installed("unimport")
    check_tool_installed("isort")
    check_tool_installed("black")

    print("Выберите режим:")
    print("  1) Полная чистка проекта")
    print("  2) Чистка одного файла")
    print("  3) Тестовый запуск (dry-run)")
    choice = input("Введите 1, 2 или 3: ").strip()

    if choice == "1":
        print("Запускается полная чистка проекта...")
        clean_project(PROJECT_ROOT, config)
    elif choice == "2":
        filepath_input = input("Введите путь к файлу (.py): ").strip()
        filepath = Path(filepath_input).resolve()
        if not filepath.is_file():
            print(f"❌ Файл {filepath} не найден.")
            sys.exit(1)
        clean_file(filepath, config)
    elif choice == "3":
        config["enable_dry_run"] = True
        print("Запускается dry-run...")
        clean_project(PROJECT_ROOT, config)
    else:
        print("Неверный выбор. Завершение.")
        sys.exit(1)

    logging.info("=== Cleaning finished ===")
    print(f"✅ Лог сохранён: {log_path}")


if __name__ == "__main__":
    main()
