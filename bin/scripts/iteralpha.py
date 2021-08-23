import string

alpha = string.ascii_lowercase

data = enumerate(alpha, 1)

for i, e in data:
    print(f"'{e}': {i},")