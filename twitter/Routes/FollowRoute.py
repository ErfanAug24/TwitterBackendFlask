from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from ..Services.FollowService import follow_queries
from ..Services.UserService import user_queries

bp = Blueprint("follow", __name__)


@bp.route("/user/follow", methods=["POST"])
@jwt_required()
def follow():
    data = request.get_json(force=True)
    query = follow_queries()
    following = user_queries().get_object_by_value(id=data.user_id).first()
    query.add_obj(
        query.create_obj(
            follower_id=current_user.id,
            following_id=following.id,
            following=following,
            follower=current_user,
        )
    )
    query.save_changes()
    return jsonify({"msg": "followed successfully"}), 200


@bp.route("/user/unfollow", methods=["DELETE"])
@jwt_required()
def unfollow():
    data = request.get_json(force=True)
    query = follow_queries()
    following = user_queries().get_object_by_value(id=data.user_id).first()
    query.delete_obj(
        query.get_object_by_value(
            follower_id=current_user.id, following_id=following.id
        ).first()
    )
    query.save_changes()
    return jsonify({"msg": "unfollowed successfully"}), 200
