#!/usr/bin/python3

from goldbach import autograder as goldbach_autograder
from maximum import autograder as maximum_autograder
from matMul import autograder as matMul_autograder
from balanced import autograder as balanced_autograder
from bstReverseOrder import autograder as bstReverseOrder_autograder

total = 0

total += goldbach_autograder.grade_goldbach ( prefix="goldbach/", verbose=False )
total += maximum_autograder.grade_maximum ( prefix="maximum/", verbose=False )
total += matMul_autograder.grade_matMul ( prefix="matMul/", verbose=False )
total += balanced_autograder.grade_balanced ( prefix="balanced/", verbose=False )
total += bstReverseOrder_autograder.grade_bstReverseOrder ( prefix="bstReverseOrder/", verbose=False )

print ("Score on assignment: {} out of 110.".format(total))
print ("The remaining 10 points will be assigned as part of recitation discussion.")
