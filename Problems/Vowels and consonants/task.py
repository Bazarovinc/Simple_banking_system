line = input()
for symbol in line:
    if symbol in "aeiou":
        print("vowel")
    elif symbol in "qwrtypsdfghjklzxcvbnm":
        print("consonant")
    else:
        break