#!/usr/bin/env python
import os
# import os.path as op
#
# file_path = op.join(op.dirname(__file__), 'files')
# try:
#     os.mkdir(file_path)
# except OSError:
#     pass


from app import create_app, db
from app.models import user, role
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host='localhost', port=5002)


#The make_shell_context() function registers the application and database instances and the models
# so that they are automatically imported into the shell

def make_shell_context():
    return dict(app=app, db=db, User = user, Role = role)

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

