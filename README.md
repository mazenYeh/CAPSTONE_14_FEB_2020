# Capstone Project

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3.7/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Local Database Setup for Testing

With Postgres running, create a new database called 'gym_service_test'.

```bash
createdb gym_service_test
```

This newly created database will be used for testing purposes.

## Testing

To run the tests,

1. Make sure you created a Postgres database named 'gym_service_test' from the previous section
2. In a terminal, navigate to the project directory and run the command,

```
python3 test_app.py
```

## Endpoints

### Trainer Related Endpoints

=> GET '/trainers'
- Description: fetches a json object containing a list of trainers
- Request arguments: None
- Response example,
    {
    "trainers": [{
        "name": "Mostafa",
        "gender": "male",
        "age": 28
    },
    {
        "name": "Zaki",
        "gender": "male",
        "age": 22
    }], 
    "success": true
    }

=> POST '/trainers' (adding a new trainer)
- Description: adds a trainer to the Trainers' table in the database
- Request arguments: a json object containing the new trainer's name, gender, and age, example,
    {
        "name": "Mostafa",
        "gender": "male",
        "age": 28
    }
- Response example,
    {
        "new_trainer": {
            "id": 23
            "name": "Mostafa",
            "gender": "male",
            "age": 28
    }, 
    "success": true
    }

=> PATCH '/trainers/<id>' (modifying an existing trainer)
- Description: modifies an existing trainer in the Trainers' table in the database
- Request arguments: a json object containing the modified trainer's name, gender, and/or age, example,

- Old trainer table entry to be modified
    {
        "id": <id>
        "name": "Mostafa",
        "gender": "male",
        "age": 28
    }
- Request example,
    {
        "name": "Mahmoud"
    }
- Response example,
    {
        "modified_trainer": {
            "id": <id>
            "name": "Mahmoud",
            "gender": "male",
            "age": 28
    }, 
    "success": true
    }

=> DELETE '/trainers/<id>' (deleting an existing trainer)
- Description: adds a trainer to the Trainers' table in the database
- Request arguments: None
- Response example,
    {
        "deleted_trainer": {
            "id": <id>
            "name": "Mostafa",
            "gender": "male",
            "age": 28
    }, 
    "success": true
    }

### Client Related Endpoints

=> GET '/clients'
- Description: fetches a json object containing a list of clients
- Request arguments: None
- Response example,
    {
    "clients": [{
        "name": "Mostafa",
        "gender": "male",
        "age": 28
    },
    {
        "name": "Zaki",
        "gender": "male",
        "age": 22
    }], 
    "success": true
    }

=> POST '/clients' (adding a new client)
- Description: adds a client to the Clients' table in the database
- Request arguments: a json object containing the new client's name, gender, and age, example,
    {
        "name": "Zaki",
        "gender": "male",
        "age": 35
    }
- Response example,
    {
        "new_client": {
            "id": 90
            "name": "Mostafa",
            "gender": "male",
            "age": 35
    }, 
    "success": true
    }

=> PATCH '/clients/<id>' (modifying an existing client)
- Description: modifies an existing client in the clients' table in the database
- Request arguments: a json object containing the modified client's name, gender, and/or age, example,

- Old client table entry to be modified
    {
        "id": <id>
        "name": "Mostafa",
        "gender": "male",
        "age": 28
    }
- Request example,
    {
        "name": "Mahmoud"
    }
- Response example,
    {
        "modified_client": {
            "id": <id>
            "name": "Mahmoud",
            "gender": "male",
            "age": 28
    }, 
    "success": true
    }

=> DELETE '/clients/<id>' (deleting an existing client)
- Description: adds a client to the Clients' table in the database
- Request arguments: None
- Response example,
    {
        "deleted_client": {
            "id": <id>
            "name": "Zaki",
            "gender": "male",
            "age": 28
    }, 
    "success": true
    }

### Session Related Endpoints

=> GET '/sessions'
- Description: fetches a json object containing a list of sessions
- Request arguments: None
- Response example,
    {
    "sessions": [{
        "name": "Mostafa-Yehia training sessions",
        "trainer_id": 1,
        "client_id": 3
    },
    {
        "name": "Zaki-Amr training sessions",
        "trainer_id": 2,
        "client_id": 40
    }], 
    "success": true
    }

=> POST '/sessions' (adding a new session)
- Description: adds a session to the sessions' table in the database
- Request arguments: a json object containing the new session's name, trainer_id, and client_id, example,
    {
        "name": "Mostafa-Yehia training sessions",
        "trainer_id": 1,
        "client_id": 3
    }
- Response example,
    {
        "new_session": {
            "id": 4
            "name": "Mostafa-Yehia training sessions",
            trainer_id": 1,
            "client_id": 3
    }, 
    "success": true
    }

=> PATCH '/sessions/<id>' (modifying an existing session)
- Description: modifies an existing session in the sessions' table in the database
- Request arguments: a json object containing the modified session's name, gender, and/or age, example,

- Old session table entry to be modified
    {
        "id": <id>
        "name": "Mostafa-Zaki training session",
        "trainer_id": 34,
        "client_id": 28
    }
- Request example,
    {
        "name": "Mahmoud-Zaki training session"
    }
- Response example,
    {
        "modified_session": {
            "id": <id>
            "name": "Mahmoud-Zaki training session",
            "trainer_id": 34,
            "client_id": 28
    }, 
    "success": true
    }

=> DELETE '/sessions/<id>' (deleting an existing session)
- Description: adds a session to the Sessions' table in the database
- Request arguments: None
- Response example,
    {
        "deleted_session": {
            "id": <id>
            "name": "Mahmoud-Zaki training session",
            "trainer_id": 34,
            "client_id": 28
    }, 
    "success": true
    }

## URL
https://ym-fsnd-capstone.herokuapp.com/

## Auth0 Credentials

### Manager

- email: gym.manager.fsnd.ym@gmail.com
- password: Opop.123
- Permissions,
1. get:trainers
2. post:trainers
3. patch:trainers
4. delete:trainers
5. get:clients
6. post:clients
7. patch:clients
8. delete:clients
9. get:sessions
10. post:sessions
11. patch:sessions
12. delete:sessions


### Trainer

- email: gym.trainer.fsnd.ym@gmail.com
- password: Opop.123
- Permissions,
1. get:trainers
2. get:clients
3. post:clients
4. patch:clients
5. get:sessions
6. post:sessions
7. patch:sessions
8. delete:sessions

### Client

- email: gym.client.fsnd.ym@gmail.com
- password: Opop.123
- Permissions,
1. get:trainers
2. get:sessions