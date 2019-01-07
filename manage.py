#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host='0.0.0.0', port=5002)

#The make_shell_context() function registers the application and database instances and the models
# so that they are automatically imported into the shell
def make_shell_context():
    return dict(app=app, db=db, User = User, Role = Role)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", server)

if __name__ == '__main__':
    manager.run()
