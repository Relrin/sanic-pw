# Sanic-PW

A port of the [Flask-PW](https://github.com/klen/flask-pw) package for [Sanic framework](https://github.com/channelcat/sanic).

### Requirements
- Python 3.5+ (older not tested)
- peewee==2.10.2
- cached_property=1.3

**NOTE**: For using the latest Peewee ORM releases with the `pewee_async` package, necessary that` pewee_async` will have made changes in its codebase.

### Features
- Configuring Peewee ORM like in Flask with SQLAlchemy
- Migrate commands (init, create, rollback, etc.) via:
    - using commands as a part of Sanic-Script
    - click CLI
- Pre- and post-signals support for saving and deleting
