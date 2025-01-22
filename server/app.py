#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Home Route
@app.route('/')
def home():
    return "Welcome to the Camping Fun API!"


# RESTful Resources
class CampersResource(Resource):
    def get(self):
        campers = Camper.query.all()
        return jsonify([camper.to_dict(only=('id', 'name', 'age')) for camper in campers])

    def post(self):
        data = request.json
        try:
            camper = Camper(name=data['name'], age=data['age'])
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age')), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400


class CamperResource(Resource):
    def get(self, id):
        camper = Camper.query.get(id)
        if not camper:
            return {"error": "Camper not found"}, 404
        return camper.to_dict(only=('id', 'name', 'age', 'signups.activity'))

    def patch(self, id):
        camper = Camper.query.get(id)
        if not camper:
            return {"error": "Camper not found"}, 404
        data = request.json
        try:
            if 'name' in data:
                camper.name = data['name']
            if 'age' in data:
                camper.age = data['age']
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age'))
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400


class ActivitiesResource(Resource):
    def get(self):
        activities = Activity.query.all()
        return jsonify([activity.to_dict(only=('id', 'name', 'difficulty')) for activity in activities])


class ActivityResource(Resource):
    def delete(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return {"error": "Activity not found"}, 404
        try:
            db.session.delete(activity)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400


class SignupResource(Resource):
    def post(self):
        data = request.json
        try:
            signup = Signup(camper_id=data['camper_id'], activity_id=data['activity_id'], time=data['time'])
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(only=('id', 'camper_id', 'activity_id', 'time', 'activity', 'camper')), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400


# Register Resources
api.add_resource(CampersResource, '/campers')
api.add_resource(CamperResource, '/campers/<int:id>')
api.add_resource(ActivitiesResource, '/activities')
api.add_resource(ActivityResource, '/activities/<int:id>')
api.add_resource(SignupResource, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
