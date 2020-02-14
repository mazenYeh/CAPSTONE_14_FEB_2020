import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Trainer, Client, Session


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "gym_service_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        trainers = Trainer.query.all()
        for trainer in trainers:
            trainer.delete()

        clients = Client.query.all()
        for client in clients:
            client.delete()

        sessions = Session.query.all()
        for session in sessions:
            session.delete()

        pass


    # /////////////////////////////////////
    # Tests for trainers related end-points
    # /////////////////////////////////////
    
    # ////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful GET requests for all trainers
    # ////////////////////////////////////////////////////////////////////
    def test_get_trainers_success(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trainers'])

        trainer.delete()

    def test_get_trainers_fail(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', json={'age': 75})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        trainer.delete()

    # /////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful POST requests for all trainers
    # /////////////////////////////////////////////////////////////////////
    def test_post_trainers_success(self):
        res = self.client().post('/trainers', json={"name": "Mostafa", "gender": "male", "age": 28})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_trainer']['id'])
        self.assertEqual(data['new_trainer']['name'], 'Mostafa')
        self.assertEqual(data['new_trainer']['gender'], 'male')
        self.assertEqual(data['new_trainer']['age'], 28)
    
    def test_post_trainers_fail(self):
        res = self.client().post('/trainers', json={"name": "Mostafa", "gender": "male", "age": 28, 'height': 170})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # ///////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all trainers
    # ///////////////////////////////////////////////////////////////////////
    def test_delete_trainers_success(self):
        post_res = self.client().post('/trainers', json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/trainers/' + str(post_res_data['new_trainer']['id']))
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_trainer']['id'])
        self.assertEqual(delete_res_data['deleted_trainer']['name'], 'Mostafa')
        self.assertEqual(delete_res_data['deleted_trainer']['gender'], 'male')
        self.assertEqual(delete_res_data['deleted_trainer']['age'], 28)
    
    def test_delete_trainers_fail(self):
        post_res = self.client().post('/trainers', json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/trainers/1000')
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all trainers
    # //////////////////////////////////////////////////////////////////////
    def test_patch_trainers_success(self):
        post_res = self.client().post('/trainers', json={'name': "Rafiki", "gender": "monkey", "age": 123})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/trainers/' + str(post_res_data['new_trainer']['id']), json={'name': 'Mostafa', 'gender': 'male', 'age': 28})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_trainer']['id'])
        self.assertEqual(patch_res_data['modified_trainer']['name'], 'Mostafa')
        self.assertEqual(patch_res_data['modified_trainer']['gender'], 'male')
        self.assertEqual(patch_res_data['modified_trainer']['age'], 28)
    
    def test_patch_trainers_fail(self):
        post_res = self.client().post('/trainers', json={'name': "Rafiki", "gender": "monkey", "age": 123})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/trainers/1000', json={'name': 'Mostafa', 'gender': 'male', 'age': 28})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 404)
        self.assertEqual(patch_res_data['success'], False)


    # ////////////////////////////////////
    # Tests for clients related end-points
    # ////////////////////////////////////
    
    # ///////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful GET requests for all clients
    # ///////////////////////////////////////////////////////////////////
    def test_get_clients_success(self):
        client = Client(name='Yehia', gender='male', age=102)
        client.insert()

        res = self.client().get('/clients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])

        client.delete()

    def test_get_clients_fail(self):
        client = Client(name='Yehia', gender='male', age=102)
        client.insert()

        res = self.client().get('/clients', json={'age': 75})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        client.delete()

    # ////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful POST requests for all clients
    # ////////////////////////////////////////////////////////////////////
    def test_post_clients_success(self):
        res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_client']['id'])
        self.assertEqual(data['new_client']['name'], 'Mostafa')
        self.assertEqual(data['new_client']['gender'], 'male')
        self.assertEqual(data['new_client']['age'], 28)
    
    def test_post_clients_fail(self):
        res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28, 'height': 170})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all clients
    # //////////////////////////////////////////////////////////////////////
    def test_delete_clients_success(self):
        post_res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/clients/' + str(post_res_data['new_client']['id']))
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_client']['id'])
        self.assertEqual(delete_res_data['deleted_client']['name'], 'Mostafa')
        self.assertEqual(delete_res_data['deleted_client']['gender'], 'male')
        self.assertEqual(delete_res_data['deleted_client']['age'], 28)
    
    def test_delete_clients_fail(self):
        post_res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/clients/1000')
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # /////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all clients
    # /////////////////////////////////////////////////////////////////////
    def test_patch_clients_success(self):
        post_res = self.client().post('/clients', json={'name': "Rafiki", "gender": "monkey", "age": 123})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/clients/' + str(post_res_data['new_client']['id']), json={'name': 'Mostafa', 'gender': 'male', 'age': 28})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_client']['id'])
        self.assertEqual(patch_res_data['modified_client']['name'], 'Mostafa')
        self.assertEqual(patch_res_data['modified_client']['gender'], 'male')
        self.assertEqual(patch_res_data['modified_client']['age'], 28)
    
    def test_patch_clients_fail(self):
        post_res = self.client().post('/clients', json={'name': "Rafiki", "gender": "monkey", "age": 123})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/clients/1000', json={'name': 'Mostafa', 'gender': 'male', 'age': 28})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 404)
        self.assertEqual(patch_res_data['success'], False)


    # /////////////////////////////////////
    # Tests for sessions related end-points
    # /////////////////////////////////////
    
    # ////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful GET requests for all sessions
    # ////////////////////////////////////////////////////////////////////
    def test_get_sessions_success(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        client = Client(name='Yehia', gender='male', age=102)
        client.insert()

        session = Session(name='Mostafa-Yehia training session', trainer_id=trainer.id, client_id=client.id)
        session.insert()

        res = self.client().get('/sessions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['sessions'])

        trainer.delete()
        client.delete()
        session.delete()

    def test_get_sessions_fail(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        client = Client(name='Yehia', gender='male', age=102)
        client.insert()

        session = Session(name='Mostafa-Yehia training session', trainer_id=trainer.id, client_id=client.id)
        session.insert()

        res = self.client().get('/sessions', json={'age': 75})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        trainer.delete()
        client.delete()
        session.delete()

    # /////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful POST requests for all sessions
    # /////////////////////////////////////////////////////////////////////
    def test_post_sessions_success(self):
        res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_session']['id'])
        self.assertEqual(data['new_session']['name'], 'Mostafa-Yehia training session')
        self.assertEqual(data['new_session']['trainer_id'], 1)
        self.assertEqual(data['new_session']['client_id'], 3)
    
    def test_post_sessions_fail(self):
        res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3, 'duration_min': 45})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
    
    # ///////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all sessions
    # ///////////////////////////////////////////////////////////////////////
    def test_delete_sessions_success(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/sessions/' + str(post_res_data['new_session']['id']))
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_session']['id'])
        self.assertEqual(delete_res_data['deleted_session']['name'], 'Mostafa-Yehia training session')
        self.assertEqual(delete_res_data['deleted_session']['trainer_id'], 1)
        self.assertEqual(delete_res_data['deleted_session']['client_id'], 3)
    
    def test_delete_sessions_fail(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/sessions/1000')
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all sessions
    # //////////////////////////////////////////////////////////////////////
    def test_patch_session_success(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Rafiki training session', 'trainer_id': 1, 'client_id': 3})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/sessions/' + str(post_res_data['new_session']['id']), json={'name': 'Mostafa-Yehia', 'trainer_id': 100, 'client_id': 300})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_session']['id'])
        self.assertEqual(patch_res_data['modified_session']['name'], 'Mostafa-Yehia')
        self.assertEqual(patch_res_data['modified_session']['trainer_id'], 100)
        self.assertEqual(patch_res_data['modified_session']['client_id'], 300)
    
    def test_patch_session_fail(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Rafiki training session', 'trainer_id': 1, 'client_id': 3})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/sessions/1000' + str(post_res_data['new_session']['id']), json={'name': 'Mostafa-Yehia', 'trainer_id': 100, 'client_id': 300, 'duration_min': 45})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 404)
        self.assertEqual(patch_res_data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
