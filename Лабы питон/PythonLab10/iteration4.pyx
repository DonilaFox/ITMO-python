# integrate_cython.pyx
import cython
from libc.math cimport sin as c_sin  # можно использовать для теста, но наша функция принимает Python-каллбэк

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython(object f, double a, double b, int n_iter=100000):
    """
    Оптимизированная версия integrate на Cython.
    Принимает Python-функцию f, но минимизирует overhead.
    """
    if n_iter <= 0:
        raise ValueError("n_iter must be a positive integer")
    if a > b:
        return -integrate_cython(f, b, a, n_iter)

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    cdef int i

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step

    return acc