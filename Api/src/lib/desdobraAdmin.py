import requests
import json

with open('src/config/config.json', "r") as e:
    config = json.load(e)

urlApi = "https://desdobra-v2.herokuapp.com/api/v2/"

def get_page_coupons(page: int):
    headers = {
        'Authorization': f'{config["token"]}'
    }
    return requests.get(urlApi + "coupon", params={
        "page": page,
        "like": None
    }, headers=headers).json()
    
def get_coupon_info(couponId: int):
    headers = {
        'Authorization': f'{config["token"]}'
    }
    return requests.get(urlApi + f"coupon/{couponId}", headers=headers).json()
