import functools
import time
from datetime import datetime

def log_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def log_and_print_error(error, error_message_prefix):
            """Вспомогательная функция для записи ошибки"""
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            error_msg = f"[{timestamp}] ERROR: {type(error).__name__} - {error}\n"

            with open('game.log', 'a', encoding='utf-8') as log_file:
                log_file.write(error_msg)
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            log_and_print_error(e, "Файл не найден")
            raise  # Пробрасывает ошибку дальше
        except ValueError as e:
            log_and_print_error(e, "Некорректное значение")
            raise

        except PermissionError as e:
            log_and_print_error(e, "Нет прав доступа")
            raise

        except Exception as e:
            log_and_print_error(e, "Неожиданная ошибка")
            raise
        
    return wrapper

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        elapsed = end_time - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        print(f'\nВремя игры: {minutes} мин {seconds} сек\n')

        return result

    return wrapper