from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from ..Services.ReplyService import reply_queries
from ..Services.LikeService import like_queries
from ..Services.CommentService import comment_queries
from ..Services.TweetService import tweet_queries
from ..Schemas.LikeSchema import LikeSchema
from ..Utils.Validators import schema_validator
from ..Utils.Auth import csrf_token_required

bp = Blueprint("like", __name__)


@bp.route("/user/like", methods=["POST"])
@jwt_required()
@csrf_token_required
@schema_validator(LikeSchema)
def like(data):
    json_data = request.get_json(force=True)
    content_type = json_data["content_type"]

    if content_type not in {"tweet", "comment", "reply"}:
        return jsonify({"error": "Invalid content type "}), 400

    query = like_queries()

    if content_type == "tweet":
        tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
        if tweet_queries().check_unique(id=tweet.id):
            return jsonify({"error": "Tweet not found"}), 404

        if not query.check_unique(user_id=current_user.id, tweet_id=tweet.id):
            return jsonify({"error": "Already liked"}), 400

        query.add_obj(
            query.create_obj(
                user_id=current_user.id,
                user=current_user,
                tweet_id=tweet.id,
                tweet=tweet,
            )
        )
    if content_type == "comment":
        comment = comment_queries().get_object_by_value(id=data.comment_id).first()

        if comment_queries().check_unique(id=comment.id):
            return jsonify({"error": "Comment not found"}), 404

        if not query.check_unique(user_id=current_user.id, comment_id=comment.id):
            return jsonify({"error": "Already liked"}), 400

        query.add_obj(
            query.create_obj(
                user_id=current_user.id,
                user=current_user,
                comment_id=comment.id,
                comment=comment,
            )
        )
    if content_type == "reply":
        reply = reply_queries().get_object_by_value(id=data.reply_id).first()
        if reply_queries().check_unique(id=reply.id):
            return jsonify({"error": "Reply not found"}), 404

        if not query.check_unique(user_id=current_user.id, reply_id=reply.id):
            return jsonify({"error": "Already liked"}), 400

        query.add_obj(
            query.create_obj(
                user_id=current_user.id,
                user=current_user,
                reply_id=reply.id,
                reply=reply,
            )
        )
    query.save_changes()
    return jsonify({"msg": f"{content_type} liked successfully"}), 200


@bp.route("/user/like", methods=["DELETE"])
@jwt_required()
@csrf_token_required
@schema_validator(LikeSchema)
def unlike(data):
    json_data = request.get_json(force=True)
    content_type = json_data["content_type"]
    if content_type not in {"tweet", "comment", "reply"}:
        return jsonify({"error": "Invalid content type "}), 400

    query = like_queries()

    if content_type == "tweet":
        tweet = tweet_queries().get_object_by_value(id=data.tweet_id).first()
        if tweet_queries().check_unique(id=tweet.id):
            return jsonify({"error": "Tweet not found"}), 404
        like_obj = query.get_object_by_value(
            tweet_id=tweet.id, user_id=current_user.id
        ).first()
        query.delete_obj(like_obj)
    if content_type == "comment":
        comment = comment_queries().get_object_by_value(id=data.comment_id).first()
        if comment_queries().check_unique(id=comment.id):
            return jsonify({"error": "Comment not found"}), 404
        like_obj = query.get_object_by_value(
            user_id=current_user.id, comment_id=comment.id
        ).first()
        query.delete_obj(like_obj)
    if content_type == "reply":
        reply = reply_queries().get_object_by_value(id=data.reply_id).first()
        if reply_queries().check_unique(id=reply.id):
            return jsonify({"error": "Reply not found"}), 404

        like_obj = query.get_object_by_value(
            user_id=current_user.id, reply_id=reply.id
        ).first()
        query.delete_obj(like_obj)
    query.save_changes()
    return jsonify({"msg": f"{content_type} unliked successfully"}), 200
