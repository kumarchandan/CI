# visualize data

from matplotlib import pyplot as plotdata
from collections import Counter

'''
Line chart
'''
# years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
# gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

# # create a line chart, years on x-axis, gdb on y-axis
# plotdata.plot(years, gdp, color='green', marker='o', linestyle='solid')
# plotdata.title('Nominal GDP')
# plotdata.ylabel('Billions of $')
# plotdata.show()

'''
Bar chart
'''
# # list of movies
# movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
# # number of oscars won by each movie
# num_oscars = [5, 11, 3, 8, 10]

# x_axis = [i for i, _ in enumerate(movies)]

'''
enumerate does this:
>>> [i for i in enumerate(movies)]
[(0, 'Annie Hall'), (1, 'Ben-Hur'), (2, 'Casablanca'), (3, 'Gandhi'), (4, 'West Side Story')]

>>> [i for i, _ in enumerate(movies)]
[0, 1, 2, 3, 4]
'''
# plotdata.bar(x_axis, num_oscars)
# plotdata.xticks([i for _, i in enumerate(movies)], movies)
# plotdata.show()

'''
Histograms
a bar chart can also be a good choice for plotting histograms
'''
# grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]
# decile = lambda grade: grade // 10 * 10

# histogram = Counter(decile(grade) for grade in grades)

# plotdata.bar([x for x in histogram.keys()], histogram.values())
# plotdata.show()

'''
Scatterplot
scatterplot is good for visualizing the relationship between two paired sets of data
'''

friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ['Adam', 'Bella', 'Chris', 'Debby', 'Emma', 'Finley', 'Gowker', 'Hitler', 'Iriane']

plotdata.scatter(friends, minutes)

# label each point
for label, friend_count, minute_count in zip(labels, friends, minutes):
    plotdata.annotate(label, xy=(friend_count, minute_count), xytext=(5, -5))


plotdata.show()