num = input()
n_sum = 0
n = 0
while num != '.':
    n += 1
    n_sum += int(num)
    num = input()
print(n_sum / n)
