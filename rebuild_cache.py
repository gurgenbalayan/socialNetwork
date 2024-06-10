import pickle

from db.db import get_posts
from db.redis_tools import RedisTools

for i in RedisTools.get_keys():
    if "feedCache" in i:
        lst = i.split("_")
        data = get_posts(lst[1], lst[2])
        RedisTools.delete_value(i)
        RedisTools.cache_data(i, bytes(pickle.dumps(data)))
