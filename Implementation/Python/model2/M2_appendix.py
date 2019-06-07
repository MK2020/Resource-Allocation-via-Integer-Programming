"""
Model 2 : Allocate projects to students based on their preference rankings
Author: Mwanakombo Hussein
"""

from pulp import *
import M2_functions as fnc
import numpy as np
import time

#Retrieving data from excel : Input worksbook name, worksheet name
C = fnc.read_preferences('M2_TestingData.xls','Realistic')

#Data : 109 students, 10 choices, 181 project preferences
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Time it takes to run M2 start point
start = time.time()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA_M2", LpMinimize)

# A dictionary called 'x' is created to contain the referenced Variables
# Var x_{i,j} has a LB of # of students, UP of # of projects and is of type 'LpBinary'
x = LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                          cat=LpBinary)

#Objective Function
objective_function = 0
for student in range(number_of_students):
    for project in range(number_of_projects):
        if C[(student, project)] > 0:
            objective_function += x[(student, project)] * ((C[(student, project)]))
prob += objective_function

#Constraints
#1 Each student should be allocated to only 1 project
for student in range(number_of_students):
     prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#2 Each project should be allocated to at most 1 student
# Note: This constraint can be optimized away
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

#3 Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

# The problem is solved using PuLP's choice of solver : Gurobi
prob.solve(GUROBI())

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Time it takes to run M2 end point
end = time.time()
print("Time elapsed:", end - start)

# Each of the variables is printed with it's resolved optimum value
# using function sort_allocation to fix lexicographical string error
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

# Retrieve allocation rankings in array 'rank' for post-optimal analysis
rank = []
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])

# Export allocation and ranks to xls workbook
# using write_allocation function in M2_functions.py
fnc.write_allocation(allocation,rank)
