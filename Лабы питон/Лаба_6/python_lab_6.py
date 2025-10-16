import timeit
import matplotlib.pyplot as plt
import random
from collections import deque

def build_tree_iterative(root1: int = 6, height: int = 5, left_function=lambda x: x * 2 - 2, right_function=lambda x: x + 4) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''
    #Создаём список, состоящий из значений всех узлов дерева - каждые 2**(n-1) соответстуют n-ой высоте дерева
    nodes = [root1]
    for i in range (1, height):
        nodes_help = []
        for j in nodes[2**(i-1)-1:]:
            nodes_help.append(left_function(j))
            nodes_help.append(right_function(j))
        nodes += nodes_help

    if not nodes:
        return {}

    tree = {}
    queue = deque()

    # Добавляем корневой узел
    if len(nodes) > 0:
        tree['root'] = nodes[0]
        queue.append(('root', 0))

    # Обрабатываем остальные узлы
    while queue:
        current_path, current_index = queue.popleft()

        # Вычисляем индексы левого и правого потомков
        left_index = 2 * current_index + 1
        right_index = 2 * current_index + 2

        # Добавляем левого потомка, если он существует в списке
        if left_index < len(nodes):
            left_path = f"{current_path}.left"
            tree[left_path] = nodes[left_index]
            queue.append((left_path, left_index))

        # Добавляем правого потомка, если он существует в списке
        if right_index < len(nodes):
            right_path = f"{current_path}.right"
            tree[right_path] = nodes[right_index]
            queue.append((right_path, right_index))

    return tree

def build_tree_recursive(root: int, height: int, left_function=lambda x: x * 2 - 2, right_function=lambda x: x + 4) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''


    def building(current_height: int, current_root: int) -> dict:
        '''Рекурсия для построения дерева'''
        if current_height <= 0:
            return None
        # Вычисляем потомков по заданным формулам

        left_value = left_function(current_root)
        right_value = right_function(current_root)

        # Рекурсивно строим левое и правое поддеревья
        left_subtree = building(current_height - 1, left_value)
        right_subtree = building(current_height - 1, right_value)

        # Формируем общую ветку
        branch = {'root': current_root}
        if left_subtree is not None:
            branch['left'] = left_subtree
        if right_subtree is not None:
            branch['right'] = right_subtree

        return branch

    return building(height, root)

from functools import cache
@cache
def build_tree_iterative_cache(root1: int = 6, height: int = 5, left_function=lambda x: x * 2 - 2, right_function=lambda x: x + 4) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''
    #Создаём список, состоящий из значений всех узлов дерева - каждые 2**(n-1) соответстуют n-ой высоте дерева
    nodes = [root1]
    for i in range (1, height):
        nodes_help = []
        for j in nodes[2**(i-1)-1:]:
            nodes_help.append(left_function(j))
            nodes_help.append(right_function(j))
        nodes += nodes_help

    if not nodes:
        return {}

    tree = {}
    queue = deque()

    # Добавляем корневой узел
    if len(nodes) > 0:
        tree['root'] = nodes[0]
        queue.append(('root', 0))

    # Обрабатываем остальные узлы
    while queue:
        current_path, current_index = queue.popleft()

        # Вычисляем индексы левого и правого потомков
        left_index = 2 * current_index + 1
        right_index = 2 * current_index + 2

        # Добавляем левого потомка, если он существует в списке
        if left_index < len(nodes):
            left_path = f"{current_path}.left"
            tree[left_path] = nodes[left_index]
            queue.append((left_path, left_index))

        # Добавляем правого потомка, если он существует в списке
        if right_index < len(nodes):
            right_path = f"{current_path}.right"
            tree[right_path] = nodes[right_index]
            queue.append((right_path, right_index))

    return tree

@cache
def build_tree_recursive_cache(root: int, height: int, left_function=lambda x: x * 2 - 2, right_function=lambda x: x + 4) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''


    def building(current_height: int, current_root: int) -> dict:
        '''Рекурсия для построения дерева'''
        if current_height <= 0:
            return None
        # Вычисляем потомков по заданным формулам

        left_value = left_function(current_root)
        right_value = right_function(current_root)

        # Рекурсивно строим левое и правое поддеревья
        left_subtree = building(current_height - 1, left_value)
        right_subtree = building(current_height - 1, right_value)

        # Формируем общую ветку
        branch = {'root': current_root}
        if left_subtree is not None:
            branch['left'] = left_subtree
        if right_subtree is not None:
            branch['right'] = right_subtree

        return branch

    return building(height, root)

def benchmark(function, root, height, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: function(root, height), number=5, repeat=repeat)
    return min(times)



def main():
    # фиксированный набор данных
    random.seed(52)
    test_data = list(range(1, 21))

    res_recursive = []
    res_iterative = []

    for n in test_data:
        res_recursive.append(benchmark(build_tree_recursive, 6, n))
        res_iterative.append(benchmark(build_tree_iterative, 6, n))


    # График
    plt.plot(test_data, res_recursive, label="Рекурсивный без кэширования")
    plt.plot(test_data, res_iterative, label="Итеративный без кэширования")

    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного построений бинарного дерева")
    plt.legend()
    plt.show()



def cache_compare():
    # фиксированный набор данных
    random.seed(52)
    test_data = list(range(1, 21))

    res_recursive_cache = []
    res_iterative_cache = []

    for n in test_data:

        res_recursive_cache.append(benchmark(build_tree_recursive_cache, 6, n))
        res_iterative_cache.append(benchmark(build_tree_iterative_cache, 6, n))

    # График
    plt.plot(test_data, res_recursive_cache, label="Рекурсивный с кэшированием")
    plt.plot(test_data, res_iterative_cache, label="Итеративный с кэшированием")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного построений бинарного дерева с кэшированием и без")
    plt.legend()
    plt.show()

def recursive_compare():
    # фиксированный набор данных
    random.seed(52)
    test_data = list(range(1, 21))

    res_recursive = []
    res_recursive_cache = []

    for n in test_data:

        res_recursive.append(benchmark(build_tree_recursive, 6, n))
        res_recursive_cache.append(benchmark(build_tree_recursive_cache, 6, n))

    # График
    plt.plot(test_data, res_recursive, label="Рекурсивный без кэширования")
    plt.plot(test_data, res_recursive_cache, label="Рекурсивный с кэшированием")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного построения бинарного дерева с кэшированием и без")
    plt.legend()
    plt.show()

def iterative_compare():
    # фиксированный набор данных
    random.seed(52)
    test_data = list(range(1, 21))

    res_iterative = []
    res_iterative_cache = []

    for n in test_data:

        res_iterative.append(benchmark(build_tree_recursive, 6, n))
        res_iterative_cache.append(benchmark(build_tree_recursive_cache, 6, n))

    # График
    plt.plot(test_data, res_iterative, label="Итеративный без кэширования")
    plt.plot(test_data, res_iterative_cache, label="Итеративный с кэшированием")
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение итеративного построения бинарного дерева с кэшированием и без")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    iterative_compare()


print()