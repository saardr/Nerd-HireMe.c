#!/usr/bin/env python3

from constants import confusion, diffusion
from gen_candidate import gen_candidate


def xor_lists_Z2(dest_list, src_list): # assume len(dest_row) == len(src_row)
    for i in range(len(dest_list)):
        dest_list[i] ^= src_list[i]


def xor_rows(matrix, j, i, inverse_matrix = None):
    dest_row = matrix[j]
    src_row = matrix[i]
    xor_lists_Z2(dest_row, src_row)
    if inverse_matrix is not None:
        xor_rows(inverse_matrix, j, i)


def swap_rows(matrix, i, j, inverse_matrix = None):
    matrix[j], matrix[i] = matrix[i], matrix[j]
    if inverse_matrix is not None:
        swap_rows(inverse_matrix, i, j)


def Z2_gaussian_elimination(matrix, inverse_matrix = None): # only works if det(matrix) != 0
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            for j in range(i+1, len(matrix)):
                if matrix[j][i] == 1:
                    swap_rows(matrix, i, j, inverse_matrix)
        for j in range(i+1, len(matrix[0])):
            if matrix[j][i] == 1:
                xor_rows(matrix, j, i, inverse_matrix)

    
    for i in range(1, len(matrix)+1):
        if matrix[-i][-i] == 0:
            continue
        for j in range(i+1, len(matrix)+1):
            if matrix[-j][-i] == 1:
                xor_rows(matrix, -j, -i, inverse_matrix)


def gen_diffusion_matrix():
    rows = []
    for num in diffusion:
        curr_row = [(num >> k) & 1 for k in range(32)]
        rows.append(curr_row)
    return rows


def get_zero_matrix(size=32):
    return [[0 for i in range(size)] for j in range(size)]


def gen_Id_matrix(size=32):
    Id = get_zero_matrix(size)
    for j in range(size):
        Id[j][j] = 1
    return Id


diffusion_matrix = gen_diffusion_matrix()
inverse_matrix = gen_Id_matrix()
Z2_gaussian_elimination(diffusion_matrix, inverse_matrix)
diffusion_matrix = gen_diffusion_matrix()


def mult_vectors(vec1, vec2):
    res = 0
    for i in range(len(vec1)):
        res ^= ( vec1[i] * vec2[i] )
    return res


def mult_inverse_and_vec(vec, inverse_matrix = inverse_matrix):
    resulting_vec = []
    for i in range(len(inverse_matrix)):
        row_res = mult_vectors(vec, inverse_matrix[i])
        resulting_vec.append(row_res)
    return resulting_vec


def print_matrices(*M_list):
    for M in M_list:
        for row in M:
            print(row)
        print('\n' + ('-'*100 + '\n')*2)


def get_colon(M, j):
    res = []
    for i in range(len(M)):
        res.append(M[i][j])
    return res


def mult_matrices(A, B):
    res = get_zero_matrix(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            row_A = A[i]
            col_B = get_colon(B, j)
            res[i][j] = mult_vectors(row_A, col_B)
    return res


def __debug():

    A = [[1, 1, 1, 1], [0, 1, 0, 1], [0, 1, 0, 0], [1, 0, 0, 0]]
    A_clone = [[1, 1, 1, 1], [0, 1, 0, 1], [0, 1, 0, 0], [1, 0, 0, 0]]

    inverse_A = gen_Id_matrix(4)
    Z2_gaussian_elimination(A_clone, inverse_A)

    res = mult_matrices(A, inverse_A)

    print_matrices(A, inverse_A, res)




if __name__ == '__main__':
    __debug()

        