import psycopg2
from config import load_config
from create_friends import get_limit_friends

with open('posts.txt', 'r') as f:
    config = load_config()
    posts = f.readlines()
    friends = get_limit_friends()
    count_posts=1
    count = 0
    while count !=10:
        for friend in friends:
            for post_line in range(count_posts,10050):
                count_posts += 1
                sql_line = "INSERT INTO posts (author_id, posts, date) VALUES ('{}','{}', NOW())".format(friend, posts[post_line])
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sql_line)
                if post_line%16==0:
                    break
        count+=1
f.close()


