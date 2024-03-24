import psycopg2
from config import load_config

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
