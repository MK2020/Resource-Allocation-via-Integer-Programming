"""
Model 3 :   Allocate projects to students based on their preference rankings
whilst putting a upper bound (TPS),on the number of projects each lecturer is allowed to supervise.
"""

from pulp import *
import M3_functions as fnc
import numpy as np
import time

# Maximum number of projects each lecturer can supervise simultaneously
T_PS = 6
print("Superviser Limit:", T_PS)

#Retrieving Student Preferences data from excel : Input worksbook name, worksheet name
C = fnc.read_preferences('M3_TestingData.xls','ij_choice_input') #ij_choice_input  or ij_choice_simple
# Data : 109 students, 181 projects, 10 project preferences
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Retrieving Lecturer Project Proposals data from excel : Input worksbook name, worksheet name
L = fnc.read_preferences('M3_TestingData.xls','kj_input') #kj_input  or kj_simple
# Data : 57 lecturers, 181 projects
number_of_lecturers, number_of_projects = L.shape
print("Lecturers: ", number_of_lecturers, "Projects:", number_of_projects)

# Time it takes to run M3 start point
start = time.time()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA Model_3", LpMinimize)

# A dictionary called 'x' is created to contain the referenced Variables
# Var x_{i,j} has a LB of # of students, UP of # of projects and is of type 'LpBinary'
x = LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                          cat=LpBinary)
#OBJECTIVE FUNCTION
objective_function = 0
for student in range(number_of_students):
    for project in range(number_of_projects):
        if C[(student, project)] > 0:
            objective_function += x[(student, project)] * ((C[(student, project)]))
prob += objective_function

#CONSTRAINTS
#1 Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

#2 Each student should be allocated to only 1 project
for student in range(number_of_students):
    prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#3 Each project should be allocated to at most 1 student
# This constraint can be optimzed away
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

# l lecturers
#4 Each lecturer can only supervise T_PS projects/students (sensitivity on number of t_ps)
for lecturer in range(number_of_lecturers):
    prob += sum(L[lecturer, project] * sum(x[student, project]
                                          for student in range(number_of_students))
                for project in range(number_of_projects))  <= T_PS

# The problem data is written to an .lp file
prob.writeLP("SPA Model_3.lp")

# The problem is solved using PuLP's choice of solver : Gurobi
prob.solve(GUROBI())

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Time it takes to run M3 end point
end = time.time()
print("Time elapsed:", end - start)

# Each of the variables is printed with it's resolved optimum value
# using function sort_allocation to fix lexicographical string error
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)


# Calculate and print the number of projects each lecturer is supervising
# Multiply Pkj * Xij resulting in Ski
Ski = np.dot(L,allocation.T)
# Sum the number of projects each lecturer is supervising
# across columns i.e across projects
lect_count = np.sum(Ski,axis=1)


# Retrieve allocation rankings in array 'rank' for post-optimal analysis
rank = []
# final_rank = fnc.rank(ranks)
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])

# Change lect_count from ndarray to list
# Export allocation,ranks and number of projects each lecturer is supervising (lect_count)
# to xls workbook
fnc.write_allocation(allocation,rank,lect_count.tolist())
