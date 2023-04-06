
from fuzzywuzzy import fuzz,process

from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from numpy.linalg import norm
import numpy as np

def get_score(term, list_names):
    for term2 in list_names:
            X = term
            Y=["Rodrigu"]
            X_list = word_tokenize(X[0])
            Y_list = word_tokenize(Y[0])
            sw = nltk.corpus.stopwords.words('english')
            X_Set = {w for w in X_list if not w in sw}
            y_Set = {w for w in Y_list if not w in sw}

            l1 = []
            l2 = []
            rvector = X_Set.union(y_Set)

            for w in rvector:
                if w in rvector:
                    if w in X_Set:
                        l1.append(1)
                    else:
                        l1.append(0)
                    if w in y_Set:
                        l2.append(1)
                    else:
                        l2.append(0)
            c =0

            for i in range(len(rvector)):
                c+= l1[i] * l2[i]

            max_score =np.dot(l1,l2)/((norm(l1)*norm(l2))**0.5) # 2.3 sec

            # max_score = np.dot(l1,l2)/(norm(l1)*norm(l2)) # 20 sec
            # max_score=c/(sum(l1)*sum(l2)**0.5) #13.30 s
            # max_score=cosine_similarity(l1,l2)
            return (Y[0],max_score)


def cosine_similarity(x, y):
    # Ensure length of x and y are the same
    if len(x) != len(y):
        return None

    # Compute the dot product between x and y
    dot_product = np.dot(x, y)

    # Compute the L2 norms (magnitudes) of x and y
    magnitude_x = np.sqrt(np.sum(x.pow(2)))
    magnitude_y = np.sqrt(np.sum(y.pow(2)))

    # Compute the cosine similarity
    cosine_similarity = dot_product / (magnitude_x * magnitude_y)

    return cosine_similarity


