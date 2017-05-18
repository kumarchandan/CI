import random

'''
The universe consists of all the possible outcomes.
Any subset of these outcomes is an event. eg. 'the dice rolls 1, the dice rolls even number.
P(E) means "the probability of the event E. 

Dependence and Independence:
Two events E and F are dependent if knowing something about whether E happens gives us information
about whether F happens (and vice versa), otherwise they are independent. 

ex:
if we flip a fair coin twice, knowing whether the first flip is Heads gives us no information about
whether the second flip is Heads. These events are independent.
if the first flip is Heads and it certainly gives us information about whether both flips are Tails. (if the 
first flip is Heads, then definitely its not the case that both flips are Tails.) These two events are dependent. 

Two events E and F are independent if the probability that they both happen is the product of the probabilities
that each one happens. 

P(E, F) = P(E)P(F)
In the example above, the probability of “first flip Heads” is 1/2, and the probability of
“both flips Tails” is 1/4, but the probability of “first flip Heads and both flips Tails” is
0.

Conditional Probability:
When two events are independent,
P(E, F) = P(E)P(F)

If they are not independent (and if the prob of F is not 0), then
P(E | F) = P(E, F) / P(F)

'''


def random_kid():
    return random.choice(['boy', 'girl'])

both_girls = 0
older_girl = 0
either_girl = 0

random.seed(0)

for _ in range(10000):
    younger = random_kid()
    older = random_kid()
    if older == 'girl':
        older_girl += 1
    if older == 'girl' and younger == 'girl':
        both_girls += 1
    if older == 'girl' or younger == 'girl':
        either_girl += 1
    
print("P(both | older): ", both_girls / older_girl)
print("P(both | either): ", both_girls / either_girl)






'''
Uniform distribution
'''
def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0






