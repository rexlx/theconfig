import sys

# x = int(sys.argv[1])
# factors = {}

def jeez(x):
    factors = {}
    for i in range(1, (x+1)):
        if x % i == 0:
            y = x / i
            if y == x:
                continue
            factors[str(i)] = str(y)
    num = [float(e) for e in factors.values()]

    if sum(num) == x:
        print(f"{x} is perfect")
        print(num, x)

for i in range(1, 8888):
    jeez(i)