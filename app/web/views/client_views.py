import os
from flask import Blueprint, send_from_directory, current_app, jsonify
from app.web.db import db

bp = Blueprint(
    "client",
    __name__,
)


@bp.route("/health")
def health_check():
    """Health check endpoint to verify database connectivity."""
    try:
        # Test database connection
        db.session.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return (
            jsonify(
                {"status": "unhealthy", "database": "disconnected", "error": str(e)}
            ),
            503,
        )


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, "index.html")
