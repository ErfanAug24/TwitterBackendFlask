from flask import Blueprint, jsonify, request
from flask.views import MethodView
from ..Utils.Auth import csrf_token_required
from flask_jwt_extended import jwt_required, current_user
from ..Services import TweetService
from ..Schemas.TweetSchema import TweetSchema

bp = Blueprint("tweet", __name__)

GET = ["GET"]
POST = ["POST"]
GETandPOST = ["GET", "POST"]
tweet_schema = TweetSchema()


@bp.route("/tweets", methods=GET)
@jwt_required()
@csrf_token_required
def get_tweets():
    return jsonify(tweet_schema.dumps(TweetService.get_all_tweets(), many=True)), 200


# get user tweet

# search tweet

# crud tweet


@bp.route("/tweet", methods=POST)
@jwt_required()
@csrf_token_required
def create_tweet():
    data = request.get_json(force=True)
    errors = tweet_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tweet = TweetService.create_tweet(
        data["title"], data["body"], current_user["id"], current_user
    )
    TweetService.add_tweet(tweet)
    TweetService.save_changes()
    return tweet_schema.dump(tweet)


@bp.route("/tweet/<int:tid>", methods=["PUT"])
@jwt_required()
@csrf_token_required
def update_tweet(tid: int):
    data = request.get_json(force=True)
    errors = tweet_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tweet = TweetService.get_tweet_by_id(tid)
    tweet["title"] = data["title"]
    tweet["body"] = data["body"]
    tweet["slug"] = data["slug"]
    tweet["user_id"] = current_user["id"]
    tweet["user"] = current_user
    TweetService.save_changes()
    return tweet_schema.dump(tweet), 201


@bp.route("/tweet/<int:tid>", methods=["DELETE"])
@jwt_required()
@csrf_token_required
def delete_tweet(tid: int):
    TweetService.delete_tweet(TweetService.get_tweet_by_id(tid))
    TweetService.save_changes()
    return jsonify({"msg": "Tweet has been deleted."})
