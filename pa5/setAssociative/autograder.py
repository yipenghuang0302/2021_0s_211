#!/usr/bin/python3

import re
import os
import datetime
import subprocess

def generate_matMul_trace ( filenum, dimension=2, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        trace = subprocess.run(
            ['valgrind', '--tool=lackey', '--basic-counts=no', '--trace-mem=yes', '--log-fd=1', '../matMul/matMul', str(dimension)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        with open(".marker".format(path,filenum), "r") as marker_file:
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

def answers_from_csim ( filenum, path="./" ):

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        csim = subprocess.run(
            ['../csim-ref', '-s', '4', '-E', '16', '-b', '8', '-l', '1', '-t', "{}tests/test{}.txt".format(path,filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )
        outfile.write(csim.stdout)

def generate_test_suite():

    subprocess.run( ['make', '-B', '-C', '../matMul'], cwd='./', check=True, )
    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_matMul_trace ( 4, 1 )
    generate_matMul_trace ( 5, 2 )
    generate_matMul_trace ( 6, 16 )
    generate_matMul_trace ( 7, 32 )
    for filenum in range(8):
        answers_from_csim ( filenum )


def test_setAssociative ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./setAssociative', "tests/test{}.txt".format(filenum)],
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
        assert answer == result.stdout, "The printed result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./setAssociative returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a hexadecimal number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_setAssociative( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile setAssociative.")
        return score

    for filenum in range(8):
        if test_setAssociative(filenum,path,verbose):
            score += 3
        else:
            break

    print ("Score on setAssociative: {} out of 24.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_setAssociative(verbose=True)
    exit()
