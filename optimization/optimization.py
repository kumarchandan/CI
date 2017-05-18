import time
import random

# peoples
people_and_places = [('Seymour', 'BOS'), ('Franny', 'DAL'), ('Zooey', 'CAK'), ('Walt', 'MIA'), ('Buddy', 'ORD'), ('Les', 'OMA')]

# LaGuardia airport in New York
destination = 'LGA'

# load data into a dictionary with the origin and destination as the keys and a list of possible flights
flights = {}
flights_schedule = open('./optimization/schedule.txt')        # to run from visual studio
# flights_schedule = open('./schedule.txt')                       # to execute from outside (gitshell)

# read each line of the file
for line in flights_schedule:
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    # add details to the list of possible flights
    flights[(origin, dest)].append((depart, arrive, int(price)))

# utility fns:
# calculates how many minutes into the day a given time is:
def get_minutes(t):
    temp = time.strptime(t, '%H:%M')
    return temp[3] * 60 + temp[4]           # temp[3] = hours and temp[4] = minutes

# input as [1,4,3,2,7,3,6,3,2,4,5,3]    6 people, two-way flights (native to ny, from ny to native)
def print_schedule(sol_list):
    # flights, people_and_places, sol_list
    counter = 0
    for data in people_and_places:
        name = data[0]
        native = data[1]

        native_to_lga = flights[(native, destination)][sol_list[counter]]
        counter += 1
        lga_to_native = flights[(destination, native)][sol_list[counter]]
        counter += 1

        print(name, native, native_to_lga[0], native_to_lga[1], native_to_lga[2], lga_to_native[0], lga_to_native[1], lga_to_native[2])

# cost function : input sol_list = [1,4,3,2,7,3,6,3,2,4,5,3]
def schedule_cost(sol_list):
    total_price = 0
    latest_arrival = 0
    earliest_dep = 24 * 60

    counter = 0
    for data in range(0, len(sol_list), 2):
        # get the inbound and outbound flights
        lv_origin = people_and_places[counter][1]
        counter += 1
        # dep, arriv, price
        native_to_lga = flights[(lv_origin, destination)][sol_list[data]]
        lga_to_native = flights[(destination, lv_origin)][sol_list[data + 1]]

        # total price = price of all incoming flights and returning flights
        total_price += native_to_lga[2]
        total_price += lga_to_native[2]
        # track the latest arrival and earliest departure time
        if latest_arrival < get_minutes(native_to_lga[1]):
            latest_arrival = get_minutes(native_to_lga[1])
        if earliest_dep > get_minutes(lga_to_native[0]):
            earliest_dep = get_minutes(lga_to_native[0])

    # every person must wait at the airport until the latest person arrives
    # they also must arrive at the same time (earliest departure time) and wait for their flights
    total_wait = 0
    counter = 0
    for data in range(0, len(sol_list), 2):
        lv_origin = people_and_places[counter][1]
        counter += 1
        # dep, arriv, price
        native_to_lga = flights[(lv_origin, destination)][sol_list[data]]
        lga_to_native = flights[(destination, lv_origin)][sol_list[data + 1]]
        # wait in case of arriving to lga from native
        temp = latest_arrival - get_minutes(native_to_lga[1])
        total_wait += temp
        # wait in case of departing from lga to native_to_lga
        temp = get_minutes(lga_to_native[0]) - earliest_dep
        total_wait += temp
    # does this solution requires an extra day of car rental
    if latest_arrival > earliest_dep:
        total_price += 50
    return total_price + total_wait

# random optimize
def random_optimize(domain, costfn):
    best = 999999999
    best_r = None
    for i in range(1000):
        # create a random solution
        random_sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        # get the cost
        cost = costfn(random_sol)
        # compare it to the best one so far
        if cost < best:
            best = cost
            best_r = random_sol
    return random_sol

# hill climb : eg for variables
# domain: [(0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8), (0, 8)]
# anysol: [8, 3, 7, 0, 0, 5, 2, 6, 6, 5, 6, 7]
def hill_climb(domain, costfn):
    # create a random solution
    len_of_domain = len(domain)
    any_sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len_of_domain)]

    # loop until none of the neighboring schedules improve the cost
    while 1:
        # create list of neighboring solutions
        neighbors = []
        # selects each element of any_sol, increases by 1, append as a new sol to neighbors, then decreases by 1 and append to neighbors
        for j in range(len_of_domain):
            # one away in each direction
            if any_sol[j] > domain[j][0]:
                neighbors.append(any_sol[0:j] + [any_sol[j] + 1] + any_sol[j + 1: ])
            if any_sol[j] < domain[j][1]:
                neighbors.append(any_sol[0:j] + [any_sol[j] - 1] + any_sol[j + 1: ])
        
        # get cost of any_sol first
        current_cost = costfn(any_sol)
        best_cost = current_cost
        len_neighbor = len(neighbors)

        # now see what the best solution among the neighbors is
        for j in range(len_neighbor):
            neighbor_cost = costfn(neighbors[j])
            if neighbor_cost < best_cost:
                best_cost = neighbor_cost
                any_sol = neighbors[j]

        # If there's no improvement, then we've reached the top
        if best_cost == current_cost:
            break
    return any_sol

# annealing optimize
def annealing_optimize(domain, costfn, T=10000.0, cool=0.95, step=1):
    # initialize the values randomly
    vec = [float(random.randint(domain[i][0], domain[i][1])) for in range(len(domain))]
    
















# test
list_data = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
# print_schedule(list_data)
# schedule_cost(list_data)

# number of flights available = 9 inbound and 9 outbound flights for each person (8 person)
domain = [(0, 8)] * (len(people_and_places) * 2)
# best_sol = random_optimize(domain, schedule_cost)
# best_cost = schedule_cost(best_sol)
# print(best_cost)
# print_schedule(best_sol)
sol = hill_climb(domain, schedule_cost)
print(schedule_cost(sol))
print_schedule(sol)
