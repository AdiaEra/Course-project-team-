import sqlalchemy
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2 import sql
from models import create_tables, User, Like, UsersLike
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError, IntegrityError
from pprint import pprint
import configparser

DSN = 'postgresql://postgres:voimant11@localhost:5432/users_vk_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Service:
    def __init__(self, session):
        self.session = session

    def double_user(self, users_id):
        """
        Функция проверки наличия id в таблице 'users'
        """
        res = self.session.query(User).filter(User.users_id == users_id).all()
        a = False if res == [] else True
        return a

    def insert_user(self, users_id: int):
        """
        Функция заполнения данными таблицы 'users'
        """
        if not self.double_user(users_id):
            user = User(users_id=users_id)
            session.add(user)
            session.commit()
            print('пользователь добавлен в базу')
        else:
            print('такой пользователь есть в базе')

    def double_liked(self, liked_id):
        """
        Функция проверки наличия id в таблице 'liked'
        """
        res = self.session.query(Like).filter(Like.liked_id == liked_id).all()
        a = False if res == [] else True
        return a

    def double_user_like(self, liked_id, users_id):
        """
        Функция проверки наличия id в таблице 'users_liked'
        """
        res = self.session.query(UsersLike).filter(UsersLike.liked_id == liked_id, UsersLike.users_id == users_id).all()
        a = False if res == [] else True
        return a

    def insert_liked(self, liked_id: int, users_id: int, first_name: str, last_name: str, age: int, link: str):
        """
        Функция заполнения данными таблиц 'liked' и 'users_liked'
        """
        if not self.double_liked(liked_id):
            like = Like(liked_id=liked_id, first_name=first_name, last_name=last_name, age=age, link=link)
            session.add(like)
            session.commit()
            print('избранный пользователь добавлен')
        else:
            print('double')
        if not self.double_user_like(liked_id, users_id):
            user_like = UsersLike(liked_id=liked_id, users_id=users_id)
            session.add(user_like)
            session.commit()
            print('промежуточная таблица заполнена')
        else:
            print('id double')

    def liked_users(self, users_id):
        """
        Функция выводит список пользователей из таблицы 'liked' по id пользователя из таблицы 'users'
        """
        return self.session.query(Like).join(UsersLike).filter(UsersLike.users_id == users_id)


def open_base(id_user, liked_id: int, first_name: str, last_name: str, age: int, link: str):
    service = Service(session)
    service.insert_user(id_user)
    service.insert_liked(liked_id, id_user, first_name, last_name, age, link)
    print("все получилось")


def get_liked_user(user_id):
    service = Service(session)
    list_1 = []
    x = service.liked_users(user_id)
    for n in x:
        list_1.append(n)
    return str(list_1).strip('[]').replace(',', '')


# service = Service(session)
# service.insert_user(567)
# service.insert_liked(897, 567, 'uiui', 'jhbu', 35, 'https//ijinuyugu9889786')
#
# for n in service.liked_users(888):
#     print(n)
session.close()
