# obviously just doing a sum on a range of numbers is easier but...

def sum_seq(n1, n2):
    seq = range(n1, (n2+1))
    return n2 * (n1 + n2) / 2

print(sum_seq(1, 500))
