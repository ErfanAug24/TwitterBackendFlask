from flask import jsonify, Blueprint
from ..Utils.Validators import schema_validator
from ..Schemas.FeedbackSchema import FeedbackSchema
from ..Utils.Auth import csrf_token_required
from flask_jwt_extended import jwt_required, current_user
from ..Services.FeedbackService import feedback_query

bp = Blueprint("feedback", __name__)


@bp.route("/feedback/submit", methods=["POST"])
@schema_validator(FeedbackSchema)
@csrf_token_required
@jwt_required()
def submit_feedback(data):
    query = feedback_query()
    feedback_obj = query.create_obj(
        user_id=current_user.id,
        content=data.content,
        rating=data.rating,
        category=data.category,
    )
    query.add_obj(feedback_obj)
    query.save_changes()
    return jsonify({"msg": "feedback created successfully!"}), 200
