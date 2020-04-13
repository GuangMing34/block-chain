with open ('new.txt', 'r') as f:
    len_s = f.read(5)
    print(len(len_s))
    len_s = f.read(5)
    print(len(len_s))

'''
    while True:
        line = f.readline()
        if line == "":
            print("exit:")
            break
        if line == "\n":
            print("blank")
        else:
            print("xxx")
'''