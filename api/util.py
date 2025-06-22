import numpy as np
from numpy import argsort

def normalize(lst: list):
    s = sum(lst)
    if s == 0:
        return lst
    return [round(100 * i / s, 3) for i in lst]


def bundle_to_matrix(allocation):
    return tuple_matrix_to_matrix([list(bundle.enumerate_fractions()) for bundle in allocation])


def tuple_matrix_to_matrix(matrix):
    return [[0 if tup[1]==-0.0 else tup[1] for tup in matrix[i]] for i in range(len(matrix))]


def transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

def round_allocation(allocation):
    new_allocation = []
    for item_allocation in allocation:
        if np.count_nonzero(item_allocation) <= 2:
            new_allocation.append(item_allocation)
        else:
            max_sharing_indx = argsort(item_allocation)[-2:]
            sum_indx = sum(np.array(item_allocation)[max_sharing_indx])
            new_allocation.append([0 if i not in max_sharing_indx else round(item_allocation[i] / sum_indx, 2) for i in range(len(item_allocation))])
    return new_allocation