#!/usr/bin/env python
import os, sys

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
    db.create_all()

@manager.command
def test():
    '''
    Runs tests
    '''
    TESTING = True
    import test
    test.run()

if __name__ == "__main__":
    manager.run()