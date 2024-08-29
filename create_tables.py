import psycopg2
from config import load_config, load_config2

def create_table_chats():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS chats (
        user_id UUID NOT NULL,
        companion UUID NOT NULL,
        unread bigint NOT NULL,
        date TIMESTAMP NOT NULL)
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
def create_table_posts():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS posts (
            author_id UUID NOT NULL,
            posts VARCHAR(2550) NOT NULL,
            date TIMESTAMP NOT NULL)
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

def create_table_dialogs():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS dialogs (
            id bigint NOT NULL PRIMARY KEY,
            sender UUID NOT NULL,
            recipient UUID NOT NULL,
            text VARCHAR(2550) NOT NULL,
            date TIMESTAMP NOT NULL)
        """,
    )
    try:
        config = load_config2()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
def create_table_friends():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS friends (
            friend_id_first UUID NOT NULL,
            friend_id_second UUID NOT NULL,
            date TIMESTAMP NOT NULL,
            PRIMARY KEY(friend_id_first, friend_id_second))
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