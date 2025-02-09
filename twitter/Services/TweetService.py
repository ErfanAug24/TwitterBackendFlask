from typing import Optional

from ..Models import Tweet
from ..Config.sqlalchemy_conf import db


def get_tweet_by_id(tid: int):
    db.session.query(Tweet).filter_by(id=tid).first()


def get_all_tweets():
    db.session.query(Tweet).all()


def create_tweet(
    title: str, body: str, user_id: int, user: "User", slug: Optional[str] = None
):
    tweet = Tweet(title, body, slug, user_id, user)
    return tweet


def add_tweet(tweet: Tweet):
    db.session.add(tweet)


def save_changes():
    db.session.commit()


def delete_tweet(tweet: Tweet):
    db.session.delete(tweet)
