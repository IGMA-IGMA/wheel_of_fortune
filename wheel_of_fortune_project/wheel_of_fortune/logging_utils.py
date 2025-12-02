import functools
import logging
import time
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])

logging.basicConfig(
    filename="game.log",
    filemode="a",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger("wheel_of_fortune")

def log_errors(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception in {func.__module__}.{func.__name__}: {e}")
            raise
    return wrapper  # type: ignore

def timer(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"Call {func.__module__}.{func.__name__} took {elapsed:.3f} sec")
        return result
    return wrapper  # type: ignore
