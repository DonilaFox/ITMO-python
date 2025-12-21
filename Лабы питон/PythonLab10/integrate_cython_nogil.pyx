# integrate_cython_nogil.pyx
import cython
from libc.math cimport cos as c_cos

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef double integrate_cos_cython_nogil(double a, double b, int n_iter) nogil:
    """
    Интегрирует cos(x) на [a, b] методом левых прямоугольников без удержания GIL.
    Известно: ∫₀^{π/2} cos(x) dx = 1, ∫₀^π cos(x) dx = 0.
    """
    if n_iter <= 0:
        return -10.0  # специальное значение ошибки (нельзя исключение без GIL)

    cdef double acc = 0.0
    cdef double x
    cdef int i

    # Обрабатываем случай a > b без рекурсии
    if a > b:
        # ∫_a^b = -∫_b^a
        tmp = a
        a = b
        b = tmp
        # step будет положительным, но результат инвертируем в конце
        is_reversed = True
    else:
        is_reversed = False

    cdef double step = (b - a) / n_iter

    for i in range(n_iter):
        x = a + i * step
        acc += c_cos(x) * step

    if is_reversed:
        acc = -acc

    return acc