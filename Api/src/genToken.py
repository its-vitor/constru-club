import jwt
import json
from bson import ObjectId
from .database import database

with open("src/config/config.json", "r") as e:
    config = json.load(e)


def generate_token(user_id: str):
    try:
        payload = {
            'sub': user_id
        }
        return jwt.encode(payload, config['key'], algorithm='HS256')
    except Exception as e:
        return str(e)


def validate_token(token):
    try:
        user_id = str(jwt.decode(token, config["key"], algorithms=["HS256"])["sub"])
        if database["construClub"]["accounts"].find_one({"_id": ObjectId(user_id)}):
            return user_id
        else:
            return None
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
    except Exception as e:
        return str(e)