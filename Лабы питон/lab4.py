import timeit
import matplotlib.pyplot as plt
import random

def fact_iterative(n: int) -> int:
    '''Итерактивный факториал'''
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
    return fact

from functools import cache
@cache

def fact_iterative_cache(n: int) -> int:
    '''Итерактивный факториал с кэшированием'''
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
    return fact


def benchmark(function, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: function(n), number=5, repeat=repeat)
    return min(times)



def main():
    # фиксированный набор данных
    random.seed(52)
    test_data = list(range(10, 700, 10))

    res_iterative = []
    res_iterative_cache = []

    for n in test_data:
        res_iterative.append(benchmark(fact_iterative, n))
        res_iterative_cache.append(benchmark(fact_iterative_cache, n))

    # График
    plt.plot(test_data, res_iterative, label="Итеративный без кэширования")
    plt.plot(test_data, res_iterative_cache, label="Итеративный с кэшированием")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение итеративного факториала с кэшированием и без")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
