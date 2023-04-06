
from fuzzywuzzy import fuzz,process

from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from numpy.linalg import norm
import numpy as np

def get_score(term, list_names):
    print(len(list_names))
    for term2 in list_names:
            X = term
            Y=term2
            max_score=jaro_winkler_distance(X[0],Y[0])
            # X_list = word_tokenize(X[0])
            # Y_list = word_tokenize(Y[0])
            # sw = nltk.corpus.stopwords.words('english')
            # X_Set = {w for w in X_list if not w in sw}
            # y_Set = {w for w in Y_list if not w in sw}
            #
            # l1 = []
            # l2 = []
            # rvector = X_Set.union(y_Set)
            #
            # for w in rvector:
            #     if w in rvector:
            #         if w in X_Set:
            #             l1.append(1)
            #         else:
            #             l1.append(0)
            #         if w in y_Set:
            #             l2.append(1)
            #         else:
            #             l2.append(0)
            # c =0
            #
            # for i in range(len(rvector)):
            #     c+= l1[i] * l2[i]
            #
            # max_score =np.dot(l1,l2)/((norm(l1)*norm(l2))**0.5) # 2.3 sec

            return (Y[0],max_score)


def jaro_winkler_distance(s1, s2, prefix_weight=0.1):
    # Compute Jaro distance
    jaro_sim = 0.0
    if s1 == s2:
        jaro_sim = 1.0
    else:
        # Find matching characters
        len_s1 = len(s1)
        len_s2 = len(s2)
        match_distance = max(len_s1, len_s2) // 2 - 1
        s1_matches = [False] * len_s1
        s2_matches = [False] * len_s2
        matches = 0
        for i in range(len_s1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len_s2)
            for j in range(start, end):
                if not s2_matches[j] and s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break
        if matches > 0:
            # Compute transpositions
            transpositions = 0
            j = 0
            for i in range(len_s1):
                if s1_matches[i]:
                    while not s2_matches[j]:
                        j += 1
                    if s1[i] != s2[j]:
                        transpositions += 1
                    j += 1
            transpositions //= 2
            # Compute Jaro distance
            jaro_sim = (matches / len_s1 + matches / len_s2 + (matches - transpositions) / matches) / 3

    # Compute Jaro-Winkler distance
    prefix_len = 0
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    jaro_winkler_sim = jaro_sim + prefix_weight * prefix_len * (1 - jaro_sim)
    return jaro_winkler_sim
