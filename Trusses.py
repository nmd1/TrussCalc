#Imports
import numpy as np
import math as m
import scipy as sc
import numpy.linalg as lin

a = np.matrix('1 2; 3, 4')



#=================================
#this function here takes the C matrix and determines if it how many members ther are per joint
#and it determines if the truss is valid or not
#                                             ===============================================

def check(matrix):
    test = True
    for column in matrix.T:
        sumC = 0
        for element in column:
            sumC = sumC + element
        test = test and (sumC == 2)

    i = 0
    info = []
    for row in matrix:
        sum = 0
        for element in row:
            sum = sum + element
        i = i + 1
        info.append((sum, i))

    for pairs in info:
        if(pairs[0] != 1):
            print "there are %d members on joint %d" % (pairs[0], pairs[1])
        else:
            print "there is %d member on joint %d" % (pairs[0], pairs[1])


    if (sumC == 2):
        return "This is a valid truss"
    else:
        return "This Truss in invalid"

#=================This function finds the distance between two points==================
def distance(x1, x2, y1, y2):
    r = m.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
    return r

#================These functions get the values from the input file=====================
from ast import literal_eval as make_tuple

def letterToNumber(letter):
    p = [ord(char) - 65 for char in letter.upper()]
    return p[0]

def numberToLetter(numb):
    if(numb > 25 or numb < 0):
        return ''
    else:
        return chr(numb + 65)

def getJoints(data):
    set = False
    for element in data:
        if(set):
            return int(element)
        if(element == "JointNumber"):
            set = True;

def getLoadValue(data):
    set = False
    for element in data:
        if (set):
            return int(element)
        if (element == "LoadV"):
            set = True;

def getLoadPosition(data):

    set = False
    coord = ()
    for element in data:
        if (set):
            coord = make_tuple(element)
            break
        if (element == "LoadP"):
            set = True;


    search = getPositions(data)

    i = 0
    for pos in search:
        if (pos == coord):
            return i
        else:
            i = i + 1

def getPinValue(data):
    set = False
    coord = ()
    for element in data:
        if (set):
            coord = make_tuple(element)
            break
        if (element == "Sy"):
            set = True;
    search = getPositions(data)

    i = 0
    for pos in search:
        if (pos == coord):
            return i
        else:
            i = i + 1

def getPositions(data):
    set = False
    list = []
    for element in data:
        if (element == "end" and set):
            break
        if (set):
            list.append(make_tuple(element))
        if (element == "Positions" and not set):
            set = True;
    return list

def getMembers(data):
    change = False
    members = []
    #first go througth the imputted list of letters
    for element in data:
        if (element == "end" and change):
            break
        if (change):
            members.append(element)
        if (element == "CMatrix" and not change):
            change = True
    #then go in and remove duplicates, while
    memberTouples = []
    for letters in members:
        values = list(letters)  #turn the string into a list
        values = sorted(values) #sort that list
        memberTouples.append(values)    #remove duplicates
    #print memberTouples
    #print list(set(memberTouples))
    #list(set(memberTouples))                        #NOT CONFIDENT IN THIS: It should be set equal to beams
    beams = memberTouples

    #now create a matrix based off of these values
    Joints = getJoints(data)
    Members = (2 * Joints) - 3
    C = np.zeros((Joints, Members))

    col = 0
    for j in beams:
        a = letterToNumber(j[0])
        b = letterToNumber(j[1])
        C[a, col] = 1
        C[b, col] = 1
        col = col + 1
    return C
#==============================++these functions have to do with the post calculations++==============================

def idsToNames(idList):
    returnList = []
    for pair in idList:
        a = pair[0]
        b = pair[1]
        a = numberToLetter(a)
        b = numberToLetter(b)
        returnList.append(a + b)
    return returnList


#https://docs.google.com/document/d/1lb1cN4jgkR9VC8xRc7WfZIG10J5rpVw3pawuWf924wk/edit
#=============================MANUAL INPUT==========================================
#
# Joints = 11
# Members = (2 * Joints) - 3
# LoD = 4.91                                  #load on the Truss
#
#
# C = np.zeros((Joints,Members))
# # C[0,0] = 1
# # C[0,1] = 0
# # C[0,2] = 1
# # C[1,0] = 1
# # C[1,1] = 1
# # C[1,2] = 0
# # C[2,0] = 0
# # C[2,1] = 1
# # C[2,2] = 1
#                                             #input elements into C matrix
# col = 0
# for columns in C.T:
#     row = 0
#     for rows in columns:
#         id = "(" + str(row) + "," + str(col) + "):"
#         n = raw_input(id)
#         C[row, col] = n
#         row = row + 1
#     col = col + 1
#
# print(check(C))
#
# Sx = np.zeros((Joints,3))                   #Matrix of X Support Forces
# Sy = np.zeros((Joints,3))                   #Matrix of Y Support Forces
#
# #pinx, piny, rollery                        #A single pin and roller at joint 1
# Sx[0,0] = 1
# Sy[0,1] = 1
# Sy[6,2] = 1
# Joint number
#
#
#
# X = [0] * Joints                            #X position of Joints Vector
# Y = [0] * Joints                            #Y position of Joints Vector
#
#                                             #adding in position coordinates
#
# JointCoord = [(0,0),(6,8),(18,8),(28,8),(38,8),(50,8),(56,0),(44,0),(32,0),(24,0),(12,0)]
# i = 0
# for pos in JointCoord:
#     X[i] = pos[0]
#     Y[i] = pos[1]
#     i = i + 1
#
#
#                                             #adding x and y loads to truss
# Lx = np.zeros((Joints, 1))
# Ly = np.zeros((Joints, 1))
# Ly[9,0] = LoD                                #CHANGE THIS
# L = np.append(Lx, Ly, axis = 0)


inputFile = "ArchTruss"
f = open(inputFile + ".txt")
data = f.readlines()

i = 0
for items in data:
    data[i] = items.strip()
    i = i + 1

data = filter(None, data)
f.close()
#==========================++++++++++Data Parsing+++++++++++=========================================

Joints = getJoints(data)        #number of joints
Members = (2 * Joints) - 3      #number of members
LoD = getLoadValue(data)        #load value
C = getMembers(data)            #get members matrix
Sx = np.zeros((Joints,3))       #x support
Sy = np.zeros((Joints,3))
Sx[0,0] = 1
Sy[0,1] = 1
pinJ = getPinValue(data)
Sy[pinJ,2] = 1
X = [0] * Joints
Y = [0] * Joints
JointCoord = getPositions(data)
i = 0
for pos in JointCoord:
    X[i] = pos[0]
    Y[i] = pos[1]
    i = i + 1
Lx = np.zeros((Joints, 1))
Ly = np.zeros((Joints, 1))
loadp = getLoadPosition(data)
Ly[loadp,0] = LoD
L = np.append(Lx, Ly, axis = 0)

                                            #X Components
ids = []    #these will contain the member joint pairs
Ax = C.copy()
col = 0
row = 0
rownumb1 = 0
rownumb2 = 0

for columns in Ax.T:
    fir = True
    for element in columns:
        if (element == 1 and fir):
            rownumb1 = row
            fir = False
        elif(element == 1 and not fir):
            rownumb2 = row
            ids.append((rownumb1, rownumb2))

            r  = distance(X[rownumb2], X[rownumb1], Y[rownumb2], Y[rownumb1])
            if(r == 0):
                print("A DIVIDE BY ZERO EXCPETION OCCURED")
                r = 1

            Ax[rownumb1, col] = (X[rownumb2] - X[rownumb1])/r
            Ax[rownumb2, col] = (X[rownumb1] - X[rownumb2])/r
            break
        row = row + 1
    row = 0
    rownumb1 = 0
    rownumb2 = 0
    col = col + 1
                                             #Y Components
Ay = C.copy()

col = 0
row = 0
rownumb1 = 0
rownumb2 = 0
for columns in Ay.T:
    fir = True
    for element in columns:
        if (element == 1 and fir):
            rownumb1 = row
            fir = False
        elif(element == 1 and not fir):
            rownumb2 = row


            r  = distance(X[rownumb2], X[rownumb1], Y[rownumb2], Y[rownumb1])
            if(r == 0):
                print("A DIVIDE BY ZERO EXCPETION OCCURED")
                r = 1

            Ay[rownumb1, col] = (Y[rownumb2] - Y[rownumb1])/r
            Ay[rownumb2, col] = (Y[rownumb1] - Y[rownumb2])/r
            break
        row = row + 1
    row = 0
    rownumb1 = 0
    rownumb2 = 0
    col = col + 1


ASx = np.append(Ax, Sx, axis = 1)
ASy = np.append(Ay, Sy, axis = 1)

A = np.append(ASx, ASy, axis = 0)
print(A)

if(lin.det(A) == 0):
    "Cannot solve, Determinemt is Zero"
else:
    invA = lin.inv(A)
    T = invA.dot(L)
    print(T)

j = 0
for values in ids:
    j = j + 1

Output = []
members = idsToNames(ids)
i = 0
k = 0
for values in T:
    if(i < j):
        if (T[i] < 0):
            s = "Member " + str(i + 1) + ": " + str(members[i]) + " --> " + str(round(T[i][0], 2)) + " compression"
            print(s)
            Output.append(s)
        else:
            s = "Member " + str(i + 1) + ": " + str(members[i]) + " --> " + str(round(T[i][0], 2)) + " tension"
            print(s)
            Output.append(s)
    else:
        if(k == 0):
            s = "Sx1 --> " + str(round(T[i],2))
            print(s)
            Output.append(s)
            k = k + 1
        elif(k == 1):
            s = "Sy1 --> " + str(round(T[i], 2))
            print(s)
            Output.append(s)
            k = k + 1
        elif(k == 2):
            s = "Sy2 --> " + str(round(T[i], 2))
            print(s)
            Output.append(s)
    i = i + 1
#====================================== FORCE ANALYSIS ===============================================#

c = 1277.78

Failures = []
Uncertainties = []
Output.append("")
i = 0
for cords in ids:
    first = cords[0]
    second = cords[1]
    L = distance(X[second], X[first], Y[second],  Y[first])
    s = "Length of Member " + str(i + 1) + ": " + str(members[i]) + " is " + str(round(L,3))  #length calculations
    Output.append(s)
    Fl = c / (L * L)

    Fail = T[i][0] / Fl
    U = 643.7125 / (L * L * L)
    if(Fail > 0):
        Fail = 0
        U = 0
    Failures.append(Fail)
    Uncertainties.append(U)
    i = i + 1

print("Fails")
print(Failures)
print("Uncertainties")
print(Uncertainties)


value = 0
i = 0
index = 0
for fails in Failures:
    if (abs(fails) > abs(value)):
        value = fails
        index = i
    i = i + 1

Output.append("")
s = "Member " + str(i + 1) + ": " + str(members[index]) + " is the first to fail (1N fail force: " + str(round(-value,2)) + " +/- " + str(round(Uncertainties[index],3)) + ")"
print(s)
Output.append(s)

maxLoadRatio = -value
Load = LoD
maxForce = Load * maxLoadRatio
maxU = Load * Uncertainties[index]
s = "Given an applied load of " + str(LoD) + "N, the force Member " + str(index) + " (" + str(members[index]) + ") would experience before bending is " + str(round(maxForce,2))  + " +/- " + str(round(maxU,2))
print(s)
Output.append(s)


#=====================Total Cost=======================#
Output.append("")
Total = 0
for cords in ids:
    first = cords[0]
    second = cords[1]
    L = distance(X[second], X[first], Y[second], Y[first])
    print L
    Total = Total + L

Cost = (Joints * 10) + (Total)
s = "The total cost of this structure is $" + str(round(Cost,2))
print(s)
Output.append(s)

s = "Dollar per Newton = " + str(round(Cost/LoD,3))
print(s)
Output.append(s)

#==============outputFile============================="
outputFile = inputFile + "out.txt"
f = open(outputFile,'w')
for data in Output:
    f.write(data + '\n')
f.close()

print("DONE")