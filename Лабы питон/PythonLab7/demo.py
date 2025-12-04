import logging
import math

# Настройка логирования в файл quadratic.log
logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def solve_quadratic(a, b, c):
    logging.info(f"Solving equation: {a}x^2 + {b}x + {c} = 0")
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            logging.critical(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Coefficient '{name}' must be numeric")

    if a == 0:
        logging.error("Coefficient 'a' cannot be zero")
        raise ValueError("a cannot be zero")

    d = b * b - 4 * a * c
    logging.debug(f"Discriminant: {d}")

    if d < 0:
        logging.warning("Discriminant < 0: no real roots")
        return None

    if d == 0:
        x = -b / (2 * a)
        logging.info("One real root")
        return (x,)

    root1 = (-b + math.sqrt(d)) / (2 * a)
    root2 = (-b - math.sqrt(d)) / (2 * a)
    logging.info("Two real roots computed")
    return root1, root2


# Демонстрационные вызовы
if __name__ == "__main__":
    print("=== Демонстрация solve_quadratic с логированием ===")

    # Успешные случаи
    print("→ Два корня:", solve_quadratic(1, -5, 6))      # (3.0, 2.0)
    print("→ Один корень:", solve_quadratic(1, -4, 4))    # (2.0,)

    # Предупреждение: нет вещественных корней
    print("→ Нет вещественных корней:", solve_quadratic(1, 0, 1))  # None

    # Ошибка: a = 0
    try:
        solve_quadratic(0, 2, 3)
    except ValueError as e:
        print("→ Ошибка (a=0):", e)

    # Критическая ошибка: некорректный тип
    try:
        solve_quadratic("abc", 2, 3)
    except TypeError as e:
        print("→ Критическая ошибка (тип):", e)
