# Import PuLP modeler functions
from pulp import *
import numpy as np
import xlrd
import re
import string
import csv
import xlsxwriter
import pandas as pd

#Retrieving data from excel
book = xlrd.open_workbook('M5_TestingData.xls')
#Simple, Complex, Realistic
sheet = book.sheet_by_name('PID_alias')
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
P = np.array(data)
np.set_printoptions(threshold=np.inf)
#Printing preference sheet
#print(P)

book = xlrd.open_workbook('M5_TestingData.xls')
#Simple, Complex, Realistic
sheet = book.sheet_by_name('LID_alias')
data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
L = np.array(data)
np.set_printoptions(threshold=np.inf)
#Printing preference sheet
#print(L)

P_kj = np.zeros(( len(L), len(P)))
lecturer = -1
for project in range(len(P)-1):
    lecturer = lecturer + 1
    P_idx = int(P[project])
    L_idx = int(L[lecturer])
    print(L_idx, P_idx)
    P_kj[L_idx][P_idx] = 1
#print(P_kj)

#Export allocation to xls workbook
workbook = xlsxwriter.Workbook('M5_processing_output.xlsx')
worksheet1 = workbook.add_worksheet('Model5_Pkj')
row = 0
for col, data in enumerate(P_kj):
    worksheet1.write_column(row,col, data)
