#!./venv/bin/python3.7
from argparse import ArgumentParser
import bcrypt
import json
import psycopg2
import sys


def get_arguments_for_users_list():    
    parser = ArgumentParser()
    parser.add_argument("-l", "--list", help = "list all users", action='store_true')
    parser.add_argument("-c", "--config", dest="config", help="add path to config file", required = True)
    args = parser.parse_args()
    return args


def get_arguments_for_user_creation():
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", help="add username to account", required = True)
    parser.add_argument("-p", "--passwd", dest="passwd", help="add password to account", required = True)
    parser.add_argument("-c", "--config", dest="config", help="add path to config file", required = True)
    args = parser.parse_args()
    return args


def list_all_users():
    args = get_arguments_for_users_list()
    users = select_users_from_db(args.config)
    for user in users:
        print(user[0])


def create_user():
    args = get_arguments_for_user_creation()
    if check_if_user_in_db(args.config, args.username):
        print("User already in database. Please try again.")
        return
    hashed_passwd = hash_password(args.passwd)
    create_user_query = f"INSERT INTO users (name, passwd) VALUES ('{args.username}','{hashed_passwd.decode()}')"
    insert_to_db(args.config, create_user_query)


def check_if_user_in_db(config, username):
    users = select_users_from_db(config)
    for user in users:
        if user[0]==username:
            return True
    return False


def hash_password(passwd):
    return bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())


def get_dsn(config):
    with open(config, 'r') as f:
        config = json.load(f)
    return  f"postgres://{config['db']['user']}:foobar@{config['db']['host']}:{config['db']['port']}/{config['db']['name']}"


def insert_to_db(config, query):
    dsn = get_dsn(config)
    try:
        conn = psycopg2.connect(dsn)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        print("Success!")
    except psycopg2.DatabaseError as err:
        print("Could not perform database operation: {} ".format(err))
        sys.exit(-1) 


def select_users_from_db(config):
    query = "SELECT name FROM users"
    dsn = get_dsn(config)
    try:
        conn = psycopg2.connect(dsn)
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
        return records
    except psycopg2.DatabaseError as err:
        print("Could not perform database operation: {} ".format(err))
        sys.exit(-1) 

def main():
    if '--list' in sys.argv or '-l' in sys.argv:
        list_all_users() 
    else:
        create_user()


if __name__=="__main__":
    main()