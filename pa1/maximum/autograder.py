#!/usr/bin/python3

import os
import random
import subprocess
import heapq

def generate_test ( filenum, countmax, nummax, prefix=None ):

    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        numcount = random.randrange(1,countmax)
        infile.write(str(numcount)+"\n")
        maxcount = random.randrange(numcount)
        infile.write(str(maxcount)+"\n")
        randnums = [ random.randrange(-nummax,nummax) for _ in range(numcount) ]
        for randnum in randnums:
            infile.write("{} ".format(randnum))

    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        for num in heapq.nlargest(maxcount,randnums):
            outfile.write("{} ".format(num))

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 4, 4 )
    generate_test ( 1, 16, 16 )
    generate_test ( 2, 65536, 65536 )
    generate_test ( 3, 16, 2147483647 )

def test_maximum( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "./"
    command += "maximum {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            maxlist = [ int(num) for num in outfile.read().split() ]
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        resultlist = [int(string) for string in result.split()]
        assert sorted(resultlist) == sorted(maxlist), "The maximum elements don't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./maximum returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_maximum( prefix=None, verbose=False ):

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
        print ("Couldn't compile maximum.")
        return score

    if test_maximum(0,prefix,verbose):
        score += 3
        if test_maximum(1,prefix,verbose):
            score += 3
            if test_maximum(2,prefix,verbose):
                score += 3
                if test_maximum(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,6):
                        generate_test ( filenum, 16, 2147483647, prefix )
                        allpass &= test_maximum(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on maximum: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_maximum(verbose=True)
    exit()
