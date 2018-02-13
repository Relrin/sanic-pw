# --------------------------------------------------
# For running this example you will need to install:
# sanic==0.7.0
# click==6.7
# --------------------------------------------------
from sanic import Sanic
from sanic_pw import Peewee


app = Sanic('peewee_example')
app.db = Peewee(app)  # <-- Initialize Peewee ORM here, like in Flask


if __name__ == "__main__":
    app.db.cli()  # <-- Invoke a CLI as function
