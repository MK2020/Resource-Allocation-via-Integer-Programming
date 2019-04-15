"""
Model 3 :   Allocate projects to students based on their preference rankings
whilst putting a upper bound (TPS),on the number of projects each lecturer is allowed to supervise.
"""

from pulp import *
import functions as fnc
import numpy as np

#Data asssumes : 2 lecturers, 3 students, 5 choices, 10 project preferences
C = fnc.read_preferences('M3_TestingData.xls','ij_choice_input')
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

L = fnc.read_preferences('M3_TestingData.xls','kj_input')
number_of_lecturers, number_of_projects = L.shape
print("Lecturers: ", number_of_lecturers, "Projects:", number_of_projects)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA Model_3", LpMinimize)

# A dictionary called 'x' is created to contain the referenced Variables
# Var x_{i,j} has a LB of # of students, UP of # of projects and is of type 'LpBinary'
x = LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                          cat=LpBinary)
# Var p_{k,j} has a LB of # of lecturers, UP of # of projects and is of type 'LpBinary'
p = LpVariable.dicts("p", itertools.product(range(number_of_lecturers), range(number_of_projects)),
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

#3 (redundant) Each project should be allocated to at most 1 student
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

# l lecturers
# Each lecturer can only supervise 2 projects/students (sensitivity on number of t_ps)
for lecturer in range(number_of_lecturers):
    prob += sum(L[lecturer, project] * sum(x[(student, project)]
                                          for student in range(number_of_students))
                for project in range(number_of_projects))  <= 6 #min T_PS = 5 in this case? why? find out

# The problem data is written to an .lp file
# prob.writeLP("SPA Model_3.lp")

# The problem is solved using PuLP's choice of Solver
# prob.solve()
# or
prob.solve(GUROBI())

# Each of the variables is printed with it's resolved optimum value
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)
# print("Pkj is:", L)
# print("Xij is:", allocation)
Ski = np.dot(L,allocation.T)
lect_count = np.sum(Ski,axis=1)
# print("matrix mult(Pkj, Xji):",Ski)
print("# of proj each lecturer is supervising:", lect_count) #nomo columns


# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Retrieve allocation rankings
rank = []
# final_rank = fnc.rank(ranks)
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])

# Export allocation and ranks to xls workbook
fnc.write_allocation(allocation,rank)
