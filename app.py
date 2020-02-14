import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS

from models import setup_db, Trainer, Client, Session
from auth import AuthError, requires_auth, LOGIN_URI


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return redirect(LOGIN_URI, 302)
    
    @app.route('/welcome')
    def welcome():
        return jsonify({
            'success': True, 
            'message': 'Login was successful, welcome!'
        })

    ###############################
    # trainers related end-points #
    ###############################
    @app.route('/trainers', methods=['GET'])
    @requires_auth('get:trainers')
    def get_trainers():
        if request.get_json():
            abort(405)

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
    @requires_auth('post:trainers')
    def add_trainer():
        request_data = request.get_json()

        try:
            if len(request_data) > 3:
                raise AuthError({'description': 'Please include only the name, gender, and age of trainer.'}, 400)
            if not request_data['name']:
                raise AuthError({'description': 'Trainer name is missing.'}, 400)
            if not request_data['gender']:
                raise AuthError({'description': 'Trainer gender is missing.'}, 400)
            if not request_data['age']:
                raise AuthError({'description': 'Trainer age is missing.'}, 400)
        except AuthError as e:
            abort(e.status_code, e.error)

        new_trainer = Trainer()
        new_trainer.name = request_data['name']
        new_trainer.gender = request_data['gender']
        new_trainer.age = request_data['age']

        new_trainer.insert()
        
        return jsonify({
            'success': True,
            'new_trainer': new_trainer.format()
        })

    @app.route('/trainers/<id>', methods=['DELETE'])
    @requires_auth('delete:trainers')
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
            'deleted_trainer': target_trainer.format()
        })

    @app.route('/trainers/<id>', methods=['PATCH'])
    @requires_auth('patch:trainers')
    def patch_trainer(id):
        request_data = request.get_json()

        try:
            target_trainer = Trainer.query.filter_by(id=id).first()
            if target_trainer is None:
                raise AuthError({
                    'code': 'trainer_not_found',
                    'description': 'There is no trainer with the reuqested id to modify.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        if 'name' in request_data:
            target_trainer.name = request_data['name']
        if 'gender' in request_data:
            target_trainer.gender = request_data['gender']
        if 'age' in request_data:
            target_trainer.age = request_data['age']

        target_trainer.update()

        return jsonify({
            'success': True,
            'modified_trainer': target_trainer.format()
        })
    
    ##############################
    # clients related end-points #
    ##############################
    @app.route('/clients', methods=['GET'])
    @requires_auth('get:clients')
    def get_clients():
        if request.get_json():
            abort(405)

        try:
            clients = Client.query.all()
            if clients is None:
                raise AuthError({
                    'code': 'no_clients',
                    'description': 'There are no clients on system yet.'
                    }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        clients_formatted = []

        for client in clients:
            clients_formatted.append(client.format())
        
        return jsonify({
            'success': True,
            'clients': clients_formatted
        })
    
    @app.route('/clients', methods=['POST'])
    @requires_auth('post:clients')
    def add_client():
        request_data = request.get_json()

        try:
            if len(request_data) > 3:
                raise AuthError({'description': 'Please include only the name, gender, and age of client.'}, 400)
            if not request_data['name']:
                raise AuthError({'description': 'Client name is missing.'}, 400)
            if not request_data['gender']:
                raise AuthError({'description': 'Client gender is missing.'}, 400)
            if not request_data['age']:
                raise AuthError({'description': 'Client age is missing.'}, 400)
        except AuthError as e:
            abort(e.status_code, e.error)

        new_client = Client()
        new_client.name = request_data['name']
        new_client.gender = request_data['gender']
        new_client.age = request_data['age']

        new_client.insert()
        
        return jsonify({
            'success': True,
            'new_client': new_client.format()
        })

    @app.route('/clients/<id>', methods=['DELETE'])
    @requires_auth('delete:clients')
    def delete_client(id):
        try:
            target_client = Client.query.filter_by(id=id).first()
            if target_client is None:
                raise AuthError({
                    'code': 'client_not_found',
                    'description': 'There is no client with the reuqested id to delete.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        target_client.delete()

        return jsonify({
            'success': True,
            'deleted_client': target_client.format()
        })

    @app.route('/clients/<id>', methods=['PATCH'])
    @requires_auth('patch:clients')
    def patch_client(id):
        request_data = request.get_json()

        try:
            target_client = Client.query.filter_by(id=id).first()
            if target_client is None:
                raise AuthError({
                    'code': 'client_not_found',
                    'description': 'There is no client with the reuqested id to modify.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        if 'name' in request_data:
            target_client.name = request_data['name']
        if 'gender' in request_data:
            target_client.gender = request_data['gender']
        if 'age' in request_data:
            target_client.age = request_data['age']

        target_client.update()

        return jsonify({
            'success': True,
            'modified_client': target_client.format()
        })

    ###############################
    # sessions related end-points #
    ###############################
    @app.route('/sessions', methods=['GET'])
    @requires_auth('get:sessions')
    def get_sessions():
        if request.get_json():
            abort(405)

        try:
            sessions = Session.query.all()
            if sessions is None:
                raise AuthError({
                    'code': 'no_sessions',
                    'description': 'There are no sessions on system yet.'
                    }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        sessions_formatted = []

        for session in sessions:
            sessions_formatted.append(session.format())
        
        return jsonify({
            'success': True,
            'sessions': sessions_formatted
        })
    
    @app.route('/sessions', methods=['POST'])
    @requires_auth('post:sessions')
    def add_session():
        request_data = request.get_json()

        try:
            if len(request_data) > 3:
                raise AuthError({'description': 'Please include only the name, trainer_id, and client_id of the session.'}, 400)
            if not request_data['name']:
                raise AuthError({'description': 'Session name is missing.'}, 400)
            if not request_data['trainer_id']:
                raise AuthError({'description': 'Session trainer id is missing.'}, 400)
            if not request_data['client_id']:
                raise AuthError({'description': 'Session client id is missing.'}, 400)
        except AuthError as e:
            abort(e.status_code, e.error)

        new_session = Session()
        new_session.name = request_data['name']
        new_session.trainer_id = request_data['trainer_id']
        new_session.client_id = request_data['client_id']

        new_session.insert()
        
        return jsonify({
            'success': True,
            'new_session': new_session.format()
        })

    @app.route('/sessions/<id>', methods=['DELETE'])
    @requires_auth('delete:sessions')
    def delete_session(id):
        try:
            target_session = Session.query.filter_by(id=id).first()
            if target_session is None:
                raise AuthError({
                    'code': 'session_not_found',
                    'description': 'There is no session with the reuqested id to delete.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        target_session.delete()

        return jsonify({
            'success': True,
            'deleted_session': target_session.format()
        })

    @app.route('/sessions/<id>', methods=['PATCH'])
    @requires_auth('patch:sessions')
    def patch_session(id):
        request_data = request.get_json()

        try:
            target_session = Session.query.filter_by(id=id).first()
            if target_session is None:
                raise AuthError({
                    'code': 'session_not_found',
                    'description': 'There is no session with the reuqested id to modify.'
                }, 404)
        except AuthError as e:
            abort(e.status_code, e.error)

        if 'name' in request_data:
            target_session.name = request_data['name']
        if 'trainer_id' in request_data:
            target_session.trainer_id = request_data['trainer_id']
        if 'client_id' in request_data:
            target_session.client_id = request_data['client_id']

        target_session.update()

        return jsonify({
            'success': True,
            'modified_session': target_session.format()
        })

    ##################
    # error handling #
    ##################
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
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)