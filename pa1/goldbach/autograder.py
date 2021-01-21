#!/usr/bin/python3

import subprocess
from math import sqrt
from itertools import count, islice
import random

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))

def validate_string( number, string ):

    lrval = string.strip().split('=')
    assert len(lrval)==2, "Invalid output format."

    assert int(lrval[0])==number, "The original number should be on the left of the equals sign."

    rval = [int(s) for s in lrval[1].split('+')]
    assert len(rval) == 3, "Exactly three numbers should be on the right of the equals sign."
    assert is_prime(rval[0]), "{} not a prime number.".format(rval[0])
    assert is_prime(rval[1]), "{} not a prime number.".format(rval[1])
    assert is_prime(rval[2]), "{} not a prime number.".format(rval[2])
    assert rval[0]+rval[1]+rval[2] == number, "Three numbers should sum to the original number."

def test_goldbach( number, prefix=None, verbose=False ):

    command = prefix if prefix else '.'
    command += "/goldbach {}".format(number)
    if verbose:
        print (command)
    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        validate_string (number, result)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./goldbach returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_goldbach( prefix=None, verbose=False ):

    score = 0

    command = "make"
    if prefix:
        command += " --directory=" + prefix
    if verbose:
        print (command)
    try:
        subprocess.check_output(command, shell=True)
        score += 5
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile goldbach.")
        return score

    if test_goldbach(7,prefix,verbose):
        score += 5

        if test_goldbach(49,prefix,verbose):
            score += 5

            allpass = True
            for _ in range(20):
                number = random.randrange(3,100)*2 + 1
                allpass &= test_goldbach(number,prefix,verbose)
            if allpass:
                score += 7

    print ("Score on goldbach: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    grade_goldbach(verbose=True)
    exit()
