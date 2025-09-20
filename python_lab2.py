def make_list(gap: list) -> list:
    ''' Получает два числа - границы промежутка и возвращает заполненный промежуток'''
    list1 = list(range(gap[0], gap[1]+1))
    return list1

def guess_number(type_of_alg: int, number: int, gap_list: list) -> list:
    '''Поиск числа в списке с помощью двух алгоритмов на выбор'''
    count_of_compare = 1
    #Алгоритм бинарного поиска в списке
    if type_of_alg == 2:
        st = 0
        end = len(gap_list)
        mid = (st + end) // 2
        while gap_list[mid] != number:
            if gap_list[mid] < number:
                st = mid
            elif gap_list[mid] > number:
                end = mid
            count_of_compare += 1
            mid = (st + end) // 2
    # Алгоритм медленного поиска в списке
    elif type_of_alg == 1:
        mid = 0
        while gap_list[mid] != number:
            mid += 1
            count_of_compare += 1
    return gap_list[mid], count_of_compare

def main():
    '''Главная функция, содержащая ввод и вывод данных'''
    number = int(input('Your number = '))
    gap = sorted(list(map(int, input('Your gap = ').split())))
    type_of_alg = int(input('Your type = '))
    result, n_of_attempts = guess_number(type_of_alg, number, make_list(gap))
    return result, n_of_attempts
print(main())