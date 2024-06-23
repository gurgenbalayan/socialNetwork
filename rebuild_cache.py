import pickle

from create_friends import get_limit_friends
from db.db import get_posts
from db.redis_tools import RedisTools

def build_all_cache_for_all_friends():
    friends = get_limit_friends()
    for friend_id in friends:
        data = get_posts(friend_id, 1000, 0)
        RedisTools.delete_value("feed_"+friend_id)
        RedisTools.cache_data("feed_"+friend_id, bytes(pickle.dumps(data)))

def rebuild_cache_for_user(feed_user_id):
    user_id = feed_user_id.split("_")[1]
    data = get_posts(user_id, 1000, 0)
    RedisTools.delete_value(feed_user_id)
    RedisTools.cache_data(feed_user_id, bytes(pickle.dumps(data)))
