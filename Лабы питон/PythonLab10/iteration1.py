import math
from typing import Callable

def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100_000) -> float:
    """
    Численно интегрирует функцию f на отрезке [a, b] методом левых прямоугольников.

    Args:
    f : Callable[[float], float]
        Интегрируемая функция одной переменной.
    a : float
        Начало интервала интегрирования.
    b : float
        Конец интервала интегрирования.
    n_iter : int, по умолчанию 100_000
        Количество подынтервалов (чем больше, тем точнее результат).

    Returns:
    float
        Приближённое значение определённого интеграла ∫_a^b f(x) dx.

    Raises:
        ValueError: Если n_iter <= 0.

    Examples:
        >>> import math
        >>> result = integrate(math.sin, 0, math.pi, n_iter=100_000)
        >>> abs(result - 2.0) < 1e-3
        True

        >>> result = integrate(lambda x: x**2, 0, 2, n_iter=100_000)
        >>> abs(result - (8/3)) < 1e-3
        True
    """
    if n_iter <= 0:
        raise ValueError("n_iter must be a positive integer")
    if a > b:
        return -integrate(f, b, a, n_iter=n_iter)

    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc




