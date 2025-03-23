from flask import Blueprint

# Create the Blueprint
user_bp = Blueprint("user", __name__)

@user_bp.route("/test", methods=["GET"])
def test():
    return "User route is working!"
