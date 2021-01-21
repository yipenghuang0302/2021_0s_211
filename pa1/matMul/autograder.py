#!/usr/bin/python3

import os
import random
import subprocess
import numpy

def generate_test ( filenum, l, m, n, prefix=None ):

    matrix_a = [[random.randrange(8) for j in range(m)] for i in range(l)]
    matrix_b = [[random.randrange(8) for k in range(n)] for j in range(m)]
    matrix_c = numpy.matmul( matrix_a, matrix_b )

    with open("{}tests/matrix_a_{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(l))
        infile.write("{}\n".format(m))
        for i in range (l):
            for j in range (m):
                infile.write("{} ".format(matrix_a[i][j]))
            infile.write("\n")

    with open("{}tests/matrix_b_{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(m))
        infile.write("{}\n".format(n))
        for j in range (m):
            for k in range (n):
                infile.write("{} ".format(matrix_b[j][k]))
            infile.write("\n")

    with open("{}answers/matrix_c_{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        for i in range (l):
            for k in range (n):
                outfile.write("{} ".format(matrix_c[i][k]))

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 1, 1, 1 )
    generate_test ( 1, 1, 4, 1 )
    generate_test ( 2, 3, 2, 1 )
    generate_test ( 3, 2, 2, 2 )

def test_matMul ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/matMul {}tests/matrix_a_{}.txt {}tests/matrix_b_{}.txt".format( prefix if prefix else "", filenum, prefix if prefix else "", filenum )
    if verbose:
        print (command)

    try:
        with open("{}answers/matrix_c_{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answer = [ int(num) for num in outfile.read().split() ]
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/matrix_c_{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        resultlist = [int(string) for string in result.split()]
        # print ("answer")
        # print (answer)
        # print ("result")
        # print (result)
        assert resultlist == answer, "The matrix multiplication result doesn't match answers/matrix_c_{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./matMul returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_matMul( prefix=None, verbose=False ):

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
        print ("Couldn't compile matMul.")
        return score

    if test_matMul(0,prefix,verbose):
        score += 3
        if test_matMul(1,prefix,verbose):
            score += 3
            if test_matMul(2,prefix,verbose):
                score += 3
                if test_matMul(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 3, 4, 5, prefix )
                        allpass &= test_matMul(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on matMul: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_matMul(verbose=True)
    exit()
