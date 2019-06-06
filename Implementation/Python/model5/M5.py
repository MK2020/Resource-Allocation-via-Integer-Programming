
"""
Model 5 : Allocate  projects  based  on  minimizing  the
number of projects each lecturer supervises
"""
from pulp import *
import M5_functions as fnc
import numpy as np
import time

#Retrieving data from excel
A = fnc.read_preferences('M5_TestingData.xls','A_ij_choice_input')
C = fnc.read_preferences('M5_TestingData.xls','C_ij_choice_input')
P = fnc.read_preferences('M5_TestingData.xls','P_kj_input')
# T_PS = 3

#Data asssumes : 109 students, 10 choices, 181 project preferences
number_of_students, number_of_projects = A.shape
number_of_lecturers, number_of_projects = P.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)
print("Lecturers: ", number_of_lecturers, "Projects:", number_of_projects)

# Time it takes to run M5 start point
start = time.time()


# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA_M5", LpMinimize)

# A dictionary called 'x' is created to contain the referenced Variables
# Var x_{i,j} has a LB of # of students, UP of # of projects and is of type 'LpBinary'
x = LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                          cat=LpBinary)
#OBJECTIVE FUNCTION
# objective_function = 0
# for student in range(number_of_students):
#     for project in range(number_of_projects):
#         if A[(student, project)] > 0:
#             objective_function += x[(student, project)] * ((A[(student, project)]))
# prob += objective_function

objective_function = 0
objective_function = T_PS
prob += objective_function

#Constaints
#1 Each student should be allocated to only 1 project
for student in range(number_of_students):
     prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#2 (redundant) Each project should be allocated to at most 1 student
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

#3 (recheck for this model) Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(A[student, project]) #, "Preference_Constraint"

#5 Each lecturer can only supervise T_PS projects/students (sensitivity on number of t_ps)
for lecturer in range(number_of_lecturers):
    prob += sum(P[lecturer, project] * sum(x[student, project]
                                          for student in range(number_of_students))
                for project in range(number_of_projects))  <= T_PS #min T_PS = 5 in this case? why? find out

# The problem is solved using PuLP's choice of Solver
prob.solve() #or prob.solve(CPLEX()) etc

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Time it takes to run M5 end point
end = time.time()
print("Time elapsed:", end - start)

# Each of the variables is printed with it's resolved optimum value
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)
# print("alloc(student, project):", allocation)

# Calculate and print number of project each lecturer is supervising
Ski = np.dot(P,allocation.T)
lect_count = np.sum(Ski,axis=1)
# print("alloc (lecturer, student):")
# print(Ski)
print("# of proj each lecturer is supervising:", lect_count) #nomo columns

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

#Retrieve allocation rankings
rank = []
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])
print("Ranks:",rank)

#Export allocation and ranks to xls workbook
fnc.write_allocation(allocation,rank, lect_count)
