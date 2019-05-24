
"""
Model 4 : Allocate  projects  based  on  minimizing  the
number of projects each lecturer supervises
"""
from pulp import *
import M4_functions as fnc
import numpy as np

#Retrieving data from excel
C = fnc.read_preferences('M4_TestingData.xls','A_ij_mod_choice_simple')
A = fnc.read_preferences('M4_TestingData.xls','C_ij_choice_simple')
P = fnc.read_preferences('M4_TestingData.xls','P_kj_simple_2')

#Data asssumes : 109 students, 10 choices, 181 project preferences
number_of_students, number_of_projects = C.shape
number_of_lecturers, number_of_projects = P.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA_M4", LpMinimize)

# A dictionary called 'x' is created to contain the referenced Variables
# Var x_{i,j} has a LB of # of students, UP of # of projects and is of type 'LpBinary'
x = LpVariable.dicts("x", itertools.product(range(number_of_students), range(number_of_projects)),
                          cat=LpBinary)

# Objective Function
# objective_function = 0
# for student in range(number_of_students):
#     for project in range(number_of_projects):
#         if C[(student, project)] > 0:
#             objective_function += x[(student, project)] * ((C[(student, project)]))
# prob += objective_function

objective_function = 0
for lecturer in range(number_of_lecturers):
    for student in range(number_of_students):
        for project in range(number_of_projects):
            objective_function += x[(student, project)] * ((P[(lecturer, project)]))
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
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

#4 Each lecturer can only supervise T_PS projects/students (sensitivity on number of t_ps)
for lecturer in range(number_of_lecturers):
    prob +=  sum(P[lecturer, project] * sum(x[student, project]
                                          for student in range(number_of_students))
                for project in range(number_of_projects)) <= 1


# The problem is solved using PuLP's choice of Solver
prob.solve() #or prob.solve(CPLEX()) etc

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)
print("alloc(student, project):")
print(allocation)

# Calculate and print number of project each lecturer is supervising
Ski = np.dot(P,allocation.T)
lect_count = np.sum(Ski,axis=1)
print("alloc (lecturer, student):")
print(Ski)
print("# of proj each lecturer is supervising:", lect_count) #nomo columns

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

#Retrieve allocation rankings
rank = []
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(A[student, project])
print("Ranks:",rank)
#Export allocation and ranks to xls workbook
# fnc.write_allocation(allocation,rank)




# RANDOM CODE SNIPPETS
# X_interim = fnc.read_preferences('M4_TestingData.xls','alloc')
# ans = []
# for lecturer in range(number_of_lecturers):
#     ans = sum(P[lecturer, project] * sum(X_interim[student, project]
#                                           for student in range(number_of_students))
#                 for project in range(number_of_projects))
#     print(ans)

# X_interim = fnc.read_preferences('M4_TestingData.xls','alloc')
# ans = []
# for lecturer in range(number_of_lecturers):
#     ans.append(sum(P[lecturer, project] * sum(X_interim[student, project]
#                                           for student in range(number_of_students))
#                 for project in range(number_of_projects)))
# print(ans, max(ans), min(ans))
