import numpy as np
from numpy import float64

def calc_levenshtein_distance(str1: str, str2: str) -> int:
    if not str1:
        return len(str2)
    if not str2:
        return len(str1)

    len1 = len(str1)
    len2 = len(str2)
    levenshtein_matrix = np.zeros((len1 + 1, len2 + 1))

    for i1 in range(0, len1 + 1):
        levenshtein_matrix[i1, 0] = i1
    for i2 in range(0, len2 + 1):
        levenshtein_matrix[0, i2] = i2

    for i1 in range(1, len1 + 1):
        for i2 in range(1, len2 + 1):
            insertion = levenshtein_matrix[i1 - 1, i2] + 1
            deletion = levenshtein_matrix[i1, i2 - 1] + 1
            substitution = levenshtein_matrix[i1 - 1, i2 - 1] + (1 if str1[i1 - 1] != str2[i2 - 1] else 0)
            levenshtein_matrix[i1, i2] = min(insertion, deletion, substitution)

    return levenshtein_matrix[len1, len2]
