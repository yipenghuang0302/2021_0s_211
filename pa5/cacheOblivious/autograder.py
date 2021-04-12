#!/usr/bin/python3

import re
import os
import datetime
import random
import numpy
import subprocess

def generate_trace (
    n=1,
    path="./",
    dut='../matTrans/matTrans',
    trace_path="tests/trace_matTrans_{}x{}.txt"
):

    with open(trace_path.format(n,n), "w") as infile:
        trace = subprocess.run(
            ['valgrind', '--tool=lackey', '--basic-counts=no', '--trace-mem=yes', '--log-fd=1',
                dut,
                '../matTrans/tests/matrix_a_{}x{}.txt'.format(n,n)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )

        with open(path+".marker", "r") as marker_file:
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
            ['../csim-ref', '-s', '2', '-E', '4', '-b', '4', '-l', '1',
            '-t', "tests/{}.txt".format(test_name)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )
        outfile.write(csim.stdout)

def generate_test_suite():

    subprocess.run( ['make', '-B', '-C', '../matTrans'], cwd='./', check=True, )
    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    for i in range(6):
        generate_trace ( 2**i )
        answers_from_csim("trace_matTrans_{}x{}".format( 2**i, 2**i ));

def test_matTrans ( n, path="./", verbose=False ):

    try:
        with open("{}../matTrans/answers/matrix_b_{}x{}.txt".format(path,n,n), "r") as outfile:
            answer = []
            for line in outfile.read().split('\n'):
                row = []
                for string in line.split(' '):
                    if string is not '':
                        row.append(int(string))
                if line is not '':
                    answer.append(row)
    except EnvironmentError: # parent of IOError, OSError
        print ("../matTrans/answers/matrix_b_{}x{}.txt missing".format(n,n))

    try:
        result = subprocess.run(
            ['./cacheOblivious', "../matTrans/tests/matrix_a_{}x{}.txt".format(n,n)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )

        resultlist = []
        for line in result.stdout.split('\n'):
            row = []
            for string in line.split(' '):
                if string is not '':
                    row.append(int(string))
            if line is not '':
                resultlist.append(row)

        if verbose:
            print ("answer")
            print (answer)
            print ("result")
            print (resultlist)
        assert resultlist == answer, "The matrix transpose result doesn't match answers/matrix_b_{}x{}.txt.".format(n,n)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./cacheOblivious returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        # print (csim.stdout)
        print (e.args[0])

    return False

def test_cacheOblivious ( n, test_name, path="./", verbose=False ):

    if not test_matTrans ( n, path=path ):
        return False

    try:
        with open("{}answers/answer_{}.txt".format(path,test_name), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer_{}.txt missing".format(test_name))

    answer_tallies = list(map(int, re.findall(r'\d+', answer)))

    try:
        generate_trace ( n=n, path=path, dut='./cacheOblivious', trace_path="cacheOblivious_trace_{}.txt".format(test_name) )
        csim = subprocess.run(
            ['../csim-ref', '-s', '2', '-E', '4', '-b', '4', '-l', '1',
            '-t', "cacheOblivious_trace_{}.txt".format(test_name)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=8).total_seconds(),
        )

        if verbose:
            print (' '.join(csim.args))
            print ("answer")
            print (answer)
            print ("result")
            print (csim.stdout)

        result_tallies = list(map(int, re.findall(r'\d+', csim.stdout)))
        assert answer_tallies[0] < result_tallies[0], "Cache hits need to be more numerous than baseline."
        assert answer_tallies[1] > result_tallies[1], "Cache misses need to be less numerous than baseline."
        assert answer_tallies[2] > result_tallies[2], "Cache evictions need to be less numerous than baseline."
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./cacheOblivious returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (csim.stdout)
        print (e.args[0])

    return False

def grade_cacheOblivious( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile cacheOblivious.")
        return score

    for i in range(3,6):
        if test_cacheOblivious(2**i,"trace_matTrans_{}x{}".format(2**i,2**i),path,verbose):
            score += 8
        else:
            break

    print ("Score on cacheOblivious: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_cacheOblivious(verbose=True)
    exit()
