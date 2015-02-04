# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields
import requests
from models import Person
from fb import db

class PersonSchema(Schema):
    class Meta:
        fields = ('facebookId', 'username', 'name', 'gender')

class FbAPI(MethodView):

    def get(self, person_id):
        if person_id is None:
            limit = None
            try:
                if 'limit' in request.args:
                    limit = int(request.args['limit'])
       
            except ValueError:
                pass

            p = Person.query.limit(limit).all()
            r = PersonSchema(many=True).dump(p).data

            return jsonify({"persons": r}), 200

        else:
            p = Person.query.get(int(person_id))
            if p is None:
                return jsonify({'error': 'Not found.'}), 404
            r = PersonSchema().dump(p).data

            return jsonify({'persons': [r]}), 200

    def post(self, person_id):
        if not 'facebookId' in request.form:
            return jsonify({'error': 'Bad request.'}), 400

        try:
            fb = requests.get('http://graph.facebook.com/'
                        +request.form['facebookId']).json()
            if 'error' in fb:
                return jsonify({'error': 'The alias you requested do not ' \
                                'exist.'}), 803
        except:
            return jsonify({'error': 'Internal Server Error.'}), 500

        try:
            p = Person(
                facebookId=fb['id'],
                username=fb['username'],
                name=fb['name'],
                gender=fb['gender']
            )
            db.session.add(p)
            db.session.commit()

        except IntegrityError:
            pass

        r = PersonSchema().dump(p).data
        return jsonify({'persons': [r]}), 200

    def delete(self, person_id):
        p = Person.query.get(person_id)

        if p is None:
            return jsonify({'error': 'Not found.'}), 404

        db.session.delete(p)
        db.session.commit()

        return jsonify({'success': 'Removed.'}), 204