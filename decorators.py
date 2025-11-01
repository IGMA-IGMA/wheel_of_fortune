import functools
import sys
import time
import traceback
from datetime import datetime
from io import StringIO

def logging(log_file="game.log"):
    """Декоратор Логов"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            def log(level, message):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] {level}: {message}\n")
            
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            captured_stdout = StringIO()
            captured_stderr = StringIO()
            sys.stdout = captured_stdout
            sys.stderr = captured_stderr
            
            log("DEBUG", f"=== МАКСИМАЛЬНОЕ ЛОГИРОВАНИЕ ФУНКЦИИ '{func.__name__}' ===")
            log("DEBUG", f"Модуль: {func.__module__}")
            log("DEBUG", f"Файл: {sys.modules[func.__module__].__file__}")
            log("DEBUG", f"Позиционные аргументы: {args}")
            log("DEBUG", f"Именованные аргументы: {kwargs}")
            log("DEBUG", f"Время начала: {datetime.now()}")
            log("DEBUG", f"ID процесса: {os.getpid() if 'os' in sys.modules else 'N/A'}")
            
            try:
                log("INFO", f"ВЫПОЛНЕНИЕ ФУНКЦИИ НАЧАТО")
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                minutes = int(execution_time // 60)
                seconds = execution_time % 60
                
                log("INFO", f"ФУНКЦИЯ УСПЕШНО ЗАВЕРШЕНА")
                log("DEBUG", f"Возвращаемое значение: {result}")
                log("DEBUG", f"Тип возвращаемого значения: {type(result)}")
                log("INFO", f"Общее время выполнения: {minutes} мин {seconds:.2f} сек")
                log("DEBUG", f"Точное время выполнения: {execution_time:.6f} секунд")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                log("ERROR", f"КРИТИЧЕСКАЯ ОШИБКА В ФУНКЦИИ")
                log("ERROR", f"Тип ошибки: {type(e).__name__}")
                log("ERROR", f"Сообщение ошибки: {str(e)}")
                log("DEBUG", f"Полный traceback ошибки:")
                
                tb_lines = traceback.format_exc().split('\n')
                for line in tb_lines:
                    if line.strip():
                        log("DEBUG", f"    {line}")
                
                log("DEBUG", f"Время выполнения до ошибки: {execution_time:.6f} секунд")
                raise
                
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
                captured_stdout.seek(0)
                stdout_output = captured_stdout.read().strip()
                if stdout_output:
                    log("TERMINAL", "=== ВЫВОД В STDOUT ===")
                    for i, line in enumerate(stdout_output.split('\n'), 1):
                        log("TERMINAL", f"STDOUT[{i:03d}]: {line}")
                
                captured_stderr.seek(0)
                stderr_output = captured_stderr.read().strip()
                if stderr_output:
                    log("TERMINAL", "=== ВЫВОД В STDERR ===")
                    for i, line in enumerate(stderr_output.split('\n'), 1):
                        log("TERMINAL", f"STDERR[{i:03d}]: {line}")
                
                end_time = time.time()
                total_time = end_time - start_time
                log("DEBUG", f"=== ЗАВЕРШЕНИЕ ЛОГИРОВАНИЯ ФУНКЦИИ '{func.__name__}' ===")
                log("DEBUG", f"Общее время с учетом логирования: {total_time:.6f} секунд")
                log("DEBUG", f"Время окончания: {datetime.now()}")
                log("DEBUG", "=" * 80)
        
        return wrapper
    return decorator