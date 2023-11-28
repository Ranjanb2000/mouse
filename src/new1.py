inp = input()
word = "abcdefghijklmnopqrstuvwxyz"
for i in word:
    if i not in inp:
        print("'"+i+"'",end = " ")