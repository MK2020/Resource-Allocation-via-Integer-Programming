
"""
Model 2 : Allocate projects to students based on their preference rankings
Author: Mwanakombo Hussein
"""
from pulp import *
import M2_functions as fnc
import numpy as np
import time
import matplotlib.pyplot as plt

#Retrieving data from excel
C = fnc.read_preferences('Input_Data/M2_InputData.xls','Realistic')

#Data asssumes : 109 students, 10 choices, 181 project preferences
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Time it takes to run M3 start point
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

#Constaints
#1 Each student should be allocated to only 1 project
for student in range(number_of_students):
     prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#2 (NOT redundant) Each project should be allocated to at most 1 student
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

#3 Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

# The problem is solved using PuLP's choice of Solver
prob.solve(GUROBI()) #or prob.solve(CPLEX()) etc

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Time it takes to run M3 end point
end = time.time()
print("Time elapsed:", end - start)

# Each of the variables is printed with it's resolved optimum value
allocation = np.zeros((number_of_students,number_of_projects))
fnc.sort_allocation(prob,allocation)

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

#Retrieve allocation rankings
rank = []
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])



plt.hist(rank, color = 'green', edgecolor = 'white', bins=np.arange(10)-0.5)
plt.xticks(range(10))
plt.title("Rankings Allocated with Model 2")
plt.xlabel('Rankings')
plt.ylabel('Number of Students')
plt.show()


# label = ['Rank1', 'Rank2', 'Rank3', 'Rank4', 'Rank5', 'Rank6', 'Rank7', 'Rank8',
#          'Rank9', 'Rank10']
#
# index = np.arange(len(label))
# plt.bar(index,(rank))
# plt.xlabel('Rankings', fontsize=5)
# plt.ylabel('No of Movies', fontsize=5)
# plt.xticks(index, label, fontsize=5, rotation=30)
# plt.title('Market Share for Each Genre 1995-2017')
# plt.show()

#Export allocation and ranks to xls workbook
fnc.write_allocation(allocation,rank)
