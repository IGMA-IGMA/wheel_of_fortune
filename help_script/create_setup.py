#!/usr/bin/env python3
"""
Продвинутый создатель setup.py для скрипта в папке help_script
"""

import subprocess
import os
import sys
from pathlib import Path

class SetupCreator:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.data = {}
    
    def get_project_root(self):
        """Определяет корневую директорию проекта"""
        current_dir = Path(__file__).parent
        if current_dir.name == 'help_script':
            return current_dir.parent
        return current_dir
    
    def get_git_info(self):
        """Получает информацию из git"""
        try:
            # Переходим в корень проекта для git команд
            original_cwd = Path.cwd()
            os.chdir(self.project_root)
            
            name = subprocess.run(
                ['git', 'config', '--get', 'user.name'],
                capture_output=True, text=True
            ).stdout.strip()
            
            email = subprocess.run(
                ['git', 'config', '--get', 'user.email'], 
                capture_output=True, text=True
            ).stdout.strip()
            
            # URL репозитория
            repo_url = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                capture_output=True, text=True
            ).stdout.strip()
            
            os.chdir(original_cwd)
            
            return {
                'name': name or 'Unknown',
                'email': email or 'unknown@example.com',
                'repo_url': repo_url
            }
        except Exception as e:
            print(f"⚠️  Не удалось получить данные из git: {e}")
            return {'name': 'Unknown', 'email': 'unknown@example.com', 'repo_url': ''}
    
    def detect_package_name(self):
        """Определяет имя пакета из названия папки проекта"""
        return self.project_root.name.replace(' ', '_').replace('-', '_')
    
    def check_project_files(self):
        """Проверяет наличие необходимых файлов в проекте"""
        files_to_check = {
            'README.md': 'Файл README.md не найден в корне проекта',
            'LICENSE': 'Файл LICENSE не найден (рекомендуется)',
            '.git': 'Директория .git не найдена - проект не инициализирован с git',
        }
        
        for file, message in files_to_check.items():
            if not (self.project_root / file).exists():
                print(f"⚠️  {message}")
    
    def get_user_input(self):
        """Получает данные от пользователя"""
        git_info = self.get_git_info()
        
        print("🎯 Создание setup.py")
        print("=" * 50)
        print(f"📁 Корень проекта: {self.project_root}")
        print("=" * 50)
        
        # Авто-определение имени пакета
        auto_name = self.detect_package_name()
        package_name = input(f"Введите имя пакета [{auto_name}]: ").strip() or auto_name
        
        version = input("Введите версию [0.1.0]: ").strip() or "0.1.0"
        description = input("Введите описание пакета: ").strip()
        
        # Авторские данные из git
        author = input(f"Введите имя автора [{git_info['name']}]: ").strip() or git_info['name']
        email = input(f"Введите email автора [{git_info['email']}]: ").strip() or git_info['email']
        
        # URL проекта
        repo_url = git_info['repo_url']
        if repo_url:
            project_url = input(f"Введите URL проекта [{repo_url}]: ").strip() or repo_url
        else:
            project_url = input("Введите URL проекта: ").strip()
        
        self.data = {
            'package_name': package_name,
            'version': version,
            'description': description,
            'author': author,
            'email': email,
            'project_url': project_url
        }
    
    def generate_setup_py(self):
        """Генерирует setup.py файл в корне проекта"""
        
        url_section = ""
        if self.data['project_url']:
            url_section = f'    url="{self.data["project_url"]}",'
        
        setup_content = f'''from setuptools import setup, find_packages
import os

# Чтение README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "{self.data['description']}"

setup(
    name="{self.data['package_name']}",
    version="{self.data['version']}",
    author="{self.data['author']}",
    author_email="{self.data['email']}",
    description="{self.data['description']}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
{url_section}
)
'''

        setup_path = self.project_root / 'setup.py'
        with open(setup_path, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        return setup_path
    
    def run(self):
        """Запускает процесс создания"""
        self.check_project_files()
        self.get_user_input()
        setup_path = self.generate_setup_py()
        
        print("\\n" + "=" * 50)
        print("✅ setup.py успешно создан!")
        print(f"📁 Расположение: {setup_path}")
        print(f"📦 {self.data['package_name']} v{self.data['version']}")
        print(f"👤 {self.data['author']} <{self.data['email']}>")
        print("\\n📋 Не забудьте:")
        print("  📝 Заполнить README.md")
        print("  ⚖️  Добавить LICENSE файл") 
        print("  📦 Указать зависимости в install_requires")
        print("  🐍 Добавить __init__.py файлы в пакеты")

if __name__ == "__main__":
    creator = SetupCreator()
    creator.run()