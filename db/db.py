import json
from datetime import datetime

import tarantool
import psycopg2
from config import load_config, load_config2



def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)
    return d

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

def get_friends(user_id):
    config = load_config()
    friends_list=[]
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT friend_id_first FROM friends WHERE friend_id_second='{}'".format(
                        user_id))
                if cur.rowcount > 0:
                     for row in cur.fetchall():
                        friends_list.append(row[0])
                     return friends_list
    except (psycopg2.DatabaseError, Exception) as error:
        return friends_list
        print(error)
def write_post(author_id, post):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO posts (author_id, posts, date) VALUES ('{}','{}', NOW())".format(
                        author_id, post))
                return 'success'
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
def get_posts(user_id, limit, offset):
    config = load_config()
    posts_list = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "select author_id, posts, posts.date from posts left join friends on author_id=friend_id_second where friend_id_first='{}' ORDER BY posts.date DESC LIMIT {} OFFSET {}".format(
                        user_id, limit, offset))
                if cur.rowcount > 0:
                    list_of_post = cur.fetchall()
                    for post in list_of_post:
                        post_json = {'author_id': post[0], 'text': post[1], 'date_post': post[2]}
                        posts_list.append(post_json)
                return posts_list
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
def send_message_tarantool(sender, recipient, message):
    dt = str(datetime.now())
    try:
        conn = tarantool.Connection(host='127.0.0.1', port=3301)
        dialogs = conn.space('dialogs')
        one_message = {'who': sender, 'text': message, 'date_message': dt}
        response = dialogs.select((str(sender)+str(recipient)))
        if response.rowcount > 0:
            data = json.loads(response[0][1])
            data.append(one_message)
            str_list = json.dumps(data)
            dialogs.replace((str(sender) + str(recipient), str_list))
            dialogs.replace((str(recipient) + str(sender), str_list))
        else:
            list_message = []
            list_message.append(one_message)
            str_list = json.dumps(list_message)
            dialogs.insert((str(sender) + str(recipient), str_list))
            dialogs.insert((str(recipient) + str(sender), str_list))
        return "success"
    except:
        return "error"
def get_dialog_tarantool(sender, recipient):
    try:
        conn = tarantool.Connection(host='127.0.0.1', port=3301)
        dialogs = conn.space('dialogs')
        response = dialogs.select((str(sender) + str(recipient)))
        data = json.loads(response[0][1])
        return data
    except:
        return []
def send_message(sender, recipient, message):
    config = load_config2()
    sql_line = "INSERT INTO dialogs(sender,recipient,text,date) VALUES ('{}','{}','{}', NOW())".format(sender, recipient, message)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_line)
        return 'success'
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'fail'
def get_dialog(my_id, someone_id):
    config = load_config2()
    messages_list = []
    sql_line = "SELECT sender,recipient,text,date FROM dialogs WHERE (sender = '{}' and recipient = '{}') or (sender = '{}' and recipient = '{}') ORDER BY date DESC".format(my_id, someone_id, someone_id, my_id)
    try:
        with (psycopg2.connect(**config) as conn):
            with conn.cursor() as cur:
                cur.execute(sql_line)
                if cur.rowcount > 0:
                    list_of_messages = cur.fetchall()
                    for message in list_of_messages:
                        if message[0] == my_id:
                            message_json = {'who': "I'm", 'text': message[2], 'date_message': message[3]}
                        else:
                            message_json = {'who': str(message[0]), 'text': message[2], 'date_message': message[3]}
                        messages_list.append(message_json)
                return messages_list
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
