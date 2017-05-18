
# 1 Finding key connectors
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

for user in users:
    user["friends"] = []

for i, j in friendships:
    users[i]['friends'].append(users[j])
    users[j]['friends'].append(users[i])

'''
    ques. whats the average number of connections?

    users = [
        "id": 0, "name": "somename", "friends": users_instance
    ]
'''

# 
def number_of_friends(user):
    return len(user['friends'])

# count number of friends
total_connections = sum(number_of_friends(user) for user in users)
average = total_connections / len(users)

print(average)

'''
    ques. most connected people?
    
    lambda : http://stackoverflow.com/questions/8966538/syntax-behind-sortedkey-lambda
'''
num_frnds_by_id_list = [(user['id'], number_of_friends(user)) for user in users]
# sort
sorted_num_frnds_by_id_list = sorted(num_frnds_by_id_list, key=lambda frnds:frnds[1], reverse=True)

# 

print(sorted_num_frnds_by_id_list)

'''
Data scientists you may know

ques. suggest friends of friends
'''

