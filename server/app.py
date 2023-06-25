#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):

        planter = [plant.to_dict() for plant in Plant.query.all()]

        response = make_response(
            jsonify(planter),
            200,
        )

        return response
    
    def post(self):

        data = request.get_json()

        another_plant = Plant( name=data['name'], image=data['image'], price=data['price'],
        )

        db.session.add(another_plant)
        db.session.commit()

        return make_response(another_plant.to_dict(), 201)
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get (self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(plant), 200
        )
        return response
    
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)