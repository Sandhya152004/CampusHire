from functools import wraps

from flask import jsonify

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt


def role_required(required_role):

    def wrapper(fn):

        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):

            claims = get_jwt()

            if claims['role'] != required_role:

                return jsonify({
                    "message": "Access denied"
                }), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper