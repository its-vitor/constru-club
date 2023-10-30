from .database import database
from email_validator import validate_email, EmailNotValidError
from bcrypt import checkpw, hashpw, gensalt
from .genToken import generate_token, validate_token
from bson import ObjectId
from .lib.desdobraAdmin import get_coupon_info, get_page_coupons


def register_user(password: str, name: str, email: str, cpf: str):
    try:
        user_id = str(
            database["construClub"]["accounts"]
            .insert_one(
                {
                    "email": validate_email(
                        email, check_deliverability=False
                    ).normalized,
                    "password": hashpw(password.encode("utf-8"), gensalt()),
                    "cpf": cpf,
                    "name": name.upper(),
                    "totalPoints": 0,
                    "coupons": [],
                }
            )
            .inserted_id
        )
        return {
            "user_id": user_id,
            "token": generate_token(user_id),
        }
    except EmailNotValidError as e:
        return {"apiStatus": 405, "apiMessage": "Endereço de email inválido."}
    except Exception as e:
        return {"apiStatus": 500, "apiMessage": "Ops!", "service": str(e)}


def login(email: str, password: str):
    try:
        user = database["construClub"]["accounts"].find_one({"email": email})
        if user and checkpw(password.encode("utf-8"), user["password"]):
            user_id = str(user["_id"])
            return {
                "user_id": user_id,
                "token": generate_token(user_id),
            }
        else:
            return {"apiStatus": 401, "apiMessage": "Credenciais inválidas."}
    except Exception as e:
        return {"apiStatus": 500, "apiMessage": "Ops!", "service": str(e)}


def get_user_points(token: str):
    user_id = validate_token(token)
    if user_id:
        user_data = database["construClub"]["accounts"].find_one(
            {"_id": ObjectId(user_id)}
        )
        if user_data and "totalPoints" in user_data:
            return {"apiStatus": 200, "totalPoints": user_data["totalPoints"]}
        else:
            return {
                "apiStatus": 404,
                "apiMessage": "Total de pontos do usuário não encontrado.",
            }
    else:
        return {"apiStatus": 401, "apiMessage": "Token inválido. Por favor, faça login e tente novamente."}


def register_coupon(token: str, coupon: str):
    user_id = validate_token(token)
    if user_id:
        if not database["construClub"]["coupons"].find_one({"coupon": coupon.upper()}):
            coupon_data = {"coupon": coupon.upper(), "userId": ObjectId(user_id)}
            database["construClub"]["coupons"].insert_one(coupon_data)
            return {"apiStatus": 200, "apiMessage": "Cupom registrado com sucesso."}
        else:
            return {
                "apiStatus": 400,
                "apiMessage": "Cupom já registrado por outro usuário.",
            }
    else:
        return {"apiStatus": 401, "apiMessage": "Token inválido. Por favor, faça login e tente novamente."}


def get_coupons_points(token, page: int):
    user_id = validate_token(token)
    user_coupons = []
    for coupon in database["construClub"]["coupons"].find(
        {"userId": ObjectId(user_id)}
    ):
        user_coupons.append(coupon["coupon"])

    items = get_page_coupons(page)["items"]
    total_points = 0

    for item in items:
        if item["code"] in user_coupons:
            for coupon_info in get_coupon_info(item["id"]):
                order_id = coupon_info["request"]["id"]
                coupon_data = database["construClub"]["coupons"].find_one(
                    {"userId": ObjectId(user_id), "coupon": item["code"]}
                )
                if coupon_data and "orders" in coupon_data:
                    orders = coupon_data["orders"]
                    if order_id not in orders:
                        points = float(coupon_info["coupon"]["value"]) // 2
                        total_points += points
                        orders.append(order_id)
                        database["construClub"]["coupons"].update_one(
                            {"userId": ObjectId(user_id), "coupon": item["code"]},
                            {"$set": {"orders": orders}},
                        )
                    else:
                        pass

    user_data = database["construClub"]["accounts"].find_one({"_id": ObjectId(user_id)})
    if "totalPoints" in user_data:
        current_points = user_data["totalPoints"]
        if current_points <= total_points:
            database["construClub"]["accounts"].update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"totalPoints": current_points + total_points}},
            )

    return {"apiStatus": 200, "totalPoints": total_points, "coupons": user_coupons}

def get_total_points(token):
    user_id = validate_token(token)
    if user_id:
        user_data = database["construClub"]["accounts"].find_one({"_id": ObjectId(user_id)})
        if user_data and "totalPoints" in user_data:
            return {"apiStatus": 200, "totalPoints": user_data["totalPoints"]}
        else:
            return {"apiStatus": 400, "totalPoints": 0}
    else:
        return {"apiStatus": 401, "apiMessage": "Token inválido. Por favor, faça login e tente novamente."}