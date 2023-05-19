import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import backref

Base = declarative_base()


class User(Base):     # класс для создания таблицы 'users'
    __tablename__ = 'users'

    users_id = sq.Column(sq.BigInteger, primary_key=True)


class Like(Base):     # класс для создания таблицы 'liked'
    __tablename__ = 'liked'

    liked_id = sq.Column(sq.BigInteger, primary_key=True)
    first_name = sq.Column(sq.String(length=20), nullable=False)
    last_name = sq.Column(sq.String(length=30), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    link = sq.Column(sq.String(length=250), nullable=False)

    def __str__(self):
        return f'🥰{self.first_name} {self.last_name}\n возраст: {self.age}\n ссылка на профиль: {self.link}\n\n'

    def __repr__(self):
        return f'🥰{self.first_name} {self.last_name}\n возраст: {self.age}\n ссылка на профиль: {self.link}\n\n'


class UsersLike(Base):    # класс для создания таблицы 'users_liked'
    __tablename__ = 'users_liked'

    users_id = sq.Column(sq.BigInteger, sq.ForeignKey('users.users_id', ondelete="CASCADE"), primary_key=True)
    liked_id = sq.Column(sq.BigInteger, sq.ForeignKey('liked.liked_id', ondelete="CASCADE"), primary_key=True)

    like = relationship("Like", backref=backref("user_like"))
    user = relationship("User", backref=backref("user_like"))


def create_tables(engine):
    """
    Функция удаляет и создаёт таблицы класса Base
    """
    # Base.metadata.drop_all(engine)
    # print('таблицы удалены')
    Base.metadata.create_all(engine)
    print('таблицы созданы')