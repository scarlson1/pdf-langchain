import click
import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()


def init_db():
    """Initialize database tables if they don't exist."""
    with current_app.app_context():
        try:
            os.makedirs(current_app.instance_path)
        except OSError:
            pass
        # Only create tables if they don't exist
        db.create_all()
        click.echo("Database tables initialized.")


def reset_db():
    """Reset database by dropping and recreating all tables."""
    with current_app.app_context():
        try:
            os.makedirs(current_app.instance_path)
        except OSError:
            pass
        db.drop_all()
        db.create_all()
        click.echo("Database reset and initialized.")


@click.command("init-db")
def init_db_command():
    """Initialize database tables (safe for production)."""
    init_db()


@click.command("reset-db")
def reset_db_command():
    """Reset database by dropping and recreating all tables (destructive)."""
    reset_db()
