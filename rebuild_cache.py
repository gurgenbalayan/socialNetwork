import pickle

from create_friends import get_all_friends
from db.db import get_posts, get_friends
from db.redis_tools import RedisTools

def build_all_cache_for_all_friends():
    friends = get_all_friends()
    for friend_id in friends:
        data = get_posts(friend_id, 1000, 0)
        RedisTools.delete_value("feed_"+friend_id)
        RedisTools.cache_data("feed_"+friend_id, bytes(pickle.dumps(data)))

def rebuild_cache_for_user(user_id):
    data = get_posts(user_id, 1000, 0)
    RedisTools.delete_value("feed_"+user_id)
    RedisTools.cache_data("feed_"+user_id, bytes(pickle.dumps(data)))

def rebuild_cache_for_friends(user_id):
    friends_list = get_friends(user_id)
    for friend_id in friends_list:
        data = get_posts(friend_id, 1000, 0)
        RedisTools.delete_value("feed_"+friend_id)
        RedisTools.cache_data("feed_"+friend_id, bytes(pickle.dumps(data)))
