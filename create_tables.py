import psycopg2
from config import load_config

def create_table_posts():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS posts (
            posts VARCHAR(2550) NOT NULL)
        """,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
def create_table_users():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id UUID PRIMARY KEY NOT NULL ,
            first_name VARCHAR(255) NOT NULL, 
            second_name VARCHAR(255) NOT NULL,
            birthdate DATE NOT NULL,
            biography VARCHAR(255),
            city VARCHAR(255),
            pass_hash VARCHAR(255) NOT NULL )
        """,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)