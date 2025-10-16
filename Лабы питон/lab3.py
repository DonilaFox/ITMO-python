def gen_bin_tree(root: int, height: int) -> dict:
    '''Построение бинарного дерева по заданным корню, высоте'''
    def left_function1(current_value: int) -> int:
        '''Задает правило построения левой ветви'''
        return current_value * 2 - 2

    def right_function1(current_value: int) -> int:
        '''Задает правило построения правой ветви'''
        return current_value + 4

    def building(current_height: int, current_root: int) -> dict:
        '''Рекурсия для построения дерева'''
        if current_height <= 0:
            return None
        # Вычисляем потомков по заданным формулам

        left_value = left_function1(current_root)
        right_value = right_function1(current_root)

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
print(gen_bin_tree(6,5))