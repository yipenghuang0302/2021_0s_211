#!/usr/bin/python3

import os
import datetime
import random
import numpy
import subprocess

def generate_test ( n, path="./" ):

    matrix_a = [ [random.randrange(8) for j in range(n)] for i in range(n) ]
    matrix_b = numpy.transpose( matrix_a )

    with open("{}tests/matrix_a_{}x{}.txt".format(path,n,n), "w") as infile:
        infile.write("{}\n".format(n))
        for i in range (n):
            for j in range (n):
                infile.write("{} ".format(matrix_a[i][j]))
            infile.write("\n")

    with open("{}answers/matrix_b_{}x{}.txt".format(path,n,n), "w") as outfile:
        for i in range (n):
            for j in range (n):
                outfile.write("{} ".format(matrix_b[i][j]))
            outfile.write("\n")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    for i in range(6):
        generate_test ( 2**i )

def test_matTrans ( n, path="./", verbose=False ):

    try:
        with open("{}answers/matrix_b_{}x{}.txt".format(path,n,n), "r") as outfile:
            answer = []
            for line in outfile.read().split('\n'):
                row = []
                for string in line.split(' '):
                    if string is not '':
                        row.append(int(string))
                if line is not '':
                    answer.append(row)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/matrix_b_{}x{}.txt missing".format(n,n))

    try:
        result = subprocess.run(
            ['./matTrans', "tests/matrix_a_{}x{}.txt".format(n,n)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultlist = []
        for line in result.stdout.split('\n'):
            row = []
            for string in line.split(' '):
                if string is not '':
                    row.append(int(string))
            if line is not '':
                resultlist.append(row)

        # print ("answer")
        # print (answer)
        # print ("resultlist")
        # print (resultlist)
        assert resultlist == answer, "The matrix multiplication result doesn't match answers/matrix_b_{}x{}.txt.".format(n)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./matTrans returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (csim.stdout)
        print (e.args[0])

    return False

def grade_matTrans( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile matTrans.")
        return score

    for i in range(6):
        if test_matTrans(2**i,path,verbose):
            score += 4
        else:
            break

    print ("Score on matTrans: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    generate_test_suite()
    grade_matTrans(verbose=True)
    exit()
