#!/usr/bin/python3

from basicGates import autograder as basicGates_autograder
from multiInput import autograder as multiInput_autograder

total = 0

total += basicGates_autograder.grade_basicGates ( path="basicGates/", verbose=False )
total += multiInput_autograder.grade_multiInput ( path="multiInput/", verbose=False )

print ("Score on assignment: {} out of 40.".format(total))
