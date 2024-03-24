import redis

from config import load_config

access_token_expire_min = 3600

class RedisTools:

    cfg_redis = load_config(section='redis')
    cfg_token = load_config(section='token')
    __redis_connect = redis.Redis(host=cfg_redis['redis_host'], port=cfg_redis['redis_port'])

    @classmethod
    def set_key(cls, key: str, value: str, is_expire: bool = True):
        cls.__redis_connect.set(key, value)
        if is_expire:
            cls.__redis_connect.expire(key, cls.cfg_token['access_token_expire_min'])

    @classmethod
    def get_value(cls, key: str) -> str:
        return cls.__redis_connect.get(key)

    @classmethod
    def delete_value(cls, key: str):
        try:
            cls.__redis_connect.delete(key)
            return True
        except redis.DataError:
            return False

    @classmethod
    def get_keys(cls) -> list[str]:
        return [value.decode('UTF-8') for value in cls.__redis_connect.keys(pattern='*')]