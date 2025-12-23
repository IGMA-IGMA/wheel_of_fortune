import linecache
import random


def random_word_generator(filename=r'C:\Users\IGMA\Desktop\wheel_of_fortune\wheel_of_fortune_project\wheeloffortune\data\words.txt'):
    # Подсчитываем количество строк вручную
    total_lines = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for _ in f:
            total_lines += 1

    used_lines = set()

    while len(used_lines) < total_lines:
        line_num = random.randint(1, total_lines)
        if line_num in used_lines:
            continue
        used_lines.add(line_num)
        word = linecache.getline(filename, line_num).strip()
        if word:
            yield word

    linecache.clearcache()


def entry_records(filename=r'C:\Users\IGMA\Desktop\wheel_of_fortune\wheel_of_fortune_project\wheeloffortune\data\record.txt'):
    records = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    name, score = line.split(':', 1)
                    try:
                        records[name.strip()] = int(score.strip())
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return records


def save_records(records, filename=r'C:\Users\IGMA\Desktop\wheel_of_fortune\wheel_of_fortune_project\wheeloffortune\data\words.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for name, score in records.items():
            f.write(f"{name}:{score}\n")


def update_record(player_name, score, filename=r'C:\Users\IGMA\Desktop\wheel_of_fortune\wheel_of_fortune_project\wheeloffortune\data\words.txt'):
    records = entry_records(filename)
    if player_name in records:
        if score > records[player_name]:
            records[player_name] = score
            save_records(records, filename)
            return True
        return False
    else:
        records[player_name] = score
        save_records(records, filename)
        return True


def get_high_scores(filename='data/record.txt'):
    return sorted(entry_records(filename).items(), key=lambda x: x[1], reverse=True)
