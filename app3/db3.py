import json
from datetime import datetime

import tarantool
import psycopg2
from config import load_config

def rollback_unread(sender, recipient, date):
    config = load_config()
    sql_1 = "DELETE FROM chats WHERE (user_id = '{}' and companion = '{}' and unread = 0 and date = '{}')".format(sender, recipient, date)
    sql_2 = "DELETE FROM chats WHERE (user_id = '{}' and companion = '{}' and unread = 1 and date = '{}')".format(
        recipient, sender, date)
    sql_3 = "UPDATE chats SET unread = unread - 1 WHERE (user_id = '{}' and companion = '{}' and date = '{}')".format(recipient, sender, date)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_1)
                cur.execute(sql_2)
                cur.execute(sql_3)
        return 'success'
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'fail'


def add_unread(sender, recipient, date):
    config = load_config()
    sql_chats1 = "SELECT * FROM chats WHERE user_id = '{}'".format(recipient)
    sql_chats1_create = "INSERT INTO chats(user_id, companion, unread, date) VALUES ('{}','{}',{},'{}')".format(recipient, sender, 1, date)
    sql_chats1_update = "UPDATE chats SET date = '{}', unread = unread + 1 WHERE (user_id = '{}' and companion = '{}')".format(date, recipient, sender)
    sql_chats2 = "SELECT * FROM chats WHERE user_id = '{}'".format(sender)
    sql_chats2_create = "INSERT INTO chats(user_id, companion, unread, date) VALUES ('{}','{}',{},'{}')".format(sender, recipient, 0, date)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_chats1)
                if cur.rowcount == 0:
                    cur.execute(sql_chats1_create)
                else:
                    cur.execute(sql_chats1_update)
                cur.execute(sql_chats2)
                if cur.rowcount == 0:
                    cur.execute(sql_chats2_create)
        return 'success'
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'fail'
def add_read(my_id, someone_id, date):
    config = load_config()
    messages_list = []
    sql_read_chat = "UPDATE chats SET date = {}, unread = 0 WHERE (user_id = '{}' and companion = '{}')".format(date, my_id, someone_id)
    try:
        with (psycopg2.connect(**config) as conn):
            with conn.cursor() as cur:
                cur.execute(sql_read_chat)
                return 'success'
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'fail'
