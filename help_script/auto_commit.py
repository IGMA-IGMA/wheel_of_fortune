import os
import subprocess
from datetime import datetime


def auto_commit():
    try:
        result = subprocess.run(["git", "status", "--porcelain"],
                                capture_output=True, text=True)
        changed_files = result.stdout.strip().split('\n') if result.stdout else []

        changes = {'added': [], 'modified': [], 'deleted': []}

        for file_status in changed_files:
            if not file_status:
                continue
            status = file_status[:2].strip()
            filename = file_status[3:]

            if status == 'A' or status == '??':
                changes['added'].append(filename)
            elif status == 'M':
                changes['modified'].append(filename)
            elif status == 'D':
                changes['deleted'].append(filename)

        commit_message = generate_commit_message(changes)

        os.system("git add .")
        os.system(f'git commit -m "{commit_message}"')
        os.system("git push")

        print(f"✅ Коммит выполнен: {commit_message}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


def generate_commit_message(changes: dict) -> str:
    message_parts = []

    if changes['added']:
        if len(changes['added']) == 1:
            message_parts.append(f"➕ Добавлен {changes['added'][0]}")
        else:
            message_parts.append(f"➕ Добавлено {len(changes['added'])} файлов")

    if changes['modified']:
        if len(changes['modified']) == 1:
            message_parts.append(f"🔧 Обновлен {changes['modified'][0]}")
        else:
            file_types = categorize_files(changes['modified'])
            type_info = []
            if file_types.get('python', 0) > 0:
                type_info.append(f"{file_types['python']} Python файлов")
            if file_types.get('config', 0) > 0:
                type_info.append(f"{file_types['config']} конфигов")
            if file_types.get('documentation', 0) > 0:
                type_info.append(f"{file_types['documentation']} документов")
            if file_types.get('readme', 0) > 0:
                type_info.append(f"{file_types['readme']} README")
            if file_types.get('other', 0) > 0:
                type_info.append(f"{file_types['other']} других файлов")

            if type_info:
                message_parts.append(f"🔧 Обновлено: {', '.join(type_info)}")
            else:
                message_parts.append(
                    f"🔧 Обновлено {len(changes['modified'])} файлов")

    if changes['deleted']:
        if len(changes['deleted']) == 1:
            message_parts.append(f"🗑️ Удален {changes['deleted'][0]}")
        else:
            message_parts.append(
                f"🗑️ Удалено {len(changes['deleted'])} файлов")

    if not message_parts:
        return "🔄 Обновление проекта"

    return " | ".join(message_parts)


def categorize_files(files: list) -> dict:
    categories = {'python': 0, 'config': 0,
                  'documentation': 0, 'readme': 0, 'other': 0}

    for file in files:
        if file.endswith(('.py', '.pyw')):
            categories['python'] += 1
        elif file.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env')):
            categories['config'] += 1
        elif file.lower() in ['readme.md', 'readme.txt', 'readme'] or 'readme' in file.lower():
            categories['readme'] += 1
        elif file.endswith(('.md', '.txt', '.rst', '.doc', '.docx')):
            categories['documentation'] += 1
        else:
            categories['other'] += 1

    return categories


def auto_commit_simple():
    result = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True)
    changed_files = [f[3:] for f in result.stdout.strip().split(
        '\n') if f] if result.stdout else []

    if not changed_files:
        print("❌ Нет изменений для коммита")
        return

    readme_changes = [f for f in changed_files if 'readme' in f.lower()]
    has_readme = len(readme_changes) > 0

    print("📁 Измененные файлы:")
    for i, file in enumerate(changed_files[:10], 1):
        readme_flag = " 📝" if 'readme' in file.lower() else ""
        print(f"  {i}. {file}{readme_flag}")
    if len(changed_files) > 10:
        print(f"  ... и еще {len(changed_files) - 10} файлов")

    if has_readme:
        print("\n📝 Обнаружены изменения в README!")

    print("\n🎯 Тип изменений:")
    print("1. Новый функционал")
    print("2. Исправление ошибок")
    print("3. Рефакторинг кода")
    print("4. Обновление документации")
    print("5. Обновление README")
    print("6. Не знаю")
    print("7. Другое")

    choice = input("Выберите тип изменений (1-7): ").strip()

    change_types = {
        '1': '🚀 Новый функционал',
        '2': '🐛 Исправление ошибок',
        '3': '♻️ Рефакторинг кода',
        '4': '📚 Обновление документации',
        '5': '📝 Обновление README',
        '6': '🔧 Обновление проекта',
        '7': '🔧 Обновление проекта'
    }

    base_message = change_types.get(choice, '🔧 Обновление проекта')

    if choice == '7':
        custom_msg = input("Введите комментарий: ").strip()
        commit_message = f"{base_message}: {custom_msg}"
    elif choice == '6':
        file_count = len(changed_files)
        main_files = changed_files[:3]
        files_info = ", ".join(main_files)
        if file_count > 3:
            files_info += f" и еще {file_count - 3} файлов"
        commit_message = f"🔧 Обновление проекта | {files_info}"
    elif choice == '5' and has_readme:
        readme_details = input(
            "Что изменилось в README? (добавлен раздел, обновлена документация и т.д.): ").strip()
        if readme_details:
            commit_message = f"📝 Обновление README: {readme_details}"
        else:
            commit_message = "📝 Обновление README"
    else:
        file_count = len(changed_files)
        main_files = changed_files[:2]
        files_info = ", ".join(main_files)
        if file_count > 2:
            files_info += f" и еще {file_count - 2} файлов"

        if has_readme and choice != '5':
            commit_message = f"{base_message} | 📝 README | {files_info}"
        else:
            commit_message = f"{base_message} | {files_info}"

    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')
    os.system("git push")

    print(f"✅ Коммит выполнен: {commit_message}")
    return commit_message, changed_files


def update_readme_changelog(commit_message: str, changed_files: list):
    try:
        # Ищем README.md в разных возможных местах
        possible_paths = [
            "README.md",
            "./README.md",
            "../README.md",
            "../../README.md"
        ]

        readme_path = None
        for path in possible_paths:
            if os.path.exists(path):
                readme_path = path
                break

        if not readme_path:
            print("❌ README.md не найден")
            return

        result = subprocess.run(["git", "log", "--oneline", "-1"],
                                capture_output=True, text=True)
        last_commit = result.stdout.strip() if result.stdout else ""

        if last_commit:
            commit_hash = last_commit[:7]
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Создаем детальную запись для changelog
            changelog_entry = f"### {current_date} | `{commit_hash}`\n"
            changelog_entry += f"**Сообщение:** {commit_message}\n\n"

            # Добавляем список измененных файлов
            if changed_files:
                changelog_entry += "**Измененные файлы:**\n"
                for file in changed_files[:15]:  # Показываем первые 15 файлов
                    file_emoji = "📝" if 'readme' in file.lower() else "🔧"
                    changelog_entry += f"- {file_emoji} `{file}`\n"
                if len(changed_files) > 15:
                    changelog_entry += f"- ... и еще {len(changed_files) - 15} файлов\n"

            changelog_entry += "\n---\n\n"

            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Ищем раздел Changelog в разных вариантах написания
            changelog_headers = [
                "## Changelog", "## История изменений", "## CHANGELOG", "## Изменения"]
            header_found = False

            for header in changelog_headers:
                if header in content:
                    # Вставляем после заголовка
                    content = content.replace(
                        header, f"{header}\n\n{changelog_entry}")
                    header_found = True
                    break

            if not header_found:
                # Если раздела нет, добавляем в конец
                content += f"\n## Changelog\n\n{changelog_entry}"

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"📝 Changelog обновлен в {readme_path}")
            print(f"📋 Добавлено {len(changed_files)} измененных файлов")

    except Exception as e:
        print(f"❌ Ошибка при обновлении README: {e}")


if __name__ == "__main__":
    commit_msg, changed_files_list = auto_commit_simple()

    # Всегда обновляем README с информацией о коммите
    update_readme_changelog(commit_msg, changed_files_list)
