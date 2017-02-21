# Similarity score - Euclidean and Pearson

from math import sqrt

# Returns a distance based similarity score for person1 and person2
def getSimilarityEucScore(prefs, person1, person2):
    # Get the list of shared items
    shared_items = {}
    #
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1
    # if they have no ratings in common, return 0
    if len(shared_items) == 0:
        return 0

    # Add up the squares of all the differences
    sum_of_squares = sqrt(sum([pow(prefs[person1][item] - prefs[person2][item], 2) 
                          for item in prefs[person1] if item in prefs[person2]]))
    return 1 / (1 + sum_of_squares)

# Pearson correlation score
def getSimilarityPearsonScore(prefs, p1, p2):
    # get the list of mutually rated items
    mutual_items = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            mutual_items[item] = 1
    # mutual_items -> [ 'movie_name': 1]
    
    # if there are not ratings in common, return 0
    n = len(mutual_items)
    if n == 0:
        return
    
    # Add up all the preferences
    sum1 = sum([prefs[p1][item] for item in mutual_items])
    sum2 = sum([prefs[p2][item] for item in mutual_items])

    # sum up the squares
    sum1Sq = sum([pow(prefs[p1][item], 2) for item in mutual_items])
    sum2Sq = sum([pow(prefs[p2][item], 2) for item in mutual_items])

    # sum up the products
    pSum = sum([prefs[p1][item] * prefs[p2][item] for item in mutual_items])

    # calculate pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    #
    if den == 0:
        return 0
    r = num / den
    return r
    
# Ranking the critics : returns the best matches for person from the prefs dictionary
# Number of results and similarity function are optional params.
def getTopMatches(prefs, person, n=5, similarity=getSimilarityPearsonScore):
    #
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    #
    # sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Gets recommnedations for a person by using a weighted average of every other users ranking
def getRecommendations(prefs, person, similarity_score=getSimilarityPearsonScore):
    #
    totals = {}
    simSums = {}
    #
    for other in prefs:
        # don't compare to itself
        if other == person:
            continue
        sim = similarity_score(prefs, person, other)
        # ignore scores of zero or lower
        if sim <= 0:
            continue
        #
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # sum of similarity
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    # return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

# Transform
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    #
    return result
