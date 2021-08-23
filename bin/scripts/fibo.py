def fibonacci(n):
    x, y = 0, 1
    for i in range(n):
        print(x, len(str(x)))
        x, y = y, x+y

fibonacci(250)
