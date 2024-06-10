import psycopg2
from config import load_config

with open('posts.txt', 'r') as f:
    config = load_config()
    posts = f.readlines()
    for post in posts:
        sql_line = "INSERT INTO posts (posts) VALUES ('{}')".format(post)
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_line)
f.close()


