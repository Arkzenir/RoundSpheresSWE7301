# auth.py
from functools import wraps
from flask import request, jsonify
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
from django.conf import settings

# JWT Configuration
JWT_SECRET_KEY = 'RXCtPwpalYfbqOYWEEvqxsLqxQYZymvQ'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = datetime.timedelta(hours=1)

def generate_token(user_id):
    """Generate a JWT token for a user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + JWT_EXPIRATION_DELTA,
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verify the JWT token and return the token info"""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def decode_token(token):
    """Decode the JWT token - required by Connexion"""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify token
            token_data = verify_token(token)
            if token_data is None:
                return jsonify({'message': 'Token is invalid!'}), 401
            
            # Add user_id to kwargs if needed
            kwargs['user_id'] = token_data['sub']
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

    return decorated

# Authentication routes
def register():
    """Register a new user"""
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Check if user already exists
    if User.objects.filter(username=data['username']).exists():
        return jsonify({'message': 'Username already exists'}), 400
        
    # Create new user
    try:
        user = User.objects.create(
            username=data['username'],
            password=make_password(data['password'])
        )
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

def login():
    """Login user and return JWT token"""
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
        
    # Find user
    user = User.objects.filter(username=data['username']).first()
    
    if user and check_password(data['password'], user.password):
        token = generate_token(user.id)
        return jsonify({
            'token': token,
            'message': 'Login successful'
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401