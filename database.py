import psycopg2
from config import *

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

connection.autocommit = True


def create_table_seen_users():
    """СОЗДАНИЕ ТАБЛИЦЫ USERS (НАЙДЕННЫЕ ПОЛЬЗОВАТЕЛИ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )
    print("[INFO] Table SEEN_USERS was created.")

def create_table_favorites():
    """СОЗДАНИЕ ТАБЛИЦЫ favorites (фавориты"""
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS favorites(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )
    print("[INFO] Table currentuser was created.")



def insert_data_seen_users(first_name, last_name, vk_id, vk_link):
    """ВСТАВКА ДАННЫХ В ТАБЛИЦУ SEEN_USERS"""
    first_name = first_name.replace("'", '') 
    last_name = last_name.replace("'", '') 
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (first_name, last_name, vk_id, vk_link) 
            VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}')
            ON CONFLICT(vk_id) DO UPDATE SET
            first_name = '{first_name}', last_name = '{last_name}', vk_link = '{vk_link}';"""
        )

def insert_data_favorites(vk_id):
    """ВСТАВКА ДАННЫХ В ТАБЛИЦУ favorites"""
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO favorites SELECT * FROM seen_users WHERE vk_id = '{vk_id}' ON CONFLICT DO NOTHING;"""
        )

def select():
    """ВЫБОРКА ИЗ НЕПРОСМОТРЕННЫХ ЛЮДЕЙ"""
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id FROM seen_users;"""
        )
        listOfViewed = []
        for result in cursor:
           listOfViewed.append(result[0])
        return listOfViewed

def selectfavorites(offset):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT first_name,last_name,vk_id,vk_link FROM favorites OFFSET '{offset}';"""
        )
        lists = cursor.fetchone()
        return lists

def selectusers():
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT * FROM seen_users ORDER BY id DESC LIMIT 1;"""
        )
        return cursor.fetchone()


def drop_seen_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ SEEN_USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS seen_users CASCADE;"""
        )
        print('[INFO] Table SEEN_USERS was deleted.')

def drop_favorites():
    """УДАЛЕНИЕ ТАБЛИЦЫ favorites КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS favorites CASCADE;"""
        )
        print('[INFO] Table favorites was deleted.')

def creating_database():
    create_table_seen_users()
    create_table_favorites()

