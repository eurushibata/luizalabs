# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    facebookId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(6))

    def __repr__(self):
        return '<User %d - %r>' % (self.facebookId, self.username)