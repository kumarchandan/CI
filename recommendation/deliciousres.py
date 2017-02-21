#
from pydelicious  import get_popular, get_userposts, get_urlposts

def initializeUserDict(tag, count=5):
    user_dict = {}
    try:
        # get the top count popular posts
        for p1 in get_popular(tag=tag)[0:count]:
            # Find all users who posted this
            for p2 in get_urlposts(p1['href']):
                user = p2['user']
                user_dict[user] = {}
    #
    except Exception:
        print('function')
    return user_dict
