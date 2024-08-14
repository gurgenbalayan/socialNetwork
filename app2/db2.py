import json
from datetime import datetime

import tarantool
import psycopg2
from config2 import load_config2, load_config




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
