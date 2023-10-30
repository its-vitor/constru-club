from flask import Flask, request, jsonify
from flask_cors import CORS
from src.user import register_user, login, get_user_points, register_coupon, get_coupons_points, get_total_points

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    cpf = data.get('cpf')
    response = register_user(password, name, email, cpf)
    return jsonify(response)

@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    response = login(email, password)
    return jsonify(response)

@app.route('/user/points', methods=['GET'])
def user_points():
    token = request.headers.get('Authorization')
    response = get_user_points(token)
    return jsonify(response)

@app.route('/coupon/register', methods=['POST'])
def coupon_register():
    data = request.get_json()
    token = request.headers.get('Authorization')
    coupon = data.get('coupon')
    response = register_coupon(token, coupon)
    return jsonify(response)

@app.route('/coupons/points', methods=['GET'])
def coupons_points():
    token = request.headers.get('Authorization')
    page = request.args.get('page')
    response = get_coupons_points(token, int(page))
    return jsonify(response)

@app.route('/total/points', methods=['GET'])
def total_points():
    token = request.headers.get('Authorization')
    response = get_total_points(token)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=80)
