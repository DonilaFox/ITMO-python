import sys
import functools
import logging
from typing import Callable, Any, Optional

def logger(func=None, *, handle=sys.stdout):
    """
    Параметризуемый декоратор для логирования вызовов функции.
    Поддерживает:
        - sys.stdout / sys.stderr (или любой file-like объект с .write())
        - io.StringIO / другие file-like объекты
        - logging.Logger — тогда использует .info() и .error()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            use_logging = isinstance(handle, logging.Logger)

            # Форматирование аргументов
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            if use_logging:
                handle.info(f"Вызов функции {func.__name__} с аргументами: ({signature})")
            else:
                handle.write(f"INFO: Вызов функции {func.__name__} с аргументами: ({signature})\n")

            try:
                result = func(*args, **kwargs)
                if use_logging:
                    handle.info(f"Функция {func.__name__} успешно завершена. Результат: {repr(result)}")
                else:
                    handle.write(f"INFO: Функция {func.__name__} успешно завершена. Результат: {repr(result)}\n")
                return result
            except Exception as e:
                if use_logging:
                    handle.error(f"Исключение в функции {func.__name__}: {type(e).__name__}: {e}")
                else:
                    handle.write(f"ERROR: Исключение в функции {func.__name__}: {type(e).__name__}: {e}\n")
                raise
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)