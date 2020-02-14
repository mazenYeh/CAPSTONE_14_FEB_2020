import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Trainer, Client, Session


manager_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRiODA3ZWY5YjEwZjA0ZmM5MzQ4IiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMTAxLCJleHAiOjE1ODE3ODg1MDEsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2xpZW50cyIsImRlbGV0ZTpzZXNzaW9ucyIsImRlbGV0ZTp0cmFpbmVycyIsImdldDpjbGllbnRzIiwiZ2V0OnNlc3Npb25zIiwiZ2V0OnRyYWluZXJzIiwicGF0Y2g6Y2xpZW50cyIsInBhdGNoOnNlc3Npb25zIiwicGF0Y2g6dHJhaW5lcnMiLCJwb3N0OmNsaWVudHMiLCJwb3N0OnNlc3Npb25zIiwicG9zdDp0cmFpbmVycyJdfQ.Pq7nrsXar8Bd-IhjLhv_uUJM7IuMFnpxWyZy1EXjvmS2zC9ZHEr1Mhjoi-HCsvVahlmMJpsQztDd7Ga-jgg382JBnVzEixpRKEgQfjHScKXYcgl0gvTsQ7kydOPL64XnGsxyYnyDbZbRdwKiek5UVEYYpnDfFI3ZSHVA8tmb3QrW5-XsjmZSZo7cD7FzR-5XPVhQUS2SAfG0NXPBhaqlkS8JkRhPGGRwp13u-BCRm46H_bgkidg7Whl7b9JoCqejkfuNXw-BUR6YJrQ1isL86ZI6Qp00jSaWnNdqIfPKLIs3HASSksdulroxsetyCifCi1CokORvCVzXqyFk0QRyUQ'
trainer_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRhMGM3ZWY5YjEwZjA0ZmM5MTc1IiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMTkyLCJleHAiOjE1ODE3ODg1OTIsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6c2Vzc2lvbnMiLCJnZXQ6Y2xpZW50cyIsImdldDpzZXNzaW9ucyIsImdldDp0cmFpbmVycyIsInBhdGNoOmNsaWVudHMiLCJwYXRjaDpzZXNzaW9ucyIsInBvc3Q6Y2xpZW50cyIsInBvc3Q6c2Vzc2lvbnMiXX0.xkFevU_xYTZxoJewv9xRTC4wSxT9yvigC0PshXWbHYKW87RqoGkYn3crr37-ynT54uB1xcuQxfIx4aDfbcyVG_hcN48KJxPJlH_Y1fOjwenZcjmM3BBXJl8yJVux8lIVoWxwO_2nFKc5wAJoXM4nuaHqUoPgwS1Y2o7nlvAuEWPCJErs2clBt-zJCSyVxKrNUHhkWuoAvDGJUl8uQX-kZkW4F1JDy9yAsSACnY9lVTnp8rlX0lHA3mEXCyYERiTPpz5NvUbNjHi54Kgq8VuExM5uIcS8HTV2Gh3CW8KWABxv0vttAA52miOfkd-hP30Ajyug8fp3ULTDsniRYHt5yA'
client_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRhNDQ2N2YxYmEwZWJiNDBmZTBjIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMjczLCJleHAiOjE1ODE3ODg2NzMsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dHJhaW5lcnMiLCJwb3N0OnNlc3Npb25zIl19.bAPqacrHN7gqJzCbS1vEzL5MM-JzMO3S54eXTuwSXYb8DOjkD1hsBORBv2znkpYdHUt8VMD098-qBn-5EjuRyiAyyTXehgWjiBfHqQ_K6OpMiBfbAxe7sPuW4cX07A3j__33vKGkc9KNZrgM_tZnQ9haN5kTj6hJOvNUPhj1AlKY4KnhRaRtXF1r-RGQl7K1-itzlhmpV-x-XBTXLE3CfXtu4bOobB8LY5XtulHhUE_LMvCSTcE1xZg7p4M_8Pw_GnlAeyHaxREO4YWlV6Y8xZQAzHnZu96Hz2GzDRELwVNuJVVOJlNDh47VHnGuJflCm6vSCCk62Fd75StwkZ9NdA'

manager_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRiODA3ZWY5YjEwZjA0ZmM5MzQ4IiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMTAxLCJleHAiOjE1ODE3ODg1MDEsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2xpZW50cyIsImRlbGV0ZTpzZXNzaW9ucyIsImRlbGV0ZTp0cmFpbmVycyIsImdldDpjbGllbnRzIiwiZ2V0OnNlc3Npb25zIiwiZ2V0OnRyYWluZXJzIiwicGF0Y2g6Y2xpZW50cyIsInBhdGNoOnNlc3Npb25zIiwicGF0Y2g6dHJhaW5lcnMiLCJwb3N0OmNsaWVudHMiLCJwb3N0OnNlc3Npb25zIiwicG9zdDp0cmFpbmVycyJdfQ.Pq7nrsXar8Bd-IhjLhv_uUJM7IuMFnpxWyZy1EXjvmS2zC9ZHEr1Mhjoi-HCsvVahlmMJpsQztDd7Ga-jgg382JBnVzEixpRKEgQfjHScKXYcgl0gvTsQ7kydOPL64XnGsxyYnyDbZbRdwKiek5UVEYYpnDfFI3ZSHVA8tmb3QrW5-XsjmZSZo7cD7FzR-5XPVhQUS2SAfG0NXPBhaqlkS8JkRhPGGRwp13u-BCRm46H_bgkidg7Whl7b9JoCqejkfuNXw-BUR6YJrQ1isL86ZI6Qp00jSaWnNdqIfPKLIs3HASSksdulroxsetyCifCi1CokORvCVzXqyFk0QRyUq'
trainer_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRhMGM3ZWY5YjEwZjA0ZmM5MTc1IiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMTkyLCJleHAiOjE1ODE3ODg1OTIsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6c2Vzc2lvbnMiLCJnZXQ6Y2xpZW50cyIsImdldDpzZXNzaW9ucyIsImdldDp0cmFpbmVycyIsInBhdGNoOmNsaWVudHMiLCJwYXRjaDpzZXNzaW9ucyIsInBvc3Q6Y2xpZW50cyIsInBvc3Q6c2Vzc2lvbnMiXX0.xkFevU_xYTZxoJewv9xRTC4wSxT9yvigC0PshXWbHYKW87RqoGkYn3crr37-ynT54uB1xcuQxfIx4aDfbcyVG_hcN48KJxPJlH_Y1fOjwenZcjmM3BBXJl8yJVux8lIVoWxwO_2nFKc5wAJoXM4nuaHqUoPgwS1Y2o7nlvAuEWPCJErs2clBt-zJCSyVxKrNUHhkWuoAvDGJUl8uQX-kZkW4F1JDy9yAsSACnY9lVTnp8rlX0lHA3mEXCyYERiTPpz5NvUbNjHi54Kgq8VuExM5uIcS8HTV2Gh3CW8KWABxv0vttAA52miOfkd-hP30Ajyug8fp3ULTDsniRYHt5ya'
client_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NmRhNDQ2N2YxYmEwZWJiNDBmZTBjIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNzAyMjczLCJleHAiOjE1ODE3ODg2NzMsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dHJhaW5lcnMiLCJwb3N0OnNlc3Npb25zIl19.bAPqacrHN7gqJzCbS1vEzL5MM-JzMO3S54eXTuwSXYb8DOjkD1hsBORBv2znkpYdHUt8VMD098-qBn-5EjuRyiAyyTXehgWjiBfHqQ_K6OpMiBfbAxe7sPuW4cX07A3j__33vKGkc9KNZrgM_tZnQ9haN5kTj6hJOvNUPhj1AlKY4KnhRaRtXF1r-RGQl7K1-itzlhmpV-x-XBTXLE3CfXtu4bOobB8LY5XtulHhUE_LMvCSTcE1xZg7p4M_8Pw_GnlAeyHaxREO4YWlV6Y8xZQAzHnZu96Hz2GzDRELwVNuJVVOJlNDh47VHnGuJflCm6vSCCk62Fd75StwkZ9Nda'


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

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trainers'])

        trainer.delete()

    def test_get_trainers_fail(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)}, json={'age': 75})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        trainer.delete()

    # /////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful POST requests for all trainers
    # /////////////////////////////////////////////////////////////////////
    def test_post_trainers_success(self):
        res = self.client().post('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)}, json={"name": "Mostafa", "gender": "male", "age": 28})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_trainer']['id'])
        self.assertEqual(data['new_trainer']['name'], 'Mostafa')
        self.assertEqual(data['new_trainer']['gender'], 'male')
        self.assertEqual(data['new_trainer']['age'], 28)
    
    def test_post_trainers_fail(self):
        res = self.client().post('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)}, json={"name": "Mostafa", "gender": "male", "age": 28, 'height': 170})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # ///////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all trainers
    # ///////////////////////////////////////////////////////////////////////
    def test_delete_trainers_success(self):
        post_res = self.client().post('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)}, json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/trainers/' + str(post_res_data['new_trainer']['id']), headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_trainer']['id'])
        self.assertEqual(delete_res_data['deleted_trainer']['name'], 'Mostafa')
        self.assertEqual(delete_res_data['deleted_trainer']['gender'], 'male')
        self.assertEqual(delete_res_data['deleted_trainer']['age'], 28)
    
    def test_delete_trainers_fail(self):
        post_res = self.client().post('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)}, json={"name": "Mostafa", "gender": "male", "age": 28})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/trainers/1000', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all trainers
    # //////////////////////////////////////////////////////////////////////
    def test_patch_trainers_success(self):
        post_res = self.client().post('/trainers', json={'name': "Rafiki", "gender": "monkey", "age": 123}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/trainers/' + str(post_res_data['new_trainer']['id']), json={'name': 'Mostafa', 'gender': 'male', 'age': 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_trainer']['id'])
        self.assertEqual(patch_res_data['modified_trainer']['name'], 'Mostafa')
        self.assertEqual(patch_res_data['modified_trainer']['gender'], 'male')
        self.assertEqual(patch_res_data['modified_trainer']['age'], 28)
    
    def test_patch_trainers_fail(self):
        post_res = self.client().post('/trainers', json={'name': "Rafiki", "gender": "monkey", "age": 123}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/trainers/1000', json={'name': 'Mostafa', 'gender': 'male', 'age': 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
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

        res = self.client().get('/clients', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])

        client.delete()

    def test_get_clients_fail(self):
        client = Client(name='Yehia', gender='male', age=102)
        client.insert()

        res = self.client().get('/clients', json={'age': 75}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

        client.delete()

    # ////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful POST requests for all clients
    # ////////////////////////////////////////////////////////////////////
    def test_post_clients_success(self):
        res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_client']['id'])
        self.assertEqual(data['new_client']['name'], 'Mostafa')
        self.assertEqual(data['new_client']['gender'], 'male')
        self.assertEqual(data['new_client']['age'], 28)
    
    def test_post_clients_fail(self):
        res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28, 'height': 170}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all clients
    # //////////////////////////////////////////////////////////////////////
    def test_delete_clients_success(self):
        post_res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/clients/' + str(post_res_data['new_client']['id']), headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_client']['id'])
        self.assertEqual(delete_res_data['deleted_client']['name'], 'Mostafa')
        self.assertEqual(delete_res_data['deleted_client']['gender'], 'male')
        self.assertEqual(delete_res_data['deleted_client']['age'], 28)
    
    def test_delete_clients_fail(self):
        post_res = self.client().post('/clients', json={"name": "Mostafa", "gender": "male", "age": 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/clients/1000', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # /////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all clients
    # /////////////////////////////////////////////////////////////////////
    def test_patch_clients_success(self):
        post_res = self.client().post('/clients', json={'name': "Rafiki", "gender": "monkey", "age": 123}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/clients/' + str(post_res_data['new_client']['id']), json={'name': 'Mostafa', 'gender': 'male', 'age': 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_client']['id'])
        self.assertEqual(patch_res_data['modified_client']['name'], 'Mostafa')
        self.assertEqual(patch_res_data['modified_client']['gender'], 'male')
        self.assertEqual(patch_res_data['modified_client']['age'], 28)
    
    def test_patch_clients_fail(self):
        post_res = self.client().post('/clients', json={'name': "Rafiki", "gender": "monkey", "age": 123}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/clients/1000', json={'name': 'Mostafa', 'gender': 'male', 'age': 28}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
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

        res = self.client().get('/sessions', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
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

        res = self.client().get('/sessions', json={'age': 75}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
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
        res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_session']['id'])
        self.assertEqual(data['new_session']['name'], 'Mostafa-Yehia training session')
        self.assertEqual(data['new_session']['trainer_id'], 1)
        self.assertEqual(data['new_session']['client_id'], 3)
    
    def test_post_sessions_fail(self):
        res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3, 'duration_min': 45}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
    
    # ///////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful DELETE requests for all sessions
    # ///////////////////////////////////////////////////////////////////////
    def test_delete_sessions_success(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/sessions/' + str(post_res_data['new_session']['id']), headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res_data['success'], True)
        self.assertTrue(delete_res_data['deleted_session']['id'])
        self.assertEqual(delete_res_data['deleted_session']['name'], 'Mostafa-Yehia training session')
        self.assertEqual(delete_res_data['deleted_session']['trainer_id'], 1)
        self.assertEqual(delete_res_data['deleted_session']['client_id'], 3)
    
    def test_delete_sessions_fail(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Yehia training session', 'trainer_id': 1, 'client_id': 3}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        delete_res = self.client().delete('/sessions/1000', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        delete_res_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 404)
        self.assertEqual(delete_res_data['success'], False)

    # //////////////////////////////////////////////////////////////////////
    # Tests for successful and un-successful PATCH requests for all sessions
    # //////////////////////////////////////////////////////////////////////
    def test_patch_session_success(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Rafiki training session', 'trainer_id': 1, 'client_id': 3}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/sessions/' + str(post_res_data['new_session']['id']), json={'name': 'Mostafa-Yehia', 'trainer_id': 100, 'client_id': 300}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res_data['success'], True)
        self.assertTrue(patch_res_data['modified_session']['id'])
        self.assertEqual(patch_res_data['modified_session']['name'], 'Mostafa-Yehia')
        self.assertEqual(patch_res_data['modified_session']['trainer_id'], 100)
        self.assertEqual(patch_res_data['modified_session']['client_id'], 300)
    
    def test_patch_session_fail(self):
        post_res = self.client().post('/sessions', json={'name': 'Mostafa-Rafiki training session', 'trainer_id': 1, 'client_id': 3}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        post_res_data = json.loads(post_res.data)

        patch_res = self.client().patch('/sessions/1000' + str(post_res_data['new_session']['id']), json={'name': 'Mostafa-Yehia', 'trainer_id': 100, 'client_id': 300, 'duration_min': 45}, headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        patch_res_data = json.loads(patch_res.data)

        self.assertEqual(patch_res.status_code, 404)
        self.assertEqual(patch_res_data['success'], False)


    # ///////////////////////////////////
    # Tests for role-based access control
    # ///////////////////////////////////

    # //////////////////////////
    # Tests for the manager role
    # //////////////////////////
    def test_manager_get_trainers_success(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trainers'])

        trainer.delete()
    
    def test_manager_get_trainers_fail(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(manager_bad_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        trainer.delete()
    
    # //////////////////////////
    # Tests for the trainer role
    # //////////////////////////
    def test_trainer_get_trainers_success(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(trainer_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trainers'])

        trainer.delete()
    
    def test_trainer_get_trainers_fail(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(trainer_bad_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        trainer.delete()

    # //////////////////////////
    # Tests for the client role
    # //////////////////////////
    def test_client_get_trainers_success(self):
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(client_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trainers'])

        trainer.delete()
    
    def test_client_get_trainers_fail(self):        
        trainer = Trainer(name='Mostafa', gender='male', age=28)
        trainer.insert()

        res = self.client().get('/trainers', headers={'Authorization': 'Bearer {}'.format(client_bad_jwt_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        trainer.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
