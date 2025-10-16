nums = list(map(int, input('NUms: ').split(',')))
target = int(input('Target: '))
print(nums)
def sumdvuh(nums, target):
    x = y = 0
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                x = i
                y = j
                break
        if y != 0: break
    if y == 0:
        return -1
    else:
        return x, y
print(sumdvuh(nums, target))
