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

def generate_test ( filenum, negative=False, bound=32768, path="./" ):

    number = random.randrange(-bound, 0) if negative else random.randrange(bound)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write(str(number))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write(format(twos_comp(number,16), '04X'))

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, False, 128 )
    generate_test ( 1, False )
    generate_test ( 2, True, 128 )
    generate_test ( 3, True )

def test_toHex ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./toHex', "tests/test{}.txt".format(filenum)],
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
        assert int(answer,16) == int(result.stdout,16), "The printed result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./toHex returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a hexadecimal number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_toHex( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
        score += 2
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile toHex.")
        return score

    if test_toHex(0,path,verbose):
        score += 3
        if test_toHex(1,path,verbose):
            score += 3
            if test_toHex(2,path,verbose):
                score += 4
                if test_toHex(3,path,verbose):
                    score += 4

                    allpass = True
                    for filenum in range(4,16):
                        generate_test ( filenum, bool(random.getrandbits(1)), path=path )
                        allpass &= test_toHex(filenum,path,verbose)
                    if allpass:
                        score += 8

    print ("Score on toHex: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_toHex(verbose=True)
    exit()
