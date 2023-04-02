from fuzzywuzzy import fuzz,process
def get_ratio(term, list_names, min_score=0):
    max_score = 1
    max_name = ""
    for term2 in list_names:
        score = fuzz.ratio(term, term2)
        if (score > min_score) & (score > max_score):
            max_name = term2
            max_score = score
    return (max_name, max_score)

def get_partial_ratio(term, list_names, min_score=0):
    max_score = 1
    max_name = ""
    for term2 in list_names:
        score = fuzz.partial_ratio(term, term2)
        if (score > min_score) & (score > max_score):
            max_name = term2
            max_score = score
    return (max_name, max_score)


def get_partial_sort_ratio(term, list_names, min_score=0):
    max_score = 1
    max_name = ""
    for term2 in list_names:
        score = fuzz.partial_token_sort_ratio(term, term2)
        if (score > min_score) & (score > max_score):
            max_name = term2
            max_score = score
    return (max_name, max_score)

def get_partial_set_ratio(term, list_names, min_score=0):
    max_score = 1
    max_name = ""
    for term2 in list_names:
        score = fuzz.partial_token_set_ratio(term, term2)
        if (score > min_score) & (score > max_score):
            max_name = term2
            max_score = score
    return (max_name, max_score)

