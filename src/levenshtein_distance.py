import numpy as np
from numpy import float64

def calc_levenshtein_distance(str1: str, str2: str) -> int:
    if not str1:
        return len(str2)
    if not str2:
        return len(str1)

    n = len(str1)
    m = len(str2)
    levenshtein_matrix = np.zeros((n + 1, m + 1))

    for i in range(0, n + 1):
        levenshtein_matrix[i, 0] = i
    for i in range(0, m + 1):
        levenshtein_matrix[0, i] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insertion = levenshtein_matrix[i - 1, j] + 1
            deletion = levenshtein_matrix[i, j - 1] + 1
            substitution = levenshtein_matrix[i - 1, j - 1] + (1 if str1[i - 1] != str2[j - 1] else 0)
            levenshtein_matrix[i, j] = min(insertion, deletion, substitution)

    return levenshtein_matrix[n, m]
