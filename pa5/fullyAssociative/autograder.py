#!/usr/bin/python3

import re
import os
import datetime
import subprocess

def generate_matMul_trace ( n=1 ):

    with open("tests/trace_matMul_{}x{}.txt".format(n,n), "w") as infile:
        trace = subprocess.run(
            ['valgrind', '--tool=lackey', '--basic-counts=no', '--trace-mem=yes', '--log-fd=1',
                '../matMul/matMul',
                '../matMul/tests/matrix_a_{}x{}.txt'.format(n,n),
                '../matMul/tests/matrix_b_{}x{}.txt'.format(n,n)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )

        with open(".marker", "r") as marker_file:
            start = int(marker_file.readline(),16)
            end = int(marker_file.readline(),16)

        is_relevant_region = False
        for line in trace.stdout.splitlines():
            if line[1]=='L' or line[1]=='S' or line[1]=='M':
                addr = int(re.split(' |,',line)[2],16)
                if addr==start:
                    is_relevant_region = True
                elif addr==end:
                    is_relevant_region = False
                elif is_relevant_region and addr < 0xffff_ffff:
                    infile.write(line+'\n')
                else:
                    # print(line)
                    pass
            elif not line[0]=='I':
                # print(line)
                pass

def answers_from_csim ( test_name ):

    with open("answers/answer_{}.txt".format(test_name), "w") as outfile:
        csim = subprocess.run(
            ['../csim-ref', '-s', '0', '-E', '16', '-b', '4', '-l', '0',
            '-t', "tests/{}.txt".format(test_name)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )
        outfile.write(csim.stdout)

def generate_test_suite():

    subprocess.run( ['make', '-B', '-C', '../matMul'], cwd='./', check=True, )
    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    for filenum in range(4):
        answers_from_csim("trace_{}".format(filenum))

    for i in range(6):
        generate_matMul_trace ( 2**i )
        answers_from_csim("trace_matMul_{}x{}".format( 2**i, 2**i ));

def test_fullyAssociative ( test_name, path="./", verbose=False ):

    try:
        with open("{}answers/answer_{}.txt".format(path,test_name), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer_{}.txt missing".format(test_name))

    try:
        result = subprocess.run(
            ['./fullyAssociative', "tests/{}.txt".format(test_name)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )
        if verbose:
            print (' '.join(result.args))
            print ("answer")
            print (answer)
            print ("result")
            print (result.stdout)
        assert answer == result.stdout, "The printed result doesn't match answers/answer_{}.txt.".format(test_name)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./fullyAssociative returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_fullyAssociative( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile fullyAssociative.")
        return score

    for filenum in range(4):
        if test_fullyAssociative("trace_{}".format(filenum),path,verbose):
            score += 3
        else:
            break

    for i in range(6):
        if test_fullyAssociative("trace_matMul_{}x{}".format(2**i,2**i),path,verbose):
            score += 2
        else:
            break

    print ("Score on fullyAssociative: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_fullyAssociative(verbose=True)
    exit()
