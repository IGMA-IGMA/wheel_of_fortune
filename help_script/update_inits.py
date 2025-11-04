import os
import ast
import glob


class InitUpdater:
    def __init__(self, package_dir):
        self.package_dir = os.path.abspath(package_dir)

    def extract_public_names(self, file_path):
        """Извлекает все публичные функции, классы и переменные из .py файла."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except (SyntaxError, UnicodeDecodeError):
            return []

        public_names = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    public_names.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        public_names.append(target.id)

        return public_names

    def update_init(self):
        """Создает или обновляет __init__.py в текущей директории."""
        py_files = glob.glob(os.path.join(self.package_dir, "*.py"))
        py_files = [f for f in py_files if not f.endswith("__init__.py")]

        if not py_files:
            print(f"⚠️ Нет .py файлов в {self.package_dir}")
            return

        init_content = "# Автоматически сгенерированный файл\n\n"
        all_imports = []

        for file_path in sorted(py_files):
            module_name = os.path.basename(file_path)[:-3]
            public_names = self.extract_public_names(file_path)

            if public_names:
                imports_str = ", ".join(sorted(public_names))
                init_content += f"from .{module_name} import {imports_str}\n"
                all_imports.extend(public_names)

        if all_imports:
            init_content += f"\n__all__ = {sorted(all_imports)}\n"

        init_path = os.path.join(self.package_dir, "__init__.py")
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(init_content)

        print(f"✅ Обновлён {init_path}")

    @staticmethod
    def find_all_packages(root_dir="."):
        """Находит все директории с .py файлами (кроме служебных)."""
        packages = []
        for root, dirs, files in os.walk(root_dir):
            if "__pycache__" in root or "venv" in root or ".venv" in root:
                continue
            if any(f.endswith(".py") for f in files):
                packages.append(root)
        return sorted(set(packages))


def main():
    print("=== 🧩 Обновление __init__.py ===")
    print("1️⃣  Обновить все __init__.py во всём проекте")
    print("2️⃣  Обновить только одну папку")

    choice = input("\nВыберите режим (1 или 2): ").strip()

    if choice == "1":
        root = "."
        print("\n🔍 Ищу все директории с Python-файлами...\n")
        for pkg_dir in InitUpdater.find_all_packages(root):
            updater = InitUpdater(pkg_dir)
            updater.update_init()
        print("\n🎯 Все __init__.py успешно обновлены!")
    elif choice == "2":
        folder = input(
            "\nВведите путь к папке (например, help_script): ").strip()
        if not os.path.isdir(folder):
            print(f"❌ Папка '{folder}' не найдена.")
            return
        updater = InitUpdater(folder)
        updater.update_init()
    else:
        print("❌ Неверный выбор. Запустите снова и выберите 1 или 2.")


if __name__ == "__main__":
    main()
