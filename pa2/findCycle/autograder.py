#!/usr/bin/python

import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, prefix=None ):

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.spring_layout(G))
    # plt.savefig("{}tests/test{}.png".format(prefix if prefix else "",filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(nodes))
        A = nx.adjacency_matrix(G).toarray()
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        for cycle in nx.simple_cycles(G):
            for graphNode in cycle:
                outfile.write(str(graphNode))
                outfile.write(' ')
            outfile.write('\n')

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 2, 3 )
    generate_test ( 1, 4, 6 )
    generate_test ( 2, 8, 12 )
    generate_test ( 3, 16, 24 )
    generate_test ( 4, 32, 48 )
    generate_test ( 5, 64, 96 )

def test_findCycle ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/findCycle {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answerCycles = []
            for line in outfile.readlines():
                answerCycles.append(map(int, line.split()))
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii').strip()

        if not answerCycles:
            assert result.strip() == "DAG", 'Expected "DAG" printout indicating no cycles found.'
        else:
            resultCycle = map(int, result.split())

            resultInAnswer = False
            def rotate(l, n):
                return l[-n:] + l[:-n]
            for rot in range(len(resultCycle)):
                if rotate(resultCycle,rot) in answerCycles:
                    resultInAnswer = True

            # print ("answerCycles")
            # print (answerCycles)
            # print ("resultCycle")
            # print (resultCycle)
            assert resultInAnswer, "Your answer doesn't match answers/answer{}.txt.".format(filenum)

        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./findCycle returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_findCycle( prefix=None, verbose=False ):

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
        print ("Couldn't compile findCycle.")
        return score

    if test_findCycle(0,prefix,verbose):
        score += 2
        if test_findCycle(1,prefix,verbose):
            score += 2
            if test_findCycle(2,prefix,verbose):
                score += 2
                if test_findCycle(3,prefix,verbose):
                    score += 2
                    if test_findCycle(4,prefix,verbose):
                        score += 2
                        if test_findCycle(5,prefix,verbose):
                            score += 2

                            allpass = True
                            for filenum in range(6,12):
                                generate_test ( filenum, 256, 256, prefix )
                                allpass &= test_findCycle(filenum,prefix,verbose)
                            if allpass:
                                score += 5

    print ("Score on findCycle: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_findCycle(verbose=True)
    exit()
