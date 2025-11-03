import os
import ast
import glob


class InitUpdater:
    def __init__(self, package_dir):
        self.package_dir = package_dir

    def extract_public_names(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return []

        public_names = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not node.name.startswith('_'):
                    public_names.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        public_names.append(target.id)

        return public_names

    def update_init(self):
        py_files = glob.glob(os.path.join(self.package_dir, "*.py"))
        py_files = [f for f in py_files if not f.endswith("__init__.py")]

        init_content = "# Автоматически сгенерированный файл\n\n"
        all_imports = []

        for file_path in sorted(py_files):
            module_name = os.path.basename(file_path)[:-3]
            public_names = self.extract_public_names(file_path)

            if public_names:
                imports_str = ", ".join(sorted(public_names))
                init_content += f"from .{module_name} import {imports_str}\n"
                all_imports.extend(
                    [f"{module_name}.{name}" for name in public_names])

        if all_imports:
            init_content += f"\n__all__ = {sorted(all_imports)}\n"

        init_path = os.path.join(self.package_dir, "__init__.py")
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(init_content)

        print(f"Обновлен {init_path}")


updater = InitUpdater(".")
updater.update_init()
