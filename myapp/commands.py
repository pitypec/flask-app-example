import click
from flask.cli import with_appcontext
from .models import User, Userprofile

from myapp.extensions import db


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
