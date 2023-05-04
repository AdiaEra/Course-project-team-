import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, User, Like, NotLike

DSN = 'postgresql://postgres:Hun$917&305TpS@localhost:5432/users_vk_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Service:
    def __init__(self, session):
        self.session = session

    def insert_user(self, id: int):
        try:
            user = User(id=id)
            # session.add(user)
            session.commit()
            print('пользователь добавлен в базу')
        except:
            print('такой пользователь есть в базе')
        return user

    def insert_liked(self, liked_id: int, first_name: str, last_name: str, age: int, link: str, users_id: int):
        like = Like(liked_id=liked_id, first_name=first_name, last_name=last_name, age=age, link=link,
                    users_id=user1.id)
        # session.add(like)
        session.commit()
        return like

    def insert_not_liked(self, not_liked_id: int, users_id: int):
        not_like = NotLike(not_liked_id=not_liked_id, users_id=user1.id)
        # session.add(not_like)
        session.commit()
        return not_like

    def delete_user(self, user):  # что прописать?
        session.query(User).filter(User.id == 11).delete()
        session.commit()
        print('пользователь удалён')

    def liked_users(self, data):  # ???
        return self.session.query(Like)


service = Service(session)
user1 = service.insert_user(9)
liked1 = service.insert_liked(67767676754, 'kjhuhgyubyvty', 'hdtjhg', 22, 'https//ijinuyugu9889786', users_id=user1.id)
nliked1 = service.insert_not_liked(778999897896764, users_id=user1.id)

# del_user = service.delete_user(user1)

# for n in service.liked_users(liked1):
#     print(n)

session.close()
