
"""
Model 2 : Allocate projects to students based on their preference rankings
Author: Mwanakombo Hussein
"""

# Import PuLP modeler functions
from pulp import *
import numpy as np

#Data asssumes : 3 students, 5 choices, 10 project preferences
C = np.array([[1,2,3,0,0], [0,1,2,3,0], [0,0,1,2,3]])
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA Model_2", LpMinimize)

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
# Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

# Each student should be allocated to only 1 project
for student in range(number_of_students):
    prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#Each project should be allocated to at most 1 student
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

# The problem data is written to an .lp file
prob.writeLP("SPA Model_2.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve() #or prob.solve(CPLEX()) etc

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
#for v in prob.variables():
#    print(v.name, "=", v.varValue)

# Print in matrix form
intermediate = []
for v in prob.variables():
    intermediate.append("%.1f"%v.varValue)
result = np.reshape(intermediate,(-1,number_of_projects))
print(result)

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))
