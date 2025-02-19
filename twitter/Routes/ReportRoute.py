from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from ..Services.UserService import user_queries
from ..Services.ReportService import report_queries
from ..Schemas.ReportSchema import ReportSchema
from ..Utils.Validators import schema_validator
from ..Utils.Auth import csrf_token_required, ReportOptions

bp = Blueprint("report", __name__)


@bp.route("/user/report", methods=["POST"])
@jwt_required()
@csrf_token_required
@schema_validator(ReportSchema)
def report(data):
    query = report_queries()
    reported = (
        user_queries().get_object_by_value(id=data.user_reported_id).one_or_none()
    )
    if reported is None:
        return jsonify({"msg": "User don't exists."}), 404
    query.add_obj(
        query.create_obj(
            user_reporter_id=current_user.id,
            user_reported_id=data.user_reported_id,
            content_type=data.content_type,
            content_id=data.content_id,
            reasons=ReportOptions.SPAM,
            explanation=data.explanation,
            reporter=current_user,
            reported=reported,
        )
    )
    query.save_changes()
    return jsonify({"msg": "Report submitted successfully"}), 200
