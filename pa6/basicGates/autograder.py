#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def generate_test ( filenum, inCount=1, gateCount=0, outCount=1, path="./" ):

    inVars = [ "input"+str(i) for i in range(inCount) ]
    gates = ("NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR")
    tempCount = 0
    tempVars = inVars.copy()
    circuit = []
    outVars = []

    for i in range(gateCount):

        in0 = random.choice(tempVars)
        in1 = random.choice(tempVars)
        gate = random.choice(gates)
        out = "temp"+str(tempCount)
        tempCount += 1
        circuit.append({ "in0":in0, "in1":in1, "gate":gate, "out":out })
        tempVars.append(out)

    for i in range(outCount):
        in0 = random.choice(tempVars)
        in1 = random.choice(tempVars)
        gate = random.choice(gates)
        out = "output"+str(i)
        circuit.append({ "in0":in0, "in1":in1, "gate":gate, "out":out })
        outVars.append(out)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write("INPUTVAR {}".format(inCount))
        for inVar in inVars:
            infile.write(" "+inVar)
        infile.write("\n")

        infile.write("OUTPUTVAR {}".format(outCount))
        for outVar in outVars:
            infile.write(" "+outVar)
        infile.write("\n")

        for gate in circuit:
            if gate["gate"] is "NOT":
                infile.write( "NOT {} {}\n".format( gate["in0"], gate["out"] ) )
            else:
                infile.write( "{} {} {} {}\n".format( gate["gate"], gate["in0"], gate["in1"], gate["out"] ) )

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        for i in range(2**inCount):

            state = {}
            for bit, inVar in enumerate(inVars):
                state[inVar] = bool(1&i>>bit)

            for gate in circuit:
                inState0 = state[gate["in0"]]
                inState1 = state[gate["in1"]]
                if gate["gate"] is "NOT":
                    outState = not inState0
                elif gate["gate"] is "AND":
                    outState = inState0 and inState1
                elif gate["gate"] is "NAND":
                    outState = not(inState0 and inState1)
                elif gate["gate"] is "OR":
                    outState = inState0 or inState1
                elif gate["gate"] is "NOR":
                    outState = not(inState0 or inState1)
                elif gate["gate"] is "XOR":
                    outState = inState0!=inState1
                elif gate["gate"] is "XNOR":
                    outState = inState0==inState1
                else:
                    error()
                state[gate["out"]] = outState

            for inVar in inVars:
                outfile.write("{} ".format(int(state[inVar])))
            for outVar in outVars:
                outfile.write("{} ".format(int(state[outVar])))

            outfile.write("\n")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, inCount=1, gateCount=0, outCount=1, path="./" )
    generate_test ( 1, inCount=2, gateCount=1, outCount=1, path="./" )
    generate_test ( 2, inCount=2, gateCount=2, outCount=2, path="./" )
    generate_test ( 3, inCount=2, gateCount=4, outCount=2, path="./" )
    generate_test ( 4, inCount=4, gateCount=8, outCount=4, path="./" )
    generate_test ( 5, inCount=4, gateCount=16, outCount=4, path="./" )

def test_basicGates ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerSet = set()
            for line in outfile.read().split("\n"):
                row = []
                for string in line.split(" "):
                    if string is not "":
                        row.append(int(string))
                if line is not "":
                    answerSet.add(tuple(row))
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./basicGates", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultSet = set()
        for line in result.stdout.split("\n"):
            row = []
            for string in line.split(" "):
                if string is not "":
                    row.append(int(string))
            if line is not "":
                resultSet.add(tuple(row))

        if verbose:
            print (' '.join(result.args))
            # print ("answer")
            # print (answerSet)
            # print ("result")
            # print (result.stdout)
        assert resultSet == answerSet, "The circuit simulation result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./basicGates returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_basicGates( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile basicGates.")
        return score

    if test_basicGates(0,path,verbose):
        score += 5
        if test_basicGates(1,path,verbose):
            score += 5
            if test_basicGates(2,path,verbose):
                score += 5
                if test_basicGates(3,path,verbose):
                    score+= 5
                    if test_basicGates(4,path,verbose):
                        score += 5
                        if test_basicGates(5,path,verbose):
                            score += 5
                            for filenum in range(6,16):
                                generate_test ( filenum, inCount=8, gateCount=16, outCount=8, path=path )
                                if test_basicGates(filenum,path,verbose):
                                    score += 1
                                else:
                                    break

    print ("Score on basicGates: {} out of 40.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_basicGates(verbose=True)
    exit()
