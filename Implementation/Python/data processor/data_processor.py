"""
Data Processor :  Convert the list of student preferences to binary data
"""

import pandas as pd
import numpy as np
import json


def make_project_aliases(project):
    N, M = project.shape
    next_val = 1
    project_to_alias = {0:0}
    alias_to_project = {0:0}
    for i in range(N):
        for j in range(M):
            if project[i,j] not in project_to_alias:
                project_to_alias[project[i,j]] = next_val
                alias_to_project[next_val] = project[i,j]
                project[i,j] = next_val
                next_val+=1
            else:
                project[i,j] = project_to_alias[project[i,j]]
    return project_to_alias, alias_to_project

def generate_output(n, m, students_by_preferences):
    students_by_projects = np.zeros((n,m))
    # so we iterate over arr1 and write into arr2[row,arr1]
    # value of col + 1
    N, M = students_by_preferences.shape
    for i in range(N):
        for j in range(M):
            if students_by_preferences[i,j] != 0:
                students_by_projects[i,students_by_preferences[i,j]] = j + 1

    return students_by_projects[:,1:].astype(int)


if __name__ == "__main__":
    df1 = pd.read_excel("./EEE_student_preferences.xls")
    df2 = pd.read_excel("./Partial_example_ desired_output.xls")

    students_by_preferences = df1.values
    students_by_preferences = students_by_preferences[:,1:]

    p_2_a, a_2_p = make_project_aliases(students_by_preferences)

    print("students_by_preferences: %s \n" % students_by_preferences)

    with open('project_alias_to_actual_name.json', 'w') as fp:
        json.dump(a_2_p, fp, sort_keys=True, indent=4)

    # no_students = students_by_preferences.shape[0]
    # no_projects = len(p_2_a)
    #
    # students_by_projects = generate_output(no_students,no_projects,students_by_preferences)
    #
    # np.savetxt("./Result.csv",students_by_projects, delimiter =" ",fmt='%10.0f')
    # print("students_by_projects: %s \n" % students_by_projects)
