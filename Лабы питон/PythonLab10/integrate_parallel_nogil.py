# integrate_parallel_nogil.py
import threading
from integrate_cython_nogil import integrate_cos_cython_nogil

def integrate_cos_parallel_nogil(a: float, b: float, *, n_jobs: int = 2, n_iter: int = 1_000_000) -> float:
    """
    Параллельное интегрирование cos(x) с использованием потоков и Cython-функции без GIL.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter < n_jobs:
        n_iter = n_jobs

    step = (b - a) / n_jobs
    base_chunk = n_iter // n_jobs
    remainder = n_iter % n_jobs

    results = [0.0] * n_jobs
    threads = []

    def worker(i: int):
        chunk_a = a + i * step
        chunk_b = a + (i + 1) * step
        chunk_n = base_chunk + (1 if i < remainder else 0)
        res = integrate_cos_cython_nogil(chunk_a, chunk_b, chunk_n)
        if res == -10.0:
            raise ValueError("n_iter must be positive")
        results[i] = res

    for i in range(n_jobs):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)