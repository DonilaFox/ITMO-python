import concurrent.futures as ftres
from typing import Callable
from iteration1 import integrate  # та же базовая функция
from iteration1 import integrate

def integrate_process(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 1_000_000
) -> float:
    """
    Численное интегрирование с использованием процессов (ProcessPoolExecutor).
    Эффективно для CPU-bound задач — обходит ограничения GIL.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be a positive integer")
    if n_iter < n_jobs:
        n_iter = n_jobs

    step = (b - a) / n_jobs
    base_chunk = n_iter // n_jobs
    remainder = n_iter % n_jobs

    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            chunk_a = a + i * step
            chunk_b = a + (i + 1) * step
            chunk_n_iter = base_chunk + (1 if i < remainder else 0)
            future = executor.submit(integrate, f, chunk_a, chunk_b, n_iter=chunk_n_iter)
            futures.append(future)
        total = sum(future.result() for future in futures)
    return total