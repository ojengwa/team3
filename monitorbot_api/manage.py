#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Role, Frequency, User, Watch, Check
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


# setup shell commands and migration contexts:
def make_shell_context():
    return dict(app=app, db=db, Role=Role, Frequency=Frequency, User=User, Watch=Watch, Check=Check)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
