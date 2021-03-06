import json
from flask import request, _request_ctx_stack, jsonify, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import base64


AUTH0_DOMAIN = 'ymfsnd.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'gym'
CLIENT_ID = 'xWzOC0Vr7MxNCHqG1RdAQO58n7sjwC5i'
CALLBACK_URI = 'https://ym-fsnd-capstone.herokuapp.com/welcome'
LOGIN_URI = "https://" + AUTH0_DOMAIN + "/authorize?audience=" + API_AUDIENCE + "&response_type=token&client_id=" + CLIENT_ID + "&redirect_uri=" + CALLBACK_URI

## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    try:
        if not auth:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 401)

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

        elif len(parts) == 1:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 401)

        elif len(parts) > 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 401)
    except AuthError as e:
        abort(e.status_code, e.error)

    
    token = parts[1]
    return token


def check_permissions(permission, payload):
    try:
        if permission not in payload['permissions']:
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'User does not have the permission to make the request.'
            }, 401)
        else:
            return True
    except AuthError as e:
        abort(e.status_code, e.error)


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    try:
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )

                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception as e:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
                }, 400)
    except AuthError as e:
        abort(e.status_code, e.error)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
