import get_factors as gf
import sys

x = int(sys.argv[1])
res = gf.find_factors(x)
if len(res.keys()) == 1:
    print(f"{x} is prime")
else:
    print(f"{x} has the following factors:")
    for k, v in res.items():
        print(k, v)
