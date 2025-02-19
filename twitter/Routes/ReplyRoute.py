from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, current_user
from ..Services.ReplyService import reply_queries, reply_schema
from ..Services.CommentService import comment_queries
from ..Schemas.ReplySchema import ReplySchema
from ..Utils.Validators import schema_validator
from ..Utils.Auth import csrf_token_required


bp = Blueprint("reply", __name__)


@bp.route("/user/reply", methods=["GET"])
@jwt_required()
@csrf_token_required
@schema_validator(ReplySchema)
def get_reply(data):
    query = reply_queries()
    comment = comment_queries().get_object_by_value(id=data.comment_id).first()
    reply = query.get_object_by_value(user_id=current_user.id, comment_id=comment.id)
    return jsonify(reply_schema.dump(reply))


@bp.route("/user/reply", methods=["POST"])
@jwt_required()
@csrf_token_required
@schema_validator(ReplySchema)
def get_reply(data):
    query = reply_queries()
    comment = comment_queries().get_object_by_value(id=data.comment_id).first()
    query.add_obj(
        query.create_obj(
            user_id=current_user.id,
            comment_id=comment.id,
            user=current_user,
            comment=comment,
            message=data.message,
        )
    )
    query.save_changes()
    return jsonify({"msg": "reply created successfully"}), 200


@bp.route("/user/reply", methods=["PUT"])
@jwt_required()
@csrf_token_required
@schema_validator(ReplySchema)
def update_reply(data):
    query = reply_queries()
    comment = comment_queries().get_object_by_value(id=data.comment_id).first()
    reply = query.get_object_by_value(user_id=current_user.id, comment_id=comment.id)
    query.update_obj(reply, message=data.message)
    query.save_changes()
    return jsonify({"msg": "reply updated successfully"}), 201


@bp.route("/user/reply", methods=["DELETE"])
@jwt_required()
@csrf_token_required
@schema_validator(ReplySchema)
def delete_reply(data):
    query = reply_queries()
    comment = comment_queries().get_object_by_value(id=data.comment_id).first()
    reply = query.get_object_by_value(user_id=current_user.id, comment_id=comment.id)
    query.delete_obj(reply)
    query.save_changes()
    return jsonify({"msg": "reply deleted successfully!"}), 200
