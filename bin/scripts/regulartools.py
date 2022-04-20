import os


def get_factors(n):
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append((i, (n / i)))
    return factors


def conv_bytes(n):
    for i in ['  B', 'KiB', 'GiB', 'TiB', 'PiB']:
        # if the number is LT 1k || GT PiB, break loop
        if n < 1024 or i == "PiB":
            break
        n /= 1024.0
    # return f-string like: "114.95 MiB"
    return f"{n:7.2f} {i}"


def is_perfect(n):
    """determine if an integer is "perfect"
    
    factors is a list of tuples, unpack into:
    (for n=28) [(1, 2, 4, 7, 14), (28.0, 14.0, 7.0, 4.0, 2.0)]
    then sum the first element (1, 2, 4, 7, 14)

    Args:
        n (list): a list of tuples

    Returns:
        bool: 
    """
    factors = get_factors(n)
    if factors:
        result = sum(list(zip(*factors))[0])
        return True if result == n else False
    return False


def is_prime(n):
    factors = get_factors(n)
    return True if len(factors) == 1 else False


def sum_seq(n1, n2):
    return n2 * (n1 + n2) / 2



def get_files(source):
    """Using the os walk function, recursively get a list of files in
       the target directory. Returns a list of strings

    Args:
        source (str): directory path

    Returns:
        list: list of strings
    """
    # list comprehension joins the direcctory path and file name
    file_list = [os.path.join(dir_path, x)
                 for dir_path, dirs, files in os.walk(source)
                 for x in files]
    return file_list


def checkdir(target):
    try:
        # create the path if it doesnt exist
        if not os.path.exists(target):
            os.makedirs(target)
            return f"created {target}"
    except Exception as e:
        return f"checkdir() got an error! --> {e}"
