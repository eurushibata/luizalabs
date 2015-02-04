# -*- coding: utf-8 -*-
from flask import Flask
import logging
import os
import sys

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