import math
import pytest
from iteration1 import integrate

def test_integrate_cos():
    """Тест интегрирования cos(x) от 0 до pi/2."""
    result = integrate(math.cos, 0, math.pi / 2, n_iter=100)
    assert round(result, 5) == 1.00783

def test_integrate_sin_full_period():
    """Тест интегрирования sin(x) от 0 до 2π — должно быть близко к 0."""
    result = integrate(math.sin, 0, 2 * math.pi, n_iter=100_000)
    assert abs(result) < 1e-3  # погрешность мала

def test_integrate_negative_interval():
    """Интеграл от большего к меньшему — должен быть отрицательным."""
    res1 = integrate(math.sin, 0, math.pi, n_iter=1000)
    res2 = integrate(math.sin, math.pi, 0, n_iter=1000)
    assert abs(res1 + res2) < 1e-6

def test_integrate_zero_width():
    """Интеграл по нулевому интервалу — должен быть 0."""
    result = integrate(math.sin, 5, 5, n_iter=1000)
    assert result == 0.0

def test_invalid_n_iter():
    """Проверка ошибки при некорректном n_iter."""
    with pytest.raises(ValueError):
        integrate(math.sin, 0, 1, n_iter=0)
    with pytest.raises(ValueError):
        integrate(math.sin, 0, 1, n_iter=-10)