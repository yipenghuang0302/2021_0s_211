#!/usr/bin/python

import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, prefix=None ):

    while True:
        G = nx.gnm_random_graph(nodes, edges)
        if nx.is_connected(G): # ensure connected graph
            break

    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.random()

    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.spring_layout(G))
    # nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
    # plt.savefig("{}tests/test{}.png".format(prefix if prefix else "",filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        infile.write("{}\n".format(nodes))

        A = nx.adjacency_matrix(G).toarray()
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    mst = nx.minimum_spanning_tree(G)
    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "wb") as answerfile:
        nx.write_edgelist(mst, answerfile, data=False)

    # nx.draw(mst, with_labels=True, font_weight='bold', pos=nx.spring_layout(mst))
    # nx.draw_networkx_edge_labels(mst, pos=nx.spring_layout(mst))
    # plt.savefig("{}answers/answer{}.png".format(prefix if prefix else "",filenum))
    # plt.close()

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 2, 4 )
    generate_test ( 1, 3, 6 )
    generate_test ( 2, 8, 16 )
    generate_test ( 3, 16, 32 )

def test_mst ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/mst {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as answerfile:
            answerGraph = nx.read_edgelist(answerfile,nodetype=int)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii').strip()
        lines = result.split('\n')
        resultGraph = nx.parse_edgelist(lines,nodetype=int)

        assert answerGraph.nodes == resultGraph.nodes, "The nodes in your graph don't match the graph in answers/answer{}.txt.".format(filenum)
        assert answerGraph.edges == resultGraph.edges, "The edge list doesn't match answers/answer{}.txt.".format(filenum)

        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./mst returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_mst( prefix=None, verbose=False ):

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
        print ("Couldn't compile mst.")
        return score

    if test_mst(0,prefix,verbose):
        score += 3
        if test_mst(1,prefix,verbose):
            score += 3
            if test_mst(2,prefix,verbose):
                score += 3
                if test_mst(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 256, 512, prefix )
                        allpass &= test_mst(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on mst: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_mst(verbose=True)
    exit()
