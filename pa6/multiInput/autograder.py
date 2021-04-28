#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def generate_test ( filenum, circuitInCount=1, gateInMax=4, gateCount=0, circuitOutCount=1, path="./" ):

    inVars = [ "input"+str(i) for i in range(circuitInCount) ]
    gates = ("NOT", "AND", "NAND", "OR", "NOR")
    tempCount = 0
    tempVars = inVars.copy()
    circuit = []
    outVars = []

    for i in range(gateCount):

        gate = random.choice(gates)
        if gate is "NOT":
            gateInCount = 1
        elif gate in ("AND", "NAND", "OR", "NOR"):
            gateInCount = random.randint(2,gateInMax)
        gateIn = random.choices(tempVars,k=gateInCount)
        gateOut = "temp"+str(tempCount)
        tempCount += 1
        circuit.append({ "inCount":gateInCount, "gateIn":gateIn, "gate":gate, "gateOut":gateOut })
        tempVars.append(gateOut)

    for i in range(circuitOutCount):
        gate = random.choice(gates)
        if gate is "NOT":
            gateInCount = 1
        elif gate in ("AND", "NAND", "OR", "NOR"):
            gateInCount = random.randint(2,gateInMax)
        gateIn = random.choices(tempVars,k=gateInCount)
        gateOut = "output"+str(i)
        circuit.append({ "inCount":gateInCount, "gateIn":gateIn, "gate":gate, "gateOut":gateOut })
        outVars.append(gateOut)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write("INPUTVAR {}".format(circuitInCount))
        for inVar in inVars:
            infile.write(" "+inVar)
        infile.write("\n")

        infile.write("OUTPUTVAR {}".format(circuitOutCount))
        for outVar in outVars:
            infile.write(" "+outVar)
        infile.write("\n")

        for gate in circuit:
            if gate["gate"] is "NOT":
                infile.write( "NOT {} {}\n".format( ' '.join(map(str, gate["gateIn"])), gate["gateOut"] ) )
            else:
                infile.write( "{} {} {} {}\n".format( gate["gate"], gate["inCount"], ' '.join(map(str, gate["gateIn"])), gate["gateOut"] ) )

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        for i in range(2**circuitInCount):

            state = {}
            for bit, inVar in enumerate(inVars):
                state[inVar] = bool(1&i>>bit)

            for gate in circuit:
                inStates = [ state[gateIn] for gateIn in gate["gateIn"] ]
                if gate["gate"] is "NOT":
                    outState = not inStates[0]
                elif gate["gate"] is "AND":
                    outState = True
                    for inState in inStates:
                        outState = outState and inState
                elif gate["gate"] is "NAND":
                    outState = True
                    for inState in inStates:
                        outState = outState and inState
                    outState = not outState
                elif gate["gate"] is "OR":
                    outState = False
                    for inState in inStates:
                        outState = outState or inState
                elif gate["gate"] is "NOR":
                    outState = False
                    for inState in inStates:
                        outState = outState or inState
                    outState = not outState
                else:
                    sys.exit("Invalid gate.")
                state[gate["gateOut"]] = outState

            for inVar in inVars:
                outfile.write("{} ".format(int(state[inVar])))
            for outVar in outVars:
                outfile.write("{} ".format(int(state[outVar])))

            outfile.write("\n")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, circuitInCount=1, gateInMax=2, gateCount=0, circuitOutCount=1, path="./" )
    generate_test ( 1, circuitInCount=2, gateInMax=2, gateCount=1, circuitOutCount=1, path="./" )
    generate_test ( 2, circuitInCount=2, gateInMax=3, gateCount=2, circuitOutCount=2, path="./" )
    generate_test ( 3, circuitInCount=2, gateInMax=4, gateCount=4, circuitOutCount=2, path="./" )
    generate_test ( 4, circuitInCount=4, gateInMax=5, gateCount=8, circuitOutCount=4, path="./" )
    generate_test ( 5, circuitInCount=4, gateInMax=6, gateCount=16, circuitOutCount=4, path="./" )

def test_multiInput ( filenum, path="./", verbose=False ):

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
            ["./multiInput", "tests/test{}.txt".format(filenum)],
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
        print ("Calling ./multiInput returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_multiInput( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile multiInput.")
        return score

    if test_multiInput(0,path,verbose):
        score += 5
        if test_multiInput(1,path,verbose):
            score += 5
            if test_multiInput(2,path,verbose):
                score += 5
                if test_multiInput(3,path,verbose):
                    score+= 5
                    if test_multiInput(4,path,verbose):
                        score += 5
                        if test_multiInput(5,path,verbose):
                            score += 5
                            for filenum in range(6,16):
                                generate_test ( filenum, circuitInCount=8, gateInMax=8, gateCount=16, circuitOutCount=8, path=path )
                                if test_multiInput(filenum,path,verbose):
                                    score += 1
                                else:
                                    break

    print ("Score on multiInput: {} out of 0. (extra credit)".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_multiInput(verbose=True)
    exit()
