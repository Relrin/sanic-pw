# Sanic-PW

A port of the [Flask-PW](https://github.com/klen/flask-pw) package for [Sanic framework](https://github.com/channelcat/sanic).

# Features
- Configuring Peewee ORM like in Flask with SQLAlchemy
- Migrate commands (create, rollback, etc.) via:
    - using commands as a part of Sanic-Script
    - click CLI
- Pre- and post-signals support for saving and deleting

# Requirements
- Python 3.6+ (older not tested)

# Using
## Installing
For installing Sanic-PW use the following command:
```
pip install sanic-pw
```

## List of available settings
| Config parameter | Description |  Default value |
|------------------|-------------|----------------|
| PEEWEE_DATABASE_URI      | A connection URI                                        | `'sqlite:///peewee.sqlite'`  |
| PEEWEE_CONNECTION_PARAMS | Connection parameters for Peewee ORM                    | `{}`                         |
| PEEWEE_MIGRATE_DIR       | Path to directory with migrations                       | `'migrations'`               |
| PEEWEE_MIGRATE_TABLE     | Name of database table with migrations                  | `'migratehistory'`           | 
| PEEWEE_MODELS_MODULE     | Path to module which contains you applications' Models  | `''`                         |
| PEEWEE_MODELS_IGNORE     | Models which should be ignored in migrations            | `[]`                         |
| PEEWEE_MODELS_CLASS      | Base models class                                       | `<sanic_pw.Model>`           |            
| PEEWEE_MANUAL            | Don't connect to db when request starts and close when it ends automatically | `False` |     
| PEEWEE_USE_READ_SLAVES   | Use database slaves for reading data when coming `SELECT ...` queries        | `True`  |    
| PEEWEE_READ_SLAVES       | A list of nodes which can be used for reading                                | `[]`    |    

## Migrations
If you're using the Sanic-Script package, then append a new command to your manager:
```python
from sanic_pw import Peewee

# ...
app.db = Peewee(app)

manager = Manager(app)
manager.add_command('db', app.db.manager)
```
For a case when you're prefer to use click it almost the same:
```python
from sanic_pw import Peewee

# ...
app.db = Peewee(app)
app.db.cli() 
```
After it, you can use database `create`, `migrate` or `rollback` commands.
