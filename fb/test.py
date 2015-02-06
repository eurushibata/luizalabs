# -*- coding: utf-8 -*-
import json
import os
import unittest
from flask import request
from fb import db, app
from fb.models import Person

P1 =  {
        "persons": [{
                "facebookId": 4,
                "gender": "male",
                "name": "Mark Zuckerberg",
                "username": "zuck"}]}
P2 =  {
        "persons": [{
                "facebookId": 562603040,
                "gender": "male",
                "name": "Emerson Urushibata",
                "username": "ofemerson"}]}
P3 = {
        "persons": [{
                "facebookId": 40,
                "gender": "female",
                "name": "Ebonie Hazle",
                "username": "ebonie.hazle"}]}
P1P2 = {
        "persons": [{
                "facebookId": 4,
                "gender": "male",
                "name": "Mark Zuckerberg",
                "username": "zuck"},{
                "facebookId": 562603040,
                "gender": "male",
                "name": "Emerson Urushibata",
                "username": "ofemerson"
                }]}

class FbViewTestCase(unittest.TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        p1 = Person(
            facebookId=4,
            username='zuck',
            name='Mark Zuckerberg',
            gender='male'
        )
        p2 = Person(
            facebookId=562603040,
            username='ofemerson',
            name='Emerson Urushibata',
            gender='male'
        )

        db.session.add_all([p1, p2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        '''
        Test: get all records
        '''
        tester = app.test_client(self)
        response = tester.get('/person')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), P1P2)

    def test_get_none(self):
        '''
        Test: get limit of 0 records
        '''
        tester = app.test_client(self)
        response = tester.get('/person?limit=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'persons': []})

    def test_get_one(self):
        '''
        Test: get limit of 1 record 
        '''
        tester = app.test_client(self)
        response = tester.get('/person?limit=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), P1)

    def test_get_limit(self):
        '''
        Test: get all records if args is misstyped (limits)
        '''
        tester = app.test_client(self)
        response = tester.get('/person?limits=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), P1P2)

    def test_get_mark(self):
        '''
        Test: get record from mark (facebookId=4)
        '''
        tester = app.test_client(self)
        response = tester.get('/person/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), P1)

    def test_get_unknown(self):
        '''
        Test: get record from unknown (facebookId=0)
        '''
        tester = app.test_client(self)
        response = tester.get('/person/0')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {'error': 'Not found.'})

    def test_post(self):
        '''
        Test: post new record (facebookId=40)
        '''
        tester = app.test_client(self)
        response = tester.post('/person', data=dict(facebookId=40))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), P3)

    def test_post_mistyped(self):
        '''
        Test: post new record with mistyped fields (FACEBOOKID=40)
        '''
        tester = app.test_client(self)
        response = tester.post('/person', data=dict(FACEBOOKID=40))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'Bad request.'})

    def test_post_inexist(self):
        '''
        Test: post new record that doesn't exist on Facebook (facebookId=0)
        '''
        tester = app.test_client(self)
        response = tester.post('/person', data=dict(facebookId=0))
        self.assertEqual(response.status_code, 803)
        self.assertEqual(json.loads(response.data),
            {'error': 'The alias you requested do not exist.'})

    def test_delete(self):
        '''
        Test: delete record (facebookId=4)
        '''
        tester = app.test_client(self)
        response = tester.delete('/person/4')
        self.assertEqual(response.status_code, 204)
        # self.assertEqual(json.loads(response.data), {'success': 'Removed.'})

    def test_delete_inexist(self):
        '''
        Test: delete record that doesn't exist (facebookId=40)
        '''
        tester = app.test_client(self)
        response = tester.delete('/person/40')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {'error': 'Not found.'})

def run():
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))

    try:
        unittest.TextTestRunner().run(unittest.makeSuite(FbViewTestCase))
    except:
        pass


if __name__ == '__main__':
    run()