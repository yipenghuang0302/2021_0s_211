#!/usr/bin/python3

import os
import random
import subprocess

class BinarySearchTreeNode:

    def __init__(self):
        self.l = None
        self.data = None
        self.r = None

    def insert(self, val):
        if self.data == None:
            self.data = val
        if val < self.data:
            if not self.l:
                self.l = BinarySearchTreeNode()
            self.l.insert(val)
        elif val == self.data:
            pass
        else:
            if not self.r:
                self.r = BinarySearchTreeNode()
            self.r.insert(val)

    def reverse_order_traversal(self):
        string = self.r.reverse_order_traversal() if self.r else ""
        string += str(self.data)
        string += " "
        string += self.l.reverse_order_traversal() if self.l else ""
        return string

def generate_test ( filenum, length, prefix=None ):

    root = BinarySearchTreeNode()

    with open("{}tests/test{}.txt".format(prefix if prefix else "",filenum), "w") as infile:
        for _ in range (length):
            val = random.randrange(length)
            root.insert(val)
            infile.write("{} ".format(val))

    with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "w") as outfile:
        outfile.write(root.reverse_order_traversal())

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 4 )
    generate_test ( 1, 8 )
    generate_test ( 2, 16 )
    generate_test ( 3, 32 )

def test_bstReverseOrder ( filenum, prefix=None, verbose=False ):

    command = prefix if prefix else "."
    command += "/bstReverseOrder {}tests/test{}.txt".format(prefix if prefix else "",filenum)
    if verbose:
        print (command)

    try:
        with open("{}answers/answer{}.txt".format(prefix if prefix else "",filenum), "r") as outfile:
            answer = [ int(num) for num in outfile.read().split() ]
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        resultlist = [int(string) for string in result.split()]
        # print ("answer")
        # print (answer)
        # print ("result")
        # print (result)
        assert resultlist == answer, "The breadth first traversal of the bst doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./bstReverseOrder returned non-zero exit status.")
    except AssertionError as e:
        print (result)
        print (e.args[0])

    return False

def grade_bstReverseOrder( prefix=None, verbose=False ):

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
        print ("Couldn't compile bstReverseOrder.")
        return score

    if test_bstReverseOrder(0,prefix,verbose):
        score += 3
        if test_bstReverseOrder(1,prefix,verbose):
            score += 3
            if test_bstReverseOrder(2,prefix,verbose):
                score += 3
                if test_bstReverseOrder(3,prefix,verbose):
                    score += 3

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 1024, prefix )
                        allpass &= test_bstReverseOrder(filenum,prefix,verbose)
                    if allpass:
                        score += 5

    print ("Score on bstReverseOrder: {} out of 22.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_bstReverseOrder(verbose=True)
    exit()
