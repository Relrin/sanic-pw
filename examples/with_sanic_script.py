# --------------------------------------------------
# For running this example you will need to install:
# sanic==0.7.0
# sanic_script==0.3
# --------------------------------------------------
from sanic import Sanic
from sanic_script import Manager
from sanic_pw import Peewee


app = Sanic('peewee_example')
app.db = Peewee(app)  # <-- Initialize Peewee ORM here, like in Flask


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command('db', app.db.manager)  # <-- Specify CLI commands
    manager.run()
