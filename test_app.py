import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Trainer, Client, Session


manager_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0MmExOGE2ZjlmM2EwZTRkNDA5YjQwIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNjg3MDIyLCJleHAiOjE1ODE2OTQyMjIsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2xpZW50cyIsImRlbGV0ZTpzZXNzaW9ucyIsImRlbGV0ZTp0cmFpbmVycyIsImdldDpjbGllbnRzIiwiZ2V0OnNlc3Npb25zIiwiZ2V0OnRyYWluZXJzIiwicGF0Y2g6Y2xpZW50cyIsInBhdGNoOnNlc3Npb25zIiwicGF0Y2g6dHJhaW5lcnMiLCJwb3N0OmNsaWVudHMiLCJwb3N0OnNlc3Npb25zIiwicG9zdDp0cmFpbmVycyJdfQ.GdwDQa_AdlD3Thpr6fDlnHm3VCGHPXM4UVwT0zFz7BNyve1HQ8hfocvaheDUcbCuTLAO7Jr6xtc0XxWfjeSi9BLXm7eNpJfaWvOtjuGT6qejTlU8TuBcTzrKX6y-U4ldIgPSv1GwJNnr0qDujY28P2lGt19nKi6_QU-ojaJ65N4B8pdPf1wuOJeXMJLVhsreMrMwyjxxI2f2Ylhq3eiWq3v0cCnHprNhN4dxO5ObjeZdlpI5H5cdQIxBn258wwXS2Ph6cl5xxJYrOizrz1nQd8D4LLKa0cCvxWCUorl-01I-yTJXtjv3O6Y8ZhjD6bcZrdOBCrgq014y9x97GrfDaQ'
trainer_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0Njg2NGU0ZDkxODEwZWI1NDQzZjZjIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNjg5MDg4LCJleHAiOjE1ODE2OTYyODgsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6c2Vzc2lvbnMiLCJnZXQ6Y2xpZW50cyIsImdldDpzZXNzaW9ucyIsImdldDp0cmFpbmVycyIsInBhdGNoOmNsaWVudHMiLCJwYXRjaDpzZXNzaW9ucyIsInBvc3Q6Y2xpZW50cyIsInBvc3Q6c2Vzc2lvbnMiLCJwb3N0OnRyYWluZXJzIl19.iV7OmZvtQYGsEIPxEdEZAysXetbkPnjJb0ulNfdD6cSKgYLm6OcDNU0tcfm7ncNdy3tSaI679BizvH9Jvt6wbaW5_wQhFtkqH8vAqVo3cxbIykGVfzp29Woaq7L35vKzmazISwpz_A0aFlPsFlZH8zyOOX468WRIdj1C5xaHNAWVSXE2DyfkhYNRAj2JHqnkvWIB7ImJq6DCkPFbcfhSWjNyPgA5-GjfJlyBvqb2P6UIP_fD1Sdqlh57_ga8S3ITrMT3WplxW-Xk6PNrU9XCG15PPbXEn2B3TfXUL5hRkvhddiRAXe57OIL8XgLYGh5XEfMIixacodI9wW3dxRj2Fw'
client_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIzMjY3MDgwNDE2NjQzMjUwNzEiLCJhdWQiOlsiZ3ltIiwiaHR0cHM6Ly95bWZzbmQuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MTY4OTQ1NSwiZXhwIjoxNTgxNjk2NjU1LCJhenAiOiJ4V3pPQzBWcjdNeE5DSHFHMVJkQVFPNThuN3Nqd0M1aSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6c2Vzc2lvbnMiLCJnZXQ6dHJhaW5lcnMiXX0.m-4yRuPUYAy-j0KKMfCax9M6PiylB06bgF4v08C5G7V6YsH1sDGtDChxPxyxFPz6FKZrP7_jh0eZQDE3tIoDPifK9MSIZHQzb9rOJK9cJQEczS-E9s1FHo4L3PsFomojL1NMWpvLK-Fj7alRs--y9H2DaxRBqxkOdqjP3jR9vscBnPmKZ8oepX7Sc0-MZDUaGLsuj6vFdzYl9aLiOSO6jEerQBWx6Kt06w92Yh2cZrtVFhakKJ7KmFW20xXvbFk4Ndzf7RmGIh71ecoBoMO0r1QrSnNcSVIRgKLl5W6KHo77tDf1-PFyvT3wBfGYdGI9WL0JAMeIjkS15tRu30Kr4w'

manager_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0MmExOGE2ZjlmM2EwZTRkNDA5YjQwIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNjg3MDIyLCJleHAiOjE1ODE2OTQyMjIsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2xpZW50cyIsImRlbGV0ZTpzZXNzaW9ucyIsImRlbGV0ZTp0cmFpbmVycyIsImdldDpjbGllbnRzIiwiZ2V0OnNlc3Npb25zIiwiZ2V0OnRyYWluZXJzIiwicGF0Y2g6Y2xpZW50cyIsInBhdGNoOnNlc3Npb25zIiwicGF0Y2g6dHJhaW5lcnMiLCJwb3N0OmNsaWVudHMiLCJwb3N0OnNlc3Npb25zIiwicG9zdDp0cmFpbmVycyJdfQ.GdwDQa_AdlD3Thpr6fDlnHm3VCGHPXM4UVwT0zFz7BNyve1HQ8hfocvaheDUcbCuTLAO7Jr6xtc0XxWfjeSi9BLXm7eNpJfaWvOtjuGT6qejTlU8TuBcTzrKX6y-U4ldIgPSv1GwJNnr0qDujY28P2lGt19nKi6_QU-ojaJ65N4B8pdPf1wuOJeXMJLVhsreMrMwyjxxI2f2Ylhq3eiWq3v0cCnHprNhN4dxO5ObjeZdlpI5H5cdQIxBn258wwXS2Ph6cl5xxJYrOizrz1nQd8D4LLKa0cCvxWCUorl-01I-yTJXtjv3O6Y7ZhjD6bcZrdOBCrgq014y9x97GrfDaQ'
trainer_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0Njg2NGU0ZDkxODEwZWI1NDQzZjZjIiwiYXVkIjoiZ3ltIiwiaWF0IjoxNTgxNjg5MDg4LCJleHAiOjE1ODE2OTYyODgsImF6cCI6InhXek9DMFZyN014TkNIcUcxUmRBUU81OG43c2p3QzVpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6c2Vzc2lvbnMiLCJnZXQ6Y2xpZW50cyIsImdldDpzZXNzaW9ucyIsImdldDp0cmFpbmVycyIsInBhdGNoOmNsaWVudHMiLCJwYXRjaDpzZXNzaW9ucyIsInBvc3Q6Y2xpZW50cyIsInBvc3Q6c2Vzc2lvbnMiLCJwb3N0OnRyYWluZXJzIl19.iV7OmZvtQYGsEIPxEdEZAysXetbkPnjJb0ulNfdD6cSKgYLm6OcDNU0tcfm7ncNdy3tSaI679BizvH9Jvt6wbaW5_wQhFtkqH8vAqVo3cxbIykGVfzp29Woaq7L35vKzmazISwpz_A0aFlPsFlZH8zyOOX468WRIdj1C5xaHNAWVSXE2DyfkhYNRAj2JHqnkvWIB7ImJq6DCkPFbcfhSWjNyPgA5-GjfJlyBvqb2P6UIP_fD1Sdqlh57_ga8S3ITrMT3WplxW-Xk6PNrU9XCG15PPbXEn2B3TfXUL5hRkvhddiRAXe57OIL8XgLYGh5XEfMIixAcodI9wW3dxRj2Fw'
client_bad_jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UVXpSVEZETUVJNU1rUkdSakF3TjBGQ01rVTVRVFU0TmpSQk1UZERPRUUxTVRBNU1UaERNZyJ9.eyJpc3MiOiJodHRwczovL3ltZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIzMjY3MDgwNDE2NjQzMjUwNzEiLCJhdWQiOlsiZ3ltIiwiaHR0cHM6Ly95bWZzbmQuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MTY4OTQ1NSwiZXhwIjoxNTgxNjk2NjU1LCJhenAiOiJ4V3pPQzBWcjdNeE5DSHFHMVJkQVFPNThuN3Nqd0M1aSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6c2Vzc2lvbnMiLCJnZXQ6dHJhaW5lcnMiXX0.m-4yRuPUYAy-j0KKMfCax9M6PiylB06bgF4v08C5G7V6YsH1sDGtDChxPxyxFPz6FKZrP7_jh0eZQDE3tIoDPifK9MSIZHQzb9rOJK9cJQEczS-E9s1FHo4L3PsFomojL1NMWpvLK-Fj7alRs--y9H2DaxRBqxkOdqjP3jR9vscBnPmKZ8oepX7Sc0-MZDUaGLsuj6vFdzYl9aLiOSO6jEerQBWx6Kt06w92Yh2cZrtVFhakKJ7KmFW20xXvbFk4Ndzf7RmGIh71ecoBoMO0r1QrSnNcSVIRgKLl5W6KHo77tDf1-PFyvT3wBfGYdGI9WL0JAMeIJkS15tRu30Kr4w'


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
