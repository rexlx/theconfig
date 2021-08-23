import sys

def find_factors(x):
    factors = {}
    for i in range(1, x):
        if x % i == 0:
            y = x / i
            factors[str(i)] = str(y)
    return factors


def main():
    x = int(sys.argv[1])
    factors = find_factors(x)
    f_pad = max(len(e) for e in factors.keys()) + 1
    pad = max(len(e) for e in factors.values()) + 1

    for k, v in factors.items():
        print(k.ljust(f_pad) + v.ljust(pad))

if __name__ == "__main__":
    main()