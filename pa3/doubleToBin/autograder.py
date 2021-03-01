#!/usr/bin/python3

import random
import os
import datetime
import subprocess
import struct
import sys

# https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!d', num))

def generate_test ( filenum, double=1.0, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write( str(double) )

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        bits = binary(double)
        outfile.write( bits[0] + '_' + bits[1:12] + '_' + bits[12:] )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 0.0 )
    generate_test ( 1, 1.0 )
    generate_test ( 2, -2.0 )
    generate_test ( 3, -0.5 )

    generate_test ( 4, -5./32 )
    generate_test ( 5, 3.625*16 )

def test_doubleToBin ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./doubleToBin', "tests/test{}.txt".format(filenum)],
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
        print ("Calling ./doubleToBin returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a binary number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_doubleToBin( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile doubleToBin.")
        return score

    if test_doubleToBin(0,path,verbose):
        score += 2
        if test_doubleToBin(1,path,verbose):
            score += 2
            if test_doubleToBin(2,path,verbose):
                score += 2
                if test_doubleToBin(3,path,verbose):
                    score += 2
                    if test_doubleToBin(4,path,verbose):
                        score += 3
                        if test_doubleToBin(5,path,verbose):
                            score += 3

                            # standard range test
                            allpass = True
                            for filenum in range(6,10):
                                generate_test (
                                    filenum,
                                    double = random.uniform(
                                        -65536.0,
                                        +65536.0,
                                    ),
                                    path=path
                                )
                                allpass &= test_doubleToBin(filenum,path,verbose)
                            if allpass:
                                score += 3

                            # high magnitude test
                            allpass = True
                            for filenum in range(10,14):
                                generate_test (
                                    filenum,
                                    double = random.uniform(
                                        0.,
                                        sys.float_info.max
                                    ),
                                    path=path
                                )
                                allpass &= test_doubleToBin(filenum,path,verbose)
                            if allpass:
                                score += 3

                            # denormalized range test
                            allpass = True
                            for filenum in range(14,18):
                                generate_test (
                                    filenum,
                                    double = random.uniform(
                                        -sys.float_info.min,
                                         sys.float_info.min,
                                    ),
                                    path=path
                                )
                                allpass &= test_doubleToBin(filenum,path,verbose)
                            if allpass:
                                score += 3

                            # negative zero test
                            generate_test ( 18, -0.0, path=path )
                            if test_doubleToBin(16,path,verbose):
                                score += 1

    print ("Score on doubleToBin: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_doubleToBin(verbose=True)
    exit()
