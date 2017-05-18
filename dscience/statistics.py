from collections import Counter
from linear_algebra import sum_of_squares, dot_product
from math import sqrt

'''
'''

'''
Central Tendencies:
'''

num_friends = [100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

'''
Mean
'''
def mean(list_of_int):
    return sum(list_of_int) / len(list_of_int)

print(mean(num_friends))

'''
Median
'''
def median(list_of_int):
    """finds the 'middle-most' value of list_of_int"""
    len_list_of_int = len(list_of_int)
    sorted_list_of_int = sorted(list_of_int)
    midpoint = len_list_of_int // 2

    median = 0

    if len_list_of_int % 2 == 1:
        median = list_of_int[midpoint]
    else:
        median = (sorted_list_of_int[midpoint] + sorted_list_of_int[midpoint - 1]) / 2
    return median

print(median(num_friends))

'''
Quantile:
generalization of median is quantile
'''
def quantile(list_of_int, p):
    """returns the pth-percentile value in x"""
    p_index = int(p * len(list_of_int))
    return sorted(list_of_int)[p_index]


list = [1, 2, 3, 4, 5, 6]

quantile(list, 0.10)

'''
mode
'''
def mode(list_of_int):
    counted_list = Counter(list_of_int)
    max_count = max(counted_list.values())

    return [value for value, count in counted_list.elements() if count == max_count]

'''
Dispersion
it refers to measures of how spread out our data is.
near zero: not spread out at all
largest value: more spread out
'''

def data_range(list_data):
    return max(list_data) - min(list_data)

'''
The range is zero precisely when the max and min are equal, which can only happen if
the elements of x are all the same, which means the data is as undispersed as possible.
Conversely, if the range is large, then the max is much larger than the min and the data
is more spread out.

like median, range doesn't depend upon the whole data set. A data set 
whose points are all either 0 or 100 has the same range as a data set whose values are
0, 100, and lots of 50s.

A more complex measure of dispersion is variance
'''

def de_mean(list_of_int):
    """translate x by subtracting its mean (so the result has mean 0)"""
    mean_of_list = mean(list_of_int)
    return [data - mean_of_list for data in list_of_int]

def variance(list_of_int):
    len_of_list = len(list_of_int)
    deviations = de_mean(list_of_int)
    return sum_of_squares(deviations) / (len_of_list - 1)

def standard_deviation(list_of_int):
    return sqrt(variance(list_of_int))

print(standard_deviation(num_friends))

'''
Both range and the standard_deviation has the same outlier problem.

'''

def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)


'''
Correlation:

ex. VP says more number of friends people have, they tend to spend more time on the site. verify this

log has data
daily_minutes = how many minutes per day each user spends on site

covariance:
https://www.mathsisfun.com/data/correlation.html

the paired analogue of variance.
variance measures how a single variable deviates from its mean.
whereas covariance measures how two variables vary in tandem from their means.
'''
daily_minutes = [1,68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]

def covariance(list1, list2):
    n = len(list1)
    return dot_product(de_mean(list1), de_mean(list2)) / (n - 1)

print('covariance: ', covariance(num_friends, daily_minutes))

'''
when corresponding elements of x and y are either both above their means or both below their means
a positive number enters the sum.
when one is above its mean and the other below, a negative number enters the sum. 

A "large" positive covariance means that x tends to be large when y is large and small when y is small.
A "large" negative covariance means that x tends to be small when y is large and vice versa.
a covariance close to zero means that no such relationship exists. 
'''

'''
Correlation:
It divides out the standard deviation of both variables. 
'''
def correlation(vector1, vector2):
    stdev_vector1 = standard_deviation(vector1)
    stdev_vector2 = standard_deviation(vector2)

    if stdev_vector1 > 0 and stdev_vector2 > 0:
        return covariance(vector1, vector2) / stdev_vector1 / stdev_vector2
    else:
        return 0            # if no correlation, variation is zero

print("correlation: ", correlation(num_friends, daily_minutes))     # 0.25

'''
The correlation is unitless and always lies between -1 and 1.
here 0.25 means a relatively weak positive correlation. 

The person with 100 friends (who spends only one minute per day on the site) is a
huge outlier, and correlation can be very sensitive to outliers. What happens if we
ignore him?
'''

outlier = num_friends.index(100)        # index of outlier
num_friends_good = [data for index, data in enumerate(num_friends) if index != outlier]
daily_minutes_good = [data for index, data in enumerate(daily_minutes) if index != outlier]

print("Correlation without outlier", correlation(num_friends_good, daily_minutes_good))         # 0.57



