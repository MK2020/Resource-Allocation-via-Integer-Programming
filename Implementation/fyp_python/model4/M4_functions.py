"""
Functions : Optimization Model 4 functions
Author: Mwanakombo Hussein
"""
from pulp import *
import numpy as np
import xlrd
import re
import string
import xlsxwriter

#Retrieving data from excel
def read_preferences(workbook,sheet_name):
    #Retrieving data from excel
    book = xlrd.open_workbook(workbook)
    #Simple, Complex, Realistic
    sheet = book.sheet_by_name(sheet_name)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    C = np.array(data)
    np.set_printoptions(threshold=np.inf)
    return C

#Sorting allocation from variable instead of strings to integer order
# From lexigraphical ordering to conventional numerical ordering
# no 0 1 10 11 12 2 3 4 5 6 7 8 9 but 0 1 2 3 4 5 6 7 8 9 10 11 12
def sort_allocation(prob,unsorted_allocation):
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
        unsorted_allocation[coords] = v.varValue
    # print(unsorted_allocation)

#Export allocation and ranks to xls workbook
def write_allocation(allocation,rank, lect_count):
    workbook = xlsxwriter.Workbook('M4_output_alloc_TPS1.xlsx')
    worksheet1 = workbook.add_worksheet('Model4_alloc')
    row = 0
    for col, data in enumerate(allocation.T):
        worksheet1.write_column(row,col, data)
    #Add worksheet of allocation ranks
    worksheet2 = workbook.add_worksheet('Model4_alloc_ranks')
    row = 0
    col = 0
    for ranks in rank:
        worksheet2.write(row, col, ranks)
        row += 1
    #Add worksheet of lecturer supervision count
    worksheet3 = workbook.add_worksheet('Model4_alloc_lect_count')
    row = 0
    col = 0
    for lect_counts in lect_count:
        worksheet3.write(row, col, lect_counts)
        row += 1
    workbook.close()

# How to calculate total number of projects being supervised (by all lecturers)
# X_interim = fnc.read_preferences('M4_TestingData.xls','alloc')
# ans =0
# for lecturer in range(number_of_lecturers):
#     ans += sum(P[lecturer, project] * sum(X_interim[student, project]
#                                           for student in range(number_of_students))
#                 for project in range(number_of_projects))
# print(ans)
