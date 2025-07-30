from app import create_app, db
from app.models import Record
import click
from flask.cli import with_appcontext
app = create_app()

@click.command('init-db')
@with_appcontext
def init_db():
    db.create_all()
    print("initialized")

if __name__ == "__main__":
    app.run(debug = True)