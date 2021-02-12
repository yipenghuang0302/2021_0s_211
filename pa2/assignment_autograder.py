#!/usr/bin/python2

from edgelist import autograder as edgelist_autograder
from isTree import autograder as isTree_autograder
from solveMaze import autograder as solveMaze_autograder
from mst import autograder as mst_autograder
from findCycle import autograder as findCycle_autograder

total = 0

total += edgelist_autograder.grade_edgelist ( prefix="edgelist/", verbose=False )
total += isTree_autograder.grade_isTree ( prefix="isTree/", verbose=False )
total += solveMaze_autograder.grade_solveMaze ( prefix="solveMaze/", verbose=False )
total += mst_autograder.grade_mst ( prefix="mst/", verbose=False )
total += findCycle_autograder.grade_findCycle ( prefix="findCycle/", verbose=False )

print ("Score on assignment: {} out of 110.".format(total))
print ("The remaining 10 points will be assigned as part of recitation discussion.")
