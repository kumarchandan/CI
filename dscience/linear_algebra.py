import math
'''
'''

'''
vectors:
vectors are objects that can be added together (to form new vectors)
                    that can be multiplied to scalers(ie numbers) to form new vectors

eg 3-dimensional vector
height, weight and age of people    height_weight_age = [70, 170, 40]

vectors add component wise
if vectors are of not same length, addition won't be allowed
'''

# vectors Arithmetic
def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v, w)]
# vector substract
def vector_sub(v, w):
    return [v - w for v, w in zip(v, w)]

# add many vectors
def vector_sum(vectors):
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result, vector)
    return result

# scalar multiply
def scalar_multiply(num, vector):
    return [num * elem for elem in vector]

# calculate mean of the vector
def vector_mean(vectors):
    len_of_vector = len(vectors)
    return scalar_multiply(1 / len_of_vector, vector_sum(vectors))


'''
Dot product:
The dot product of two vectors is the sum of their componentwise products
'''
def dot_product(vector1, vector2):
    return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

'''
vector sum of squares
'''
def sum_of_squares(vector):
    return dot_product(vector, vector)
# calculate magnitude

def magnitude(vector):
    return math.sqrt(sum_of_squares(vector))

def squared_distance(vector1, vector2):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_sub(vector1, vector2))

def distance(vector1, vector2):
    return math.sqrt(squared_distance(vector1, vector2))


'''
Matrices
a matrix is a two dimensional collection of numbers.
A = [[1, 2, 3], # A has 2 rows and 3 columns
    [4, 5, 6]]
B = [[1, 2], # B has 3 rows and 2 columns
    [3, 4],
    [5, 6]]

Uses of matrices
1)
we can use matrix to represent a data set consisting of multiple vectors, simply
considering each vector as a row of the matrix
for ex.
we can put height, weight and age of 1000 people in 1000 x 3 matrix
data = [[70, 170, 40],
    [65, 120, 26],
    [77, 250, 19],
    # ....
    ]
2)
we can also use, n x k matrix to represent a linear function that maps k-dimensional vectors to n-dimensional vectors

3) matrices can be used to represent binary relationships
this
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
(4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]
can be represented as

#           user 0 1  2  3  4  5  6  7  8  9
friendships =  [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0], # user 0
                [1, 0, 1, 1, 0, 0, 0, 0, 0, 0], # user 1
                [1, 1, 0, 1, 0, 0, 0, 0, 0, 0], # user 2
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0], # user 3
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0], # user 4
                [0, 0, 0, 0, 1, 0, 1, 1, 0, 0], # user 5
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], # user 6
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], # user 7
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1], # user 8
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]] # user 9

by convention, we write capital letters for matrix variables
'''
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

def get_row(A, i):
    return A[i]

def get_column(A, j):
    return [row[j] for row in A]

def make_matrix(num_rows, num_cols, entry_fn):
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_rows)]

def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0

identity_matrix = make_matrix(5, 5, is_diagonal)

