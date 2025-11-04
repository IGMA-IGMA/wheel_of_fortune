import os
from pathlib import Path
from datetime import datetime

# === ОСНОВНЫЕ НАСТРОЙКИ ===
ROOT_DIR = Path(__file__).resolve().parent.parent
README_PATH = ROOT_DIR / "README.md"

START_TAG = "<!-- PROJECT TREE START -->"
END_TAG = "<!-- PROJECT TREE END -->"

# --- Игнорируем служебные папки и файлы ---
IGNORED_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".git", ".idea", ".vscode", "build", "dist",
    "site-packages", "node_modules", "help_script"
}

IGNORED_FILES = {
    ".gitignore", ".gitattributes", ".DS_Store", "Thumbs.db",
    "desktop.ini", "pip-selfcheck.json", ".coverage",
    ".pylintrc", "mypy.ini", "pytest.ini", "setup.py",
    "pyproject.toml", "requirements.txt"
}

# --- Иконки для файлов по расширению ---
FILE_ICONS = {
    # 🐍 Python
    ".py": "🐍",
    ".pyw": "🐍",
    # 📄 Текстовые
    ".txt": "📜",
    ".md": "📝",
    ".rst": "📘",
    ".log": "🧾",
    # ⚙️ Конфиги / данные
    ".json": "🧩",
    ".yaml": "⚙️",
    ".yml": "⚙️",
    ".ini": "⚙️",
    ".cfg": "⚙️",
    ".toml": "⚙️",
    # 📁 Документы
    ".pdf": "📕",
    ".docx": "📗",
    ".doc": "📗",
    ".csv": "📊",
    ".xlsx": "📊",
    ".xls": "📊",
    # 🌐 Web
    ".html": "🌐",
    ".css": "🎨",
    ".js": "🧠",
    ".ts": "🧠",
    ".vue": "💚",
    # 🖼️ Изображения
    ".png": "🖼️",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".gif": "🖼️",
    ".svg": "🖌️",
    # 📦 Архивы
    ".zip": "🗜️",
    ".tar": "🗜️",
    ".gz": "🗜️",
    ".rar": "🗜️",
}


def is_virtual_env(path: Path) -> bool:
    if not path.is_dir():
        return False
    indicators = ["pyvenv.cfg", "bin", "Scripts", "Lib", "Include"]
    for item in indicators:
        if (path / item).exists():
            return True
    return False


def should_include(entry: str, path: Path) -> bool:
    if entry.startswith("."):
        return False
    if path.is_dir():
        if entry in IGNORED_DIRS or is_virtual_env(path):
            return False
    else:
        if entry in IGNORED_FILES:
            return False
    return True


def get_icon_for_file(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    return FILE_ICONS.get(ext, "📄")


def generate_tree(start_path: Path, prefix=""):
    tree_lines = []
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return tree_lines

    entries = [e for e in entries if should_include(e, start_path / e)]

    for i, entry in enumerate(entries):
        path = start_path / entry
        connector = "┗" if i == len(entries) - 1 else "┣"
        if path.is_dir():
            tree_lines.append(f"{prefix}{connector} 📂 {entry}")
            new_prefix = prefix + ("  " if i == len(entries) - 1 else "┃ ")
            tree_lines.extend(generate_tree(path, new_prefix))
        else:
            icon = get_icon_for_file(path)
            tree_lines.append(f"{prefix}{connector} {icon} {entry}")
    return tree_lines


def update_readme():
    project_name = ROOT_DIR.name
    tree = "\n".join(generate_tree(ROOT_DIR))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = (
        f"{START_TAG}\n"
        f"📦 **{project_name}**\n\n"
        f"```\n{tree}\n```\n"
        f"📅 Обновлено: {timestamp}\n"
        f"{END_TAG}"
    )

    if not README_PATH.exists():
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(f"# {project_name}\n\n{block}\n")
        print("✅ README.md создан в корне проекта.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if START_TAG in content and END_TAG in content:
        before = content.split(START_TAG)[0]
        after = content.split(END_TAG)[1]
        new_content = before + block + after
    else:
        new_content = content.strip() + "\n\n" + block

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ README.md обновлён деревом проекта в: {README_PATH}")


if __name__ == "__main__":
    update_readme()
