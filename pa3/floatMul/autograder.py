#!/usr/bin/python3

import random
import os
import datetime
import subprocess
import struct
import sys
import numpy as np # python by default uses double precision, so np used to force single precision

# https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))

def generate_test ( filenum, multiplier=1.0, multiplicand=1.0, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write( binary(multiplier)   + '\n' )
        infile.write( binary(multiplicand) + '\n' )

    product = np.float32(multiplier) * np.float32(multiplicand)
    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        bits = binary(product)
        outfile.write( bits[0] + '_' + bits[1:9] + '_' + bits[9:] )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 0.0, 1.0 )
    generate_test ( 1, -1.0, 1.0 )
    generate_test ( 2, -65536.0, 0.03125 )
    generate_test ( 3, 1.5, 0.625 )

def test_floatMul ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./floatMul', "tests/test{}.txt".format(filenum)],
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
        assert answer.replace('_','') == result.stdout.replace('_',''), "The printed result doesn't match answers/answer{}.txt. You can add underscores as needed for readability".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.stdout)
        print ("Calling ./floatMul returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a floating point number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_floatMul( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile floatMul.")
        return score

    if test_floatMul(0,path,verbose):
        score += 2
        if test_floatMul(1,path,verbose):
            score += 2
            if test_floatMul(2,path,verbose):
                score += 2
                if test_floatMul(3,path,verbose):
                    score += 2

                    # standard range test
                    for filenum in range(4,20):
                        generate_test (
                            filenum,
                            multiplier = random.uniform( -65536.0, +65536.0 ),
                            multiplicand = random.uniform( -65536.0, +65536.0 ),
                            path=path
                        )
                        if test_floatMul(filenum,path,verbose):
                            score += 1

    print ("Score on floatMul: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_floatMul(verbose=True)
    exit()
