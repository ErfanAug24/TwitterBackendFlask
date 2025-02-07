from ..Models import Tweet
from ..sqlalchemy_conf import db


def get_tweet_by_id(tid: int):
    db.session.query(Tweet).filter_by(id=tid).first()
