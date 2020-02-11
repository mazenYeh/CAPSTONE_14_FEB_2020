import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS

from models import setup_db, Trainer, Client, Session
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # db_drop_and_create_all()


    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome the home page!'
        })

    @app.route('/trainers', methods=['GET'])
    def get_trainers():
        trainers = Trainer.query.all()

        trainers_formatted = []

        for trainer in trainers:
            trainers_formatted.append(trainer.format())
        
        return jsonify({
            'success': True,
            'trainers': trainers_formatted
        })
    
    @app.route('/trainers', methods=['POST'])
    def add_trainer():
        request_data = request.get_json()

        new_trainer = Trainer()
        new_trainer.name = request_data['name']
        new_trainer.gender = request_data['gender']
        new_trainer.age = request_data['age']

        new_trainer.insert()

        return jsonify({
            'success': True,
            'new_trainer': new_trainer.format()
        })

    return app



app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)