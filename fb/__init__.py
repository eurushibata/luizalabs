# -*- coding: utf-8 -*-
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)

try:  
    os.environ["APP_SETTINGS"]
    if not os.environ['APP_SETTINGS'] in ['config.DevelopmentConfig',
        'config.TestingConfig']:
        raise KeyError
    app.config.from_object(os.environ['APP_SETTINGS'])
except KeyError: 
    print "Please set the environment variable APP_SETTINGS as " \
    "'config.DevelopmentConfig' or 'config.TestingConfig'. " \
    "i.e.: export APP_SETTINGS='config.DevelopmentConfig'"
    sys.exit(0)

if not app.config['TESTING']:
    file_handler = RotatingFileHandler('fb.log', 'a', 100000000, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

from fb.models import db
db.init_app(app)

from views import FbAPI

person_view = FbAPI.as_view('fb_api')
app.add_url_rule('/person', defaults={'person_id': None},view_func=person_view,
                    methods=['GET','POST',])
app.add_url_rule('/person/<int:person_id>', view_func=person_view,
                    methods=['GET','DELETE'])

if __name__ == '__main__':
    app.run()