n = int(input())
if n < 15528:
    tax = 0
elif n >= 15528 and n < 42708:
    tax = 15
elif n >= 42708 and n < 132407:
    tax = 25
elif n >= 132407:
    tax = 28
s_tax = 0
if tax != 0:
    s_tax = int(round(n * (tax / 100), 0))
print(f"The tax for {n} is {tax}%. That is {s_tax} dollars!")
