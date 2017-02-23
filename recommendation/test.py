# sqrt(pow(critics['Toby']['Snakes on a Plane'] - critics['Mick LaSalle']['Snakes on a Plane'], 2) + pow(critics['Toby']['You, Me and Dupree'] - critics['Mick LaSalle']['You, Me and Dupree'], 2))

from recommendations import getRecommendations, getSimilarityEucScore, getSimilarityPearsonScore, getTopMatches, transformPrefs

from deliciousres import initializeUserDict

critics = {'Lisa Rose': {'Ex Machina': 2.5, 'The Dark Knight Rises': 3.5, 'Dangal': 3.0, 'Superman Returns': 3.5, 'Lagaan': 2.5, 'Jab We Met': 3.0},
'Gene Seymour': {'Ex Machina': 3.0, 'The Dark Knight Rises': 3.5, 'Dangal': 1.5, 'Superman Returns': 5.0, 'Jab We Met': 3.0, 'Lagaan': 3.5},
'Michael Phillips': {'Ex Machina': 2.5, 'The Dark Knight Rises': 3.0, 'Superman Returns': 3.5, 'Jab We Met': 4.0},
'Claudia Puig': {'The Dark Knight Rises': 3.5, 'Dangal': 3.0, 'Jab We Met': 4.5, 'Superman Returns': 4.0, 'Lagaan': 2.5},
'Mick LaSalle': {'Ex Machina': 3.0, 'The Dark Knight Rises': 4.0, 'Dangal': 2.0, 'Superman Returns': 3.0, 'Jab We Met': 3.0, 'Lagaan': 2.0},
'Jack Matthews': {'Ex Machina': 3.0, 'The Dark Knight Rises': 4.0, 'Jab We Met': 3.0, 'Superman Returns': 5.0, 'Lagaan': 3.5},
'Toby': {'The Dark Knight Rises':4.5, 'Lagaan':1.0, 'Superman Returns':4.0}}

# print(getSimilarityEucScore(critics, 'Lisa Rose', 'Gene Seymour'))
# print(getSimilarityPearsonScore(critics, 'Lisa Rose', 'Gene Seymour'))
# print(getTopMatches(critics, 'Toby', 4))
# print(getRecommendations(critics, 'Toby'))

# moviePrefs = transformPrefs(critics)
# print(getTopMatches(moviePrefs, 'The Dark Knight Rises'))

initializeUserDict('programming')
