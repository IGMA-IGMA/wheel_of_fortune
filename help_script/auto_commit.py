import os
import subprocess

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
            if file_types.get('other', 0) > 0:
                type_info.append(f"{file_types['other']} других файлов")
            
            if type_info:
                message_parts.append(f"🔧 Обновлено: {', '.join(type_info)}")
            else:
                message_parts.append(f"🔧 Обновлено {len(changes['modified'])} файлов")
    
    if changes['deleted']:
        if len(changes['deleted']) == 1:
            message_parts.append(f"🗑️ Удален {changes['deleted'][0]}")
        else:
            message_parts.append(f"🗑️ Удалено {len(changes['deleted'])} файлов")
    
    if not message_parts:
        return "🔄 Обновление проекта"
    
    return " | ".join(message_parts)

def categorize_files(files: list) -> dict:
    categories = {'python': 0, 'config': 0, 'documentation': 0, 'other': 0}
    
    for file in files:
        if file.endswith(('.py', '.pyw')):
            categories['python'] += 1
        elif file.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env')):
            categories['config'] += 1
        elif file.endswith(('.md', '.txt', '.rst', '.doc', '.docx')):
            categories['documentation'] += 1
        else:
            categories['other'] += 1
    
    return categories

def auto_commit_simple():
    result = subprocess.run(["git", "status", "--porcelain"], 
                          capture_output=True, text=True)
    changed_files = [f[3:] for f in result.stdout.strip().split('\n') if f] if result.stdout else []
    
    if not changed_files:
        print("❌ Нет изменений для коммита")
        return
    
    print("📁 Измененные файлы:")
    for i, file in enumerate(changed_files[:10], 1):
        print(f"  {i}. {file}")
    if len(changed_files) > 10:
        print(f"  ... и еще {len(changed_files) - 10} файлов")
    
    print("\n🎯 Тип изменений:")
    print("1. Новый функционал")
    print("2. Исправление ошибок") 
    print("3. Рефакторинг кода")
    print("4. Обновление документации")
    print("5. Другое")
    
    choice = input("Выберите тип изменений (1-5): ").strip()
    
    change_types = {
        '1': '🚀 Новый функционал',
        '2': '🐛 Исправление ошибок',
        '3': '♻️ Рефакторинг кода',
        '4': '📚 Обновление документации',
        '5': '🔧 Обновление проекта'
    }
    
    base_message = change_types.get(choice, '🔧 Обновление проекта')
    
    if choice == '5':
        custom_msg = input("Введите комментарий: ").strip()
        commit_message = f"{base_message}: {custom_msg}"
    else:
        file_count = len(changed_files)
        main_files = changed_files[:2]
        files_info = ", ".join(main_files)
        if file_count > 2:
            files_info += f" и еще {file_count - 2} файлов"
        
        commit_message = f"{base_message} | {files_info}"
    
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')
    os.system("git push")
    
    print(f"✅ Коммит выполнен: {commit_message}")

if __name__ == "__main__":
    auto_commit()