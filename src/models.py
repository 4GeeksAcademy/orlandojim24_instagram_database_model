from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# Enum for media type
class MediaType(enum.Enum):
    image = "image"
    video = "video"

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)

    # Relationships (to connect with other tables)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower',
                             foreign_keys='Follower.user_to_id',
                             back_populates='followed')
    following = relationship('Follower',
                             foreign_keys='Follower.user_from_id',
                             back_populates='follower')


class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships (back to the User table)
    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete')
    media = relationship('Media', back_populates='post', cascade='all, delete')

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationship
    post = relationship('Post', back_populates='media')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')


if __name__ == '__main__':
    from eralchemy2 import render_er
    render_er(Base, 'diagram.png')