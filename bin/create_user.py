#!./venv/bin/python3.7
from argparse import ArgumentParser
import bcrypt
import json
import psycopg2


def create_user():
    args = get_arguments()
    with open(args.config, 'r') as f:
        config = json.load(f)
    dsn = f"postgres://{config['db']['user']}:foobar@{config['db']['host']}:{config['db']['port']}/{config['db']['name']}"
    hashed_passwd = hash_password(args.passwd)
    try:
        conn = psycopg2.connect(dsn)
        cursor = conn.cursor()
        create_user_query = f"INSERT INTO users (name, passwd) VALUES ('{args.username}','{hashed_passwd.decode()}')"
        cursor.execute(create_user_query)
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        return
    print('Success!')


def get_arguments():    
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", help="add username to account", required = True)
    parser.add_argument("-p", "--passwd", dest="passwd", help="add password to account", required = True)
    parser.add_argument("-c", "--config", dest="config", help="add path to config file", required = True)
    args = parser.parse_args()
    return args


def hash_password(passwd):
    return bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())


def main():
    create_user()


if __name__=="__main__":
    main()