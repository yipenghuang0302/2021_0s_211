#!/usr/bin/python

import os
import random
import networkx as nx
from networkx.algorithms import approximation as approx
import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, isCyclic, nodes, edges, prefix=None ):

    while True:
        if isCyclic:
            G = nx.gnm_random_graph(nodes, edges)
        else:
            G = nx.random_tree(nodes)
        if nx.is_connected(G): # ensure connected graph
            break

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

    with open("{}queries/query{}.txt".format(prefix if prefix else "",filenum), "w") as qfile:

        source = random.randrange(nodes)
        qfile.write("{}\n".format(source))

        target = source
        while target == source:
            target = random.randrange(nodes) # make sure source and target are different nodes
        qfile.write("{}\n".format(target))

    with open("{}edgelists/edgelist{}.txt".format(prefix if prefix else "",filenum), "wb") as efile:
        nx.write_edgelist(G, efile, data=False)

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("queries"):
        os.mkdir("queries")
    if not os.path.exists("edgelists"):
        os.mkdir("edgelists")

    generate_test ( 0, False, 2, 2 ) # acyclic
    generate_test ( 1, False, 4, 16 ) # acyclic
    generate_test ( 2, False, 16, 256 ) # acyclic
    generate_test ( 3, True, 2, 2 ) # cyclic
    generate_test ( 4, True, 4, 16 ) # cyclic
    generate_test ( 5, True, 16, 256 ) # cyclic

def test_solveMaze ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/solveMaze {}tests/test{}.txt {}queries/query{}.txt".format(prefix if prefix else "",filenum,prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}queries/query{}.txt".format(prefix if prefix else "",filenum), "r") as qfile:
            source = int(qfile.readline())
            target = int(qfile.readline())
        with open("{}edgelists/edgelist{}.txt".format(prefix if prefix else "",filenum), "r") as edgelistfile:
            mazeGraph = nx.read_edgelist(edgelistfile,nodetype=int)
    except EnvironmentError: # parent of IOError, OSError
        print ("edgelists/edgelist{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii').strip()
        lines = result.split('\n')
        resultGraph = nx.parse_edgelist(lines,nodetype=int)
        for edge in resultGraph.edges:
            # print(edge)
            assert edge in mazeGraph.edges, "The edge {} is not part of the original graph.".format(edge)

        assert(approx.local_node_connectivity(resultGraph,source,target)==1), "The edges you returned do not connect the source and target nodes listed in queries/query{}.txt.".format(filenum)

        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./solveMaze returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_solveMaze( prefix=None, verbose=False ):

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
        print ("Couldn't compile solveMaze.")
        return score

    if test_solveMaze(0,prefix,verbose):
        score += 2
        if test_solveMaze(1,prefix,verbose):
            score += 2
            if test_solveMaze(2,prefix,verbose):
                score += 2
                if test_solveMaze(3,prefix,verbose):
                    score += 2
                    if test_solveMaze(4,prefix,verbose):
                        score += 2
                        if test_solveMaze(5,prefix,verbose):
                            score += 2

                            allpass = True
                            for filenum in range(6,20):
                                isCyclic = bool(random.getrandbits(1))
                                generate_test ( filenum, isCyclic, 32, 64, prefix ) # cyclic
                                allpass &= test_solveMaze(filenum,prefix,verbose)
                            if allpass:
                                score += 5

    print ("Score on solveMaze: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_solveMaze(verbose=True)
    exit()
