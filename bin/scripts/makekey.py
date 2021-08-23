#!/usr/bin/python3
"""
A python tool set
"""
import sys
import random
import pickle
import copy

def makekey(method, key):
    ## oens file to store key in
    keyfile = open(key, 'wb')
    methodfile = open(method, 'wb')
    ## defines some default values
    key = []
    working_pool = {}
    out_key = {}
    ## character map, gets copied to create character pools
    all_char = ['a', 'b', 'c', 'd', 'e',
                'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y',
                'z', 'A', 'B', 'C', 'D',
                'E', 'F', 'G', 'H', 'I',
                'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S',
                'T', 'U', 'V', 'W', 'X',
                'Y', 'Z', '0', '1', '2',
                '3', '4', '5', '6', '7',
                '8', '9', '!', '@', '#',
                '$', '%', '^', '&', '*',
                '+', '-', '_', '=', '~',
                ' ', '.', ',', ';', '(',
                ')', '<', '>', '?', ':',
                '|', '/', '[', ']', '{',
                '}', '\'', '"', '\t',
                '\n', '\\']
    ## above list copied
    char_copy = copy.deepcopy(all_char)
    pool = copy.deepcopy(all_char)

    ## for each character in the character map,
    for char in char_copy[:]:
        ## pick a random character from pool
        temp_char = random.choice(pool)
        ## appends working_pool dictionary
        ## {'random': 'actual'} EXAMPLE
        working_pool[temp_char] = char
        ## appends my_key dictionary, creates key
        ## {'actual': 'random'} EXAMPLE
        out_key[char] = temp_char
        ## remove the random character assigned
        ## from the pool so it cant be picked twice
        pool.remove(temp_char)
        pickle.dump(out_key, keyfile)
        pickle.dump(working_pool, methodfile)

if len(sys.argv) < 1:
    print('No names specified using defaults!')
    makekey('method.dep', 'key.dep')
elif len(sys.argv) == 2:
    print('Expected a method name and a key name, only got one! using default key name!')
    makekey(sys.argv[1], 'key.dep')
else:
    print(len(sys.argv))
#makekey(sys.argv[1], sys.argv[2])
