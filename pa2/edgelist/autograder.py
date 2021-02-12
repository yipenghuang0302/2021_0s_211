#!/usr/bin/python

import os
import networkx as nx
import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, prefix=None ):

    G = nx.gnm_random_graph(nodes, edges)
    A = nx.adjacency_matrix(G).toarray()

    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.savefig("{}tests/test{}.png".format(prefix if prefix else "",filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(nodes))
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "wb") as outfile:
        nx.write_edgelist(G, outfile, data=False)

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 2, 2 )
    generate_test ( 1, 4, 4 )
    generate_test ( 2, 8, 16 )
    generate_test ( 3, 16, 32 )

def test_edgelist ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/edgelist {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answerGraph = nx.read_edgelist(outfile)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        lines = result.split('\n')
        resultGraph = nx.parse_edgelist(lines)
        assert answerGraph.nodes == resultGraph.nodes, "The nodes in your graph don't match the nodes in the graph in answers/answer{}.txt.".format(filenum)
        assert answerGraph.edges == resultGraph.edges, "The edge list doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./edgelist returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_edgelist( prefix=None, verbose=False ):

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
        print ("Couldn't compile edgelist.")
        return score

    if test_edgelist(0,prefix,verbose):
        score += 3
        if test_edgelist(1,prefix,verbose):
            score += 3
            if test_edgelist(2,prefix,verbose):
                score += 3
                if test_edgelist(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 256, 1024, prefix=prefix )
                        allpass &= test_edgelist(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on edgelist: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_edgelist(verbose=True)
    exit()
