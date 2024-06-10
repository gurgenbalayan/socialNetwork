import psycopg2
from config import load_config

def get_user_by_fs_without_index(first_name, second_name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                str1 = "SELECT user_id, first_name, second_name, birthdate, biography, city FROM users WHERE first_name ILIKE '{}%' and second_name ILIKE '{}%' order by user_id asc".format(first_name,second_name)
                #print(str1)
                cur.execute(str1)
                if cur.rowcount > 0:
                    return cur.fetchall()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def get_user_by_fs_with_index(first_name, second_name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                str1 = "SELECT user_id, first_name, second_name, birthdate, biography, city FROM users WHERE first_name_tsvector @@ to_tsquery('russian', '{}:*') and second_name_tsvector @@ to_tsquery('russian', '{}:*') order by user_id asc".format(first_name,second_name)
                #print(str1)
                cur.execute(str1)
                if cur.rowcount > 0:
                    return cur.fetchall()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
def add_user(user_id,
             first_name,
             second_name,
             birthdate,
             biography,
             city,
             password):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (
                    user_id, 
                    first_name, 
                    second_name, 
                    birthdate, 
                    biography, 
                    city, 
                    pass_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    , (
                        user_id,
                        first_name,
                        second_name,
                        birthdate,
                        biography,
                        city,
                        password)
                )
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def get_posts(limit, offset):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM posts LIMIT {} OFFSET {}'.format(limit, offset))
                if cur.rowcount > 0:
                    final_list=[]
                    list_of_post=cur.fetchall()
                    for i in list_of_post:
                        final_list.append(i[0])
                    return final_list
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
def authenticate_user(user_id):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT pass_hash FROM users WHERE user_id = (%s)', (user_id,))
                if cur.rowcount > 0:
                    pass_hash = cur.fetchone()[0]
                    return pass_hash
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def get_user_by_id(user_id):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id,
                    first_name,
                    second_name,
                    birthdate,
                    biography,
                    city FROM users WHERE user_id = (%s)
                    """, (user_id,))
                if cur.rowcount > 0:
                    return cur.fetchone()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
