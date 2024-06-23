import psycopg2
from config import load_config


def get_limit_friends():
    friends=[]
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM users LIMIT 10")
                if cur.rowcount > 0:
                    for row in cur.fetchall():
                        friends.append(row[0])
        return friends
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return friends
def get_all_users_with_friends():
    friends = []
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("select DISTINCT friend_id_first from friends")
                if cur.rowcount > 0:
                    for row in cur.fetchall():
                        friends.append(row[0])
        return friends
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return friends


config = load_config()
try:
    friends=get_limit_friends()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            for i in range(len(friends)-1):
                for j in range(len(friends)-1):
                    if i==j:
                        continue
                    cur.execute("INSERT INTO friends (friend_id_first, friend_id_second, date) VALUES (%s,%s,NOW())", (friends[i],friends[j]))
except (psycopg2.DatabaseError, Exception) as error:
        print(error)

