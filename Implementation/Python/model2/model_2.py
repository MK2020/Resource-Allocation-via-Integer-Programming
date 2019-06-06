
"""
Model 2 : Allocate projects to students based on their preference rankings
Author: Mwanakombo Hussein
"""

# Import PuLP modeler functions
from pulp import *
import numpy as np
import xlrd
import re
import string
import csv
import xlsxwriter

#Retrieving data from excel
book = xlrd.open_workbook('model2/M2_TestingData.xls')
#Simple, Complex, Realistic
sheet = book.sheet_by_name('Complex')
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
C = np.array(data)
np.set_printoptions(threshold=np.inf)
#Printing preference sheet
#print(C)

#Data asssumes : 15 students, 5 choices, 70 project preferences
number_of_students, number_of_projects = C.shape
print("Students: ", number_of_students, "Projects:", number_of_projects)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("SPA Model_2", LpMinimize)

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
#1 Each student can only be allocated a project that is part of their preferences subset
for student, project in x:
    prob += x[student, project] <= float(C[student, project]) #, "Preference_Constraint"

#2 Each student should be allocated to only 1 project
for student in range(number_of_students):
     prob += sum(x[(student, project)] for project in range(number_of_projects)) == 1 #, "Student_Constraint"

#3 (redundant) Each project should be allocated to at most 1 student
for project in range(number_of_projects):
    prob += sum(x[(student, project)] for student in range(number_of_students)) <= 1 #, "Project_Constraint"

# The problem data is written to an .lp file
prob.writeLP("SPA Model_2.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve() #or prob.solve(CPLEX()) etc

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
allocation = np.zeros((number_of_students,number_of_projects))
for v in prob.variables():
    #filtered is (0,_0) to 0,_0
    filtered = re.search('x_\((.+?)\)', v.name).group(1)
    #find the comma's index which is 1
    comma_idx = filtered.find(',_')
    #find the underscore's index (not used)
    underscore_idx = comma_idx + 1
    #set coords as integers from filtered to get int (0,0) from string 0,_0
    coords = int(filtered[:comma_idx]), int(filtered[comma_idx+2:])
    #create allocation array with coords and set their respective values
    allocation[coords] = v.varValue
#print(allocation)

# The optimised objective function value is printed to the screen
print("Objective Fnc= ", value(prob.objective))

#Retrieve allocation rankings
rank = []
for student in range(number_of_students):
    for project in range(number_of_projects):
        if allocation[student, project] == 1:
            rank.append(C[student, project])

#Export allocation to xls workbook
workbook = xlsxwriter.Workbook('M2_output_alloc.xlsx')
worksheet1 = workbook.add_worksheet('Model2_alloc')
row = 0
for col, data in enumerate(allocation.T):
    worksheet1.write_column(row,col, data)
#Add worksheet of allocation ranks
worksheet2 = workbook.add_worksheet('Model2_alloc_ranks')
row = 0
col = 0
for ranks in rank:
    worksheet2.write(row, col, ranks)
    row += 1
workbook.close()
