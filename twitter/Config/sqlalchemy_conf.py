from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_tables():
    from ..Models import User, Feedback, LowPriority, Report, Token, Tweet
    from ..Models.Reactions import Follow, Comment, Like, Reply

    db.create_all()


@click.command("init-tables")
def init_tables_command():
    init_tables()
    click.echo("Tables initialized successfully!")


def init_app(app):
    db.init_app(app)


def register_cli(app):
    app.cli.add_command(init_tables_command)
