#!/usr/bin/env python
import os
import sys
import coverage

from flask.ext.script import Manager, Server
from fb import app

manager = Manager(app)

manager.add_command("runserver", Server(
    use_reloader = True,
    host = '0.0.0.0',
    port = '5000')
)

@manager.command
def createdb():
    from fb import db
    app.logger.info('db created')
    db.create_all()

@manager.command
def test():
    '''
    Runs unit tests
    '''
    TESTING = True
    
    from fb import test
    test.run()

@manager.command
def cov():
    """
    Runs the unit tests with coverage.
    """
    cov = coverage.coverage(
        branch=True,
        include=['fb/*.py', 'manage.py']
    )
    cov.start()

    from fb import test
    test.run()

    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

if __name__ == "__main__":
    manager.run()