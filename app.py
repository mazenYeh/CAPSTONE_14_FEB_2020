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

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome to the home page!'
        })

    @app.route('/trainers', methods=['GET'])
    def get_trainers():
        try:
            trainers = Trainer.query.all()
            if trainers is None:
                raise AuthError({
                    'code': 'no_trainers',
                    'description': 'There are no trainers on system yet.'
                    }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        trainers_formatted = []

        for trainer in trainers:
            trainers_formatted.append(trainer.format())
        
        return jsonify({
            'success': True,
            'trainers': trainers_formatted
        })
    
    @app.route('/trainers', methods=['POST'])
    def add_trainer():
        try:
            request_data = request.get_json()

            new_trainer = Trainer()
            new_trainer.name = request_data['name']
            new_trainer.gender = request_data['gender']
            new_trainer.age = request_data['age']

            new_trainer.insert()
        except:
        

        return jsonify({
            'success': True,
            'new_trainer': new_trainer.format()
        })

    @app.route('/trainers/<id>', methods=['DELETE'])
    def delete_trainer(id):
        try:
            target_trainer = Trainer.query.filter_by(id=id).first()
            if target_trainer is None:
                raise AuthError({
                    'code': 'trainer_not_found',
                    'description': 'There is no trainer with the reuqested id to delete.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        target_trainer.delete()

        return jsonify({
            'success': True,
            'deleted_trainer': target_trainer
        })

    # error handling

    @app.errorhandler(400)
    def authError_bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": error.description
                        }), 400

    @app.errorhandler(401)
    def authError_unauthorized(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": error.description
                        }), 401

    @app.errorhandler(404)
    def authError_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": error.description
                        }), 404


    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)