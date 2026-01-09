l1 = [2, 4, 3]
l2 = [5, 6, 4]

result = int("".join(map(str, l1)))
result1 = int("".join(map(str, l2)))

a = result1 + result

arr = list(map(int, str(a)))
print(arr)