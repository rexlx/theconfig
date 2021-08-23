#!/usr/bin/python
import re, os, sys, time, argparse

def get_args():
    """
    this function collects one mandatory postional arg and two
    optional.
    """
    # create an instance of ArgumentParser named parser
    parser = argparse.ArgumentParser()
    # add the mandatory positional arg for the user pattern
    parser.add_argument("pattern", help="pattern to search for")
    # add an optional recursive arg
    parser.add_argument('-r', '--recursive', help="search everything",
                        action="store_true")
    # add the optional count arg
    parser.add_argument('-c', '--count', help="count matches",
                        action="store_true")
    # add the optional ignore case arg
    parser.add_argument('-i', '--ignore-case', help="search everything",
                        action="store_true")
    # add the optional show match only arg
    parser.add_argument('-o', '--show-match-only', help="count matches",
                        action="store_true")
    # parse it
    args = parser.parse_args()
    # store the values to be returned
    string = args.pattern
    # if you add the -r flag
    if args.recursive:
        # then you will go into subdirectories
        recursive = True
    else:
        recursive = False
    # if you add the -c flag
    if args.count:
    #count them matches
        count_matches = True
    else:
        count_matches = False
    # if you ignore the case
    if args.ignore_case:
        # set case value
        case = 'ignored'
    else:
        case = 'sensitive'
    # if you add the -o flag
    if args.show_match_only:
    # only show matched part of string
        match = True
    else:
        match = False
    # return the args for other functions to use
    return string, recursive, count_matches, case, match


def get_regex(pattern, case, line):
    """
    this function is called inside the search methods below
    checks for case sesnitivity here
    """
    if case == 'sensitive':
        result = re.search(pattern, line)
    else:
        result = re.search(pattern, line, re.IGNORECASE)
    return result



def search_the_surface(pattern, case, match):
    """
    this function will look into the current working directory
    for files and search them for a pattern
    """
    # list comprehension of the current working dir
    file_list = [e for e in os.listdir('.')]
    # test each item for its file-ness
    for item in file_list:
        if os.path.isfile(item):
            # if its a file, open it for reading
            try:
                with open(item) as f:
                    for line in f:
                        # search each line for the pattern
                        result = get_regex(pattern, case, line)
                        # if theres a match, print it
                        if match and result:
                            print(item + '\n' + str(result.group(0)))
                        elif result:
                            print(item + '\n' + line)
            # if we fail to open the file
            except Exception as e:
                # life goes on, inform the user and continue
                print('couldnt open ' + item)
                continue

def search_recursively(pattern, case, match):
    """
    refer to comments above, the difference is how the list
    comprehension is created
    """
    file_list = [os.path.join(dir_path, x)
                for dir_path, dirs, files in os.walk('.')
                for x in files]
    for item in file_list:
        if os.path.isfile(item):
            try:
                with open(item) as f:
                    for line in f:
                        result = get_regex(pattern, case, line)
                        if match and result:
                            print(item + '\n' + str(result.group(0)))
                        elif result:
                            print(item + '\n' + line)
            except Exception as e:
                print('couldnt open ' + item)
                continue

def count_shallow_matches(pattern, case):
    """
    counts the matches insted of printing them
    """
    count = 0
    file_list = [e for e in os.listdir('.')]
    for item in file_list:
        if os.path.isfile(item):
            try:
                with open(item) as f:
                    for line in f:
                        result = get_regex(pattern, case, line)
                        if result:
                            count += 1
            except Exception as e:
                continue
    print(count)


def count_recursive_matches(pattern, case):
    count = 0
    file_list = [os.path.join(dir_path, x)
                for dir_path, dirs, files in os.walk('.')
                for x in files]
    for item in file_list:
        if os.path.isfile(item):
            try:
                with open(item) as f:
                    for line in f:
                        result = get_regex(pattern, case, line)
                        if result:
                            count += 1
            except Exception as e:
                continue
    print(count)


# this is it
def main():
    # get the args
    pattern, recursive, count, case, match = get_args()
    # this evalutes to a non recursive scan (no args passed)
    if not recursive and not count:
        search_the_surface(pattern, case, match)
        #dont keep going
        sys.exit()
    # evaluates to recursive count (-r -c)
    if recursive and count:
        count_recursive_matches(pattern, case)
        sys.exit()
    # if -r
    if recursive:
        search_recursively(pattern, case, match)
    # if -c
    elif count:
        count_shallow_matches(pattern, case)
    # the search methods handle the -i and -o option, no other condition should
    # arise... i dont think
    else:
        print("""now you've done it, program terminated due to:
                 impossibilty""")
        sys.exit(1)

# do the thing
if __name__ == '__main__':
    main()
