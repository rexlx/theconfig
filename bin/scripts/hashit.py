#!/usr/bin/python3

"""
Encrypts plain text using a specified method from the command line
example:  (dep stands for dumb encryption protocol)

[user ~ ]$ /usr/bin/python3 hashit.py YOUR_method
"""

import sys
import random
import pickle
import copy
import os
import getpass

def hashit(method):
    """
    a function that encodes a file with a specified method
    and creates a converted data file
    """
    user_string = []
    new_string = []
    encoder = open(method, 'rb')
    active = True
    ## while active is true
    while active:
        try:
            ## dump data into 'contents' until EOF
            contents = pickle.load(encoder)
        except EOFError:
            ## if EOF, active is false
            active = False

    userdata = getpass.getpass('Enter your text\t')
    for ch in userdata:
        user_string.append(ch)
        ## if the character is in the conversion pool
        if ch in contents:
            ## convert character
            new_string.append(contents[ch])
        else:
            ## keep character as is, (rare)
            #ch.encode('utf-8').strip()
            new_string.append(ch)
            ## repeat

    hash = ''.join(str(e) for e in new_string)
    print(hash)


hashit(sys.argv[1])
