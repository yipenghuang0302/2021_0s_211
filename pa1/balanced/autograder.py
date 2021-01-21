#!/usr/bin/python3

import os
import random
import subprocess

def flip(p):
    return random.random() < p

def generate_test ( filenum, length, balancedProb, prefix=None ):

    braces = {
        0: ('<','>'),
        1: ('(',')'),
        2: ('[',']'),
        3: ('{','}'),
    }

    stack = []
    string = ""

    allBalanced = True

    for _ in range(length):
        openNewBrace = bool(random.getrandbits(1))
        if openNewBrace:
            braceType = braces.get(random.randrange(4))
            stack.append(braceType)
            string += braceType[0]
        elif stack:
            char = stack.pop()[1]
            balanced = flip(balancedProb)
            if balanced:
                string += char
            allBalanced &= balanced
    while stack:
        string += stack.pop()[1]

    # print (string)
    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write(string)

    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        outfile.write("yes" if allBalanced else "no")

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 4, 0.75 )
    generate_test ( 1, 4, 0.5 )
    generate_test ( 2, 8, 0.9 )
    generate_test ( 3, 8, 0.25 )
    generate_test ( 4, 256, 0.999 )
    generate_test ( 5, 256, 0.9 )

def test_balanced( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/balanced {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        # print ("result")
        # print (result)
        assert answer == result, "Your answer doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./balanced returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_balanced( prefix=None, verbose=False ):

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
        print ("Couldn't compile balanced.")
        return score

    if test_balanced(0,prefix,verbose):
        score += 2
        if test_balanced(1,prefix,verbose):
            score += 2
            if test_balanced(2,prefix,verbose):
                score += 2
                if test_balanced(3,prefix,verbose):
                    score += 2
                    if test_balanced(4,prefix,verbose):
                        score += 3
                        if test_balanced(5,prefix,verbose):
                            score += 3

                            allpass = True
                            for filenum in range(6,12):
                                generate_test ( filenum, 65536, 0.99998, prefix )
                                allpass &= test_balanced(filenum,prefix,verbose)
                            if allpass:
                                score += 3

    print ("Score on balanced: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_balanced(verbose=True)
    exit()
