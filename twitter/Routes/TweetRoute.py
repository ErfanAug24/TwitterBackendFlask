from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

bp = Blueprint("tweet", __name__)
