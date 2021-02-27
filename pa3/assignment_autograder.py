#!/usr/bin/python3

from toHex import autograder as toHex_autograder
from binSub import autograder as binSub_autograder
from binToFloat import autograder as binToFloat_autograder
from doubleToBin import autograder as doubleToBin_autograder
from floatMul import autograder as floatMul_autograder

total = 0

total += toHex_autograder.grade_toHex ( path="toHex/", verbose=False )
total += binSub_autograder.grade_binSub ( path="binSub/", verbose=False )
total += binToFloat_autograder.grade_binToFloat ( path="binToFloat/", verbose=False )
total += doubleToBin_autograder.grade_doubleToBin ( path="doubleToBin/", verbose=False )
total += floatMul_autograder.grade_floatMul ( path="floatMul/", verbose=False )

print ("Score on assignment: {} out of 120.".format(total))
