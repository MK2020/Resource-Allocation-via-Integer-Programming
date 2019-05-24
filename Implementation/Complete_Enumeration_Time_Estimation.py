"""
Complete Enumeration Method: Getting time to iterate through N variables to
identigy minimum objective value.
"""

import numpy as np
import time
from random import seed
from random import randint
# start = time.time()
# darr = np.array([1, 3.14159, 1e100, -2.71828, 4, 6, 8, -9, 10,15])
# print(darr.min())
# end = time.time()
# print("Time elapsed:", end - start)

# Creating empty array
values = []

# N : Number of variables iterated
N=1

# Fill array with N randomly geneate numbers
for _ in range(N):
	values.append(randint(0, 10))

# Start timer seconds
start = time.time()
# Find minimum value out of N variables
find_min_value = np.array(values).min()
# Stop timer
end = time.time()
# Print time elapsed
print("Time elapsed:", end - start)


#1 - 4.029273986816406e-05 seconds
#10 - 6.914138793945312e-05 seconds
#100 - 7.224082946777344e-05 seconds
#200 - 7.891654968261719e-05 seconds
#300 - -05 seconds
#400 - -05 seconds
#500 - 0.00011110305786132812 seonds
#600 - -05 seconds
#700 - -05 seconds
#800 - -05 seconds
#900 - -05 seconds
#1000 - 0.00013589859008789062 seconds
#2000 - 0.00019097328186035156 seconds
#5000 - 0.00038313865661621094 seconds
#10,000 - 0.0007092952728271484 seconds
#20,000 - 0.0011110305786132812 seconds
#50,000 - 0.0028302669525146484 seconds
#100,000 - 0.006247043609619141 seconds
#200,000 - 0.011107921600341797 seconds
#500,000 - 0.03131103515625 seconds
#1,000,000 - 0.05703020095825195 seconds
#2,000,000 - 0.11512017250061035 seconds
#5,000,000 - 0.29766297340393066 seconds
#10,000,000 - 0.596153974533081 seconds
#20,000,000 - 1.1495680809020996 seconds
#50,000,000 - 3.2952420711517334 seconds
#100,000,000 - 6.150007963180542 seconds
#1,000,000,000 - 98.04578495025635 seconds
#5.938190x10^{227} -  days
