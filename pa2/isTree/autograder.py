#!/usr/bin/python

import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, isTree, nodes, edges, prefix=None ):

    if isTree:
        G = nx.random_tree(nodes)
    else:
        G = nx.gnm_random_graph(nodes, edges)

    # nx.draw(G, with_labels=True, font_weight='bold')
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
        try:
            cycle = nx.find_cycle(G)
        except nx.NetworkXNoCycle:
            cycle = None
        outfile.write("no" if cycle else "yes")

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, True, 2, 2 )
    generate_test ( 1, True, 4, 16 )
    generate_test ( 2, True, 8, 32 )
    generate_test ( 3, False, 2, 2 )
    generate_test ( 4, False, 4, 16 )
    generate_test ( 5, False, 8, 32 )

def test_isTree ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/isTree {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answer = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii').strip()
        # print ("answer")
        # print (answer)
        # print ("result")
        # print (result)
        assert answer == result, "Your answer doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./isTree returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_isTree( prefix=None, verbose=False ):

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
        print ("Couldn't compile isTree.")
        return score

    if test_isTree(0,prefix,verbose):
        score += 2
        if test_isTree(1,prefix,verbose):
            score += 2
            if test_isTree(2,prefix,verbose):
                score += 2
                if test_isTree(3,prefix,verbose):
                    score += 2
                    if test_isTree(4,prefix,verbose):
                        score += 2
                        if test_isTree(5,prefix,verbose):
                            score += 2

                            allpass = True
                            for filenum in range(6,20):
                                isTree = bool(random.getrandbits(1))
                                generate_test ( filenum, isTree, 16, 256, prefix )
                                allpass &= test_isTree(filenum,prefix,verbose)
                            if allpass:
                                score += 5

    print ("Score on isTree: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_isTree(verbose=True)
    exit()
