import timeit
import math
import sys

# Импорт базовых версий
from iteration1 import integrate
from iteration2 import integrate_thread
from iteration3 import integrate_process

# === Попытка импорта Cython-версий ===
CYTHON_AVAILABLE = False
NOGIL_AVAILABLE = False

try:
    from iteration4 import integrate_cython
    CYTHON_AVAILABLE = True
except ImportError:
    print("⚠️  Обычная Cython-версия (с GIL) не найдена.")

try:
    from integrate_cython_nogil import integrate_cos_cython_nogil
    NOGIL_AVAILABLE = True

    # Создаём многопоточную обёртку для nogil-версии
    import threading

    def integrate_cos_thread_nogil(a, b, *, n_jobs=2, n_iter=1_000_000):
        if n_jobs <= 0:
            raise ValueError("n_jobs must be positive")
        if n_iter < n_jobs:
            n_iter = n_jobs

        step = (b - a) / n_jobs
        base = n_iter // n_jobs
        rem = n_iter % n_jobs
        results = [0.0] * n_jobs
        threads = []

        def worker(i):
            ca = a + i * step
            cb = a + (i + 1) * step
            cn = base + (1 if i < rem else 0)
            res = integrate_cos_cython_nogil(ca, cb, cn)
            if res == -10.0:  # ошибка
                raise ValueError("Invalid n_iter in nogil function")
            results[i] = res

        for i in range(n_jobs):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return sum(results)

except ImportError:
    print("⚠️  Cython-версия без GIL (nogil) не найдена.")
    integrate_cos_thread_nogil = None


def run_benchmark():
    f = math.cos
    a, b = 0, 100000
    exact = 1.0
    n_iter = 10_000_000
    n_jobs_list = [2, 4, 6, 8]

    print("Интегрирование cos(x) от 0 до 100000")
    print(f"Число итераций: {n_iter:,}")
    print("=" * 100)

    # --- Однопоточные версии ---
    print("\n Однопоточные реализации:")
    time_seq = timeit.timeit(lambda: integrate(f, a, b, n_iter=n_iter), number=1)
    res_seq = integrate(f, a, b, n_iter=n_iter)
    print(f"Python (обычный):       {time_seq:.4f} с, ошибка = {abs(res_seq - exact):.1e}")

    if CYTHON_AVAILABLE:
        time_cython = timeit.timeit(lambda: integrate_cython(f, a, b, n_iter=n_iter), number=1)
        res_cython = integrate_cython(f, a, b, n_iter=n_iter)
        speedup_cython = time_seq / time_cython
        print(f"Cython (с GIL):         {time_cython:.4f} с, ошибка = {abs(res_cython - exact):.1e}")
    else:
        time_cython = None
        speedup_cython = 1.0

    # --- Многопоточные и многопроцессные ---
    print("\n" + "="*100)
    header = f"{'n_jobs':<8} | {'Потоки (GIL)':<14} | {'Потоки (nogil)':<16} | {'Процессы':<12} | {'Ошибка (потоки nogil)'}"
    print(header)
    print("-" * len(header))

    for n_jobs in n_jobs_list:
        # 1. Потоки с GIL (обычные)
        time_t_gil = timeit.timeit(
            lambda: integrate_thread(f, a, b, n_jobs=n_jobs, n_iter=n_iter),
            number=1
        )
        res_t_gil = integrate_thread(f, a, b, n_jobs=n_jobs, n_iter=n_iter)

        # 2. Потоки без GIL (если доступны)
        if NOGIL_AVAILABLE:
            time_t_nogil = timeit.timeit(
                lambda: integrate_cos_thread_nogil(a, b, n_jobs=n_jobs, n_iter=n_iter),
                number=1
            )
            res_t_nogil = integrate_cos_thread_nogil(a, b, n_jobs=n_jobs, n_iter=n_iter)
            err_nogil = abs(res_t_nogil - exact)
        else:
            time_t_nogil = float('nan')
            err_nogil = float('nan')

        # 3. Процессы
        time_p = timeit.timeit(
            lambda: integrate_process(f, a, b, n_jobs=n_jobs, n_iter=n_iter),
            number=1
        )
        res_p = integrate_process(f, a, b, n_jobs=n_jobs, n_iter=n_iter)

        # Вывод строки
        nogil_str = f"{time_t_nogil:<16.4f}" if NOGIL_AVAILABLE else " недоступно"
        err_str = f"{err_nogil:.1e}" if NOGIL_AVAILABLE else "—"
        print(f"{n_jobs:<8} | {time_t_gil:<14.4f} | {nogil_str} | {time_p:<12.4f} | {err_str}")

    # --- Процессы + Cython (если доступно) ---
    if CYTHON_AVAILABLE:
        print("\n" + "="*100)
        print(" Многопроцессная версия с Cython (ProcessPool + Cython):")
        from concurrent.futures import ProcessPoolExecutor

        def integrate_process_cython(f, a, b, *, n_jobs=2, n_iter=1_000_000):
            step = (b - a) / n_jobs
            base = n_iter // n_jobs
            rem = n_iter % n_jobs
            with ProcessPoolExecutor(max_workers=n_jobs) as ex:
                futures = []
                for i in range(n_jobs):
                    ca = a + i * step
                    cb = a + (i + 1) * step
                    cn = base + (1 if i < rem else 0)
                    futures.append(ex.submit(integrate_cython, f, ca, cb, n_iter=cn))
                return sum(fut.result() for fut in futures)

        for n_jobs in n_jobs_list:
            time_pc = timeit.timeit(
                lambda: integrate_process_cython(f, a, b, n_jobs=n_jobs, n_iter=n_iter),
                number=1
            )
            res_pc = integrate_process_cython(f, a, b, n_jobs=n_jobs, n_iter=n_iter)
            print(f"  {n_jobs} процессов: {time_pc:.4f} с, ошибка = {abs(res_pc - exact):.1e}")



if __name__ == "__main__":
    run_benchmark()