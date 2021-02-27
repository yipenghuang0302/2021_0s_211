#!/usr/bin/python3

import random
import os
import datetime
import subprocess

# https://stackoverflow.com/questions/1604464/twos-complement-in-python
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val & ((2 ** bits) - 1)     # return positive value, masked

def generate_test ( filenum, neg0=False, neg1=False, bound=128, path="./" ):

    minuend    = random.randrange(-bound, 0) if neg0 else random.randrange(bound)
    subtrahend = random.randrange(-bound, 0) if neg1 else random.randrange(bound)
    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write( format(twos_comp(minuend    ,8), '08b') + '\n' )
        infile.write( format(twos_comp(subtrahend ,8), '08b') + '\n' )

    difference = minuend - subtrahend
    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write( format(twos_comp(difference,8), '08b') + '\n' )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, False, False, 8 )
    generate_test ( 1, False, True, 8 )
    generate_test ( 2, True, False, 8 )
    generate_test ( 3, True, True, 8 )

    generate_test ( 4, False, False, 128 )
    generate_test ( 5, False, True, 128 )
    generate_test ( 6, True, False, 128 )
    generate_test ( 7, True, True, 128 )

def test_binSub ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./binSub', "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )
        if verbose:
            print (' '.join(result.args))
            print ("answer")
            print (answer)
            print ("result")
            print (result.stdout)
        assert int(answer,2) == int(result.stdout,2), "The printed result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./binSub returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a binary number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_binSub( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
        score += 2
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile binSub.")
        return score

    if test_binSub(0,path,verbose):
        score += 1
        if test_binSub(1,path,verbose):
            score += 1
            if test_binSub(2,path,verbose):
                score += 2
                if test_binSub(3,path,verbose):
                    score += 2
                    if test_binSub(4,path,verbose):
                        score += 2
                        if test_binSub(5,path,verbose):
                            score += 2
                            if test_binSub(6,path,verbose):
                                score += 2
                                if test_binSub(7,path,verbose):
                                    score += 2

                                    allpass = True
                                    for filenum in range(8,16):
                                        generate_test (
                                            filenum,
                                            bool(random.getrandbits(1)),
                                            bool(random.getrandbits(1)),
                                            path=path
                                        )
                                        allpass &= test_binSub(filenum,path,verbose)
                                    if allpass:
                                        score += 8

    print ("Score on binSub: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_binSub(verbose=True)
    exit()
