import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.BigInteger, primary_key=True)

    def __str__(self):
        return f'{self.id}'


class Like(Base):
    __tablename__ = 'liked'

    id = sq.Column(sq.Integer, primary_key=True)
    liked_id = sq.Column(sq.BigInteger, nullable=False)
    first_name = sq.Column(sq.String(length=20), nullable=False)
    last_name = sq.Column(sq.String(length=30), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    link = sq.Column(sq.String(length=250), nullable=False)
    users_id = sq.Column(sq.BigInteger, sq.ForeignKey('users.id', ondelete="CASCADE"))

    user = relationship(User, backref=backref('likes', passive_deletes=True))

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, возраст: {self.age}, ссылка на профиль: {self.link}'


class NotLike(Base):
    __tablename__ = 'not_liked'

    id = sq.Column(sq.Integer, primary_key=True)
    not_liked_id = sq.Column(sq.BigInteger, nullable=False)
    users_id = sq.Column(sq.BigInteger, sq.ForeignKey('users.id', ondelete="CASCADE"))

    user = relationship(User, backref=backref('not_likes', passive_deletes=True))


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    # print('таблицы удалены')
    Base.metadata.create_all(engine)
    # print('таблицы созданы')
