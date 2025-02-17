from flask import Blueprint, jsonify, request
from ..Utils.Auth import csrf_token_required
from flask_jwt_extended import jwt_required, current_user
from ..Services.TweetService import tweet_queries, tweet_schema
from ..Utils.Common import create_slug
from datetime import datetime


bp = Blueprint("tweet", __name__)

GET = ["GET"]
POST = ["POST"]
GETandPOST = ["GET", "POST"]


@bp.route("/tweets", methods=GET)
# @jwt_required()
# @csrf_token_required
def get_all_tweets():
    query = tweet_queries()
    return jsonify(tweet_schema.dumps(query.get_db_model().all(), many=True)), 200


# get user tweet


# search tweet
@bp.route("/tweet/<path:identifier>", methods=GET)
def get_tweet(identifier):
    query = tweet_queries()
    if identifier.isdigit():
        return query.get_object_by_value(id=int(identifier)).one_or_none()
    elif "-" in identifier:
        return query.get_object_by_value(slug=identifier).one_or_none()
    elif identifier.strip():
        return query.get_object_by_value(title=identifier).one_or_none()
    return jsonify({"msg": "Not Found."}), 404


# crud tweet


@bp.route("/tweet", methods=POST)
@jwt_required()
@csrf_token_required
def create_tweet():
    query = tweet_queries()
    data = request.get_json(force=True)
    if not query.check_unique(title=data["title"]):
        return jsonify({"msg": "Duplicate value. The title should be unique."}), 400
    errors = tweet_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tweet = query.create_obj(
        title=data["title"],
        body=data["body"],
        slug=create_slug(data["title"]),
        user_id=current_user.id,
        user=current_user,
    )
    query.add_obj(tweet)
    query.save_changes()
    return tweet_schema.dump(tweet)


@bp.route("/tweet/<int:tid>", methods=["PUT"])
@jwt_required()
@csrf_token_required
def update_tweet(tid: int):
    query = tweet_queries()
    data = request.get_json(force=True)
    errors = tweet_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    tweet = next((t for t in current_user.tweets if t.id == tid), None)
    if not tweet:
        return jsonify({"msg": "Tweet not found."}), 404

    query.update_obj(
        tweet,
        title=data["title"],
        body=data["body"],
        user_id=current_user.id,
        user=current_user,
        updated_date=datetime.now(),
    )
    query.save_changes()
    return tweet_schema.dump(tweet), 201


@bp.route("/tweet/<int:tid>", methods=["DELETE"])
@jwt_required()
@csrf_token_required
def delete_tweet(tid: int):
    query = tweet_queries()
    tweet = next((t for t in current_user.tweets if t.id == tid), None)
    if not tweet:
        return jsonify({"msg": "Tweet not found."}), 404
    query.delete_obj(tweet)
    query.save_changes()
    return jsonify({"msg": "Tweet has been deleted."}), 200
