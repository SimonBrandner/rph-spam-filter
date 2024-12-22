from levenshtein_distance import calc_levenshtein_distance


def are_words_similar(word1: str, word2: str, min_similarity: float = 0.8) -> bool:
    """
    Determines if two words are similar based on a minimum similarity threshold using
    Levenshtein distance as a measure of similarity.
    """

    def calc_words_similarity(distance: int, max_distance: int) -> float:
        return 1 - (distance / max_distance)

    len1 = len(word1)
    len2 = len(word2)

    len_diff = abs(len1 - len2)
    min_levenshtein_distance = len_diff
    max_levenshtein_distance = max(len1, len2)

    max_similarity = calc_words_similarity(min_levenshtein_distance, max_levenshtein_distance)
    if max_similarity < min_similarity:
        return False

    word1 = word1.lower()
    word2 = word2.lower()

    levenshtein_distance = calc_levenshtein_distance(word1, word2)
    similarity = calc_words_similarity(levenshtein_distance, max_levenshtein_distance)
    return similarity >= min_similarity
