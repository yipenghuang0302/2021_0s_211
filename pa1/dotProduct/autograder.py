#!/usr/bin/python3

import os
import random
import subprocess
import numpy

def generate_test ( filenum, l, prefix=None ):

    vector_a = [random.random() for i in range(l)]
    vector_b = [random.random() for i in range(l)]
    dot_product = numpy.dot( vector_a, vector_b )

    with open("{}tests/vector_a_{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(l))
        for i in range (l):
            infile.write("{} ".format(vector_a[i]))

    with open("{}tests/vector_b_{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(l))
        for i in range (l):
            infile.write("{} ".format(vector_b[i]))

    with open("{}answers/dot_product_{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        outfile.write("{}".format(dot_product))

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 1 )
    generate_test ( 1, 4 )
    generate_test ( 2, 16 )
    generate_test ( 3, 256 )

def test_dotProduct ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/dotProduct {}tests/vector_a_{}.txt {}tests/vector_b_{}.txt".format( prefix if prefix else "", filenum, prefix if prefix else "", filenum )
    if verbose:
        print (command)

    try:
        with open("{}answers/dot_product_{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answer = float(outfile.read())
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/dot_product_{}.txt missing".format(filenum))

    try:
        result = float(subprocess.check_output(command, shell=True).decode('ascii'))
        print ("answer")
        print (answer)
        print ("result")
        print (result)
        assert abs(result-answer)<0.0001, "The dot product result is not close enough to answers/dot_product_{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./dotProduct returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_dotProduct( prefix=None, verbose=False ):

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
        print ("Couldn't compile dotProduct.")
        return score

    if test_dotProduct(0,prefix,verbose):
        score += 3
        if test_dotProduct(1,prefix,verbose):
            score += 3
            if test_dotProduct(2,prefix,verbose):
                score += 3
                if test_dotProduct(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 65535, prefix )
                        allpass &= test_dotProduct(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on dotProduct: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_dotProduct(verbose=True)
    exit()
