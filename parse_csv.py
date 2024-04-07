import csv
from db.db import add_user
import uuid
from config import load_config
import psycopg2
from  utils.hashing import Hasher
password=Hasher.get_password_hash("pas123")
str1 = 'INSERT INTO users (user_id, first_name, second_name, birthdate, biography, city, pass_hash) VALUES '


with open('people.v2.csv', 'r') as csv_file:
    i=0
    reader = csv.reader(csv_file)
    for row in reader:
        birthdate=row[1]
        city=row[2]
        biography="Biography"
        first_name = row[0].split()[1]
        second_name = row[0].split()[0]
        user_id = str(uuid.uuid4())
        config = load_config()
        if i==0:
            query= "('{}','{}','{}','{}','{}','{}','{}')".format(user_id,first_name,second_name,birthdate,biography,city,password)
            i+=1
        else:
            query = ",('{}','{}','{}','{}','{}','{}','{}')".format(user_id, first_name, second_name, birthdate, biography, city,
                                                    password)
            i+=1
        str1 += query
        if i % 10000 == 0:
            print(str1[0:500])
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(str1)
            str1 = 'INSERT INTO users (user_id, first_name, second_name, birthdate, biography, city, pass_hash) VALUES '
            i=0
        print(i)
        #add_user(user_id, first_name, second_name, birthdate, biography, city, Hasher.get_password_hash(password))

csv_file.close()