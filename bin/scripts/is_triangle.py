def is_triangle(*args):
    """using a tuple supplied as a parameter, determine if its contents
    form a triangle, and if so, which kind

    Returns:
        str: a string describing the type of triangle
    """

    # this try block determines if all the items in the tuple are
    # numbers
    try:
        # if one or more were a string, the sum will fail
        sum(args)
    except TypeError as e:
        # i will use f strings where formatting is needed
        return f"expected three numbers separated by comma\n{e}"

    # if the length of the tuple is greater then 3, it isnt a triangle
    if len(args) > 3:
        return f"error!, expected three numbers, got {len(args)}"

    # the base doesnt have to be the longest side, but we need to know
    # which side is the longest
    base = max(args)
    # because if the sum of the two sides are GTE to the longest, then
    # then that isnt a shape at all
    if not (sum(args) - base) >= base:
        return "error! two sides must be GTE to its longest!"
    # a set only contains unique items, this will remove duplicates.
    uniq_sides = set(args)
    # there for the len of the set tells us the kind of triangle
    if len(uniq_sides) == 3:
        return "this triangle is scalene!"
    if len(uniq_sides) == 2:
        return "this triangle is isosceles!"
    if len(uniq_sides) == 1:
        return "this triangle is equilateral!"
    

# if this script is being ran as itself (not imported), then run.
if __name__ == "__main__":
    result = is_triangle(23, 22, 44)
    print(result)