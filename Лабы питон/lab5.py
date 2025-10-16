from collections import deque


def gen_bin_tree(root1: int = 6, height: int = 5, left_function=lambda x: x * 2 - 2, right_function=lambda x: x + 4) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''
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

print(gen_bin_tree(6, 3))