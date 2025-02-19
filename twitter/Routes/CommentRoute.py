from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, current_user
from ..Services.CommentService import comment_queries, comment_schema
from ..Services.TweetService import tweet_queries
from ..Schemas.CommentSchema import CommentSchema
from ..Utils.Validators import schema_validator
from ..Utils.Auth import csrf_token_required

bp = Blueprint("comment", __name__)


@bp.route("/user/comment", methods=["POST"])
@jwt_required()
@csrf_token_required
@schema_validator(CommentSchema)
def get_comment(data):
    query = comment_queries()
    tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
    comment = query.get_object_by_value(tweet_id=tweet.id, user_id=current_user.id)
    return comment_schema.dump(comment)


@bp.route("/user/comment", methods=["POST"])
@jwt_required()
@csrf_token_required
@schema_validator(CommentSchema)
def create_comment(data):
    query = comment_queries()
    tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
    query.add_obj(
        query.create_obj(
            tweet_id=data.tweet_id,
            tweet=tweet,
            user_id=current_user.id,
            user=current_user,
            message=data.message,
        )
    )
    query.save_changes()
    return jsonify({"msg": "comment created successfully"}), 200


@bp.route("/user/comment", methods=["PUT"])
@jwt_required()
@csrf_token_required
@schema_validator(CommentSchema)
def update_comment(data):
    query = comment_queries()
    tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
    comment = query.get_object_by_value(tweet_id=tweet.id, user_id=current_user.id)
    query.update_obj(comment, message=data.message)
    query.save_changes()
    return jsonify({"msg": "comment updated successfully!"}), 201


@bp.route("/user/comment", methods=["PUT"])
@jwt_required()
@csrf_token_required
@schema_validator(CommentSchema)
def delete_comment(data):
    query = comment_queries()
    tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
    comment = query.get_object_by_value(tweet_id=tweet.id, user_id=current_user.id)
    query.delete_obj(comment)
    query.save_changes()
    return jsonify({"msg": "comment deleted successfully"})
