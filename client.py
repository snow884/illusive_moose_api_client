import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import blockcypher
import time

SERVER_URL_PROD = "http://0.0.0.0:5000"

SERVER_URL_DEV = "http://0.0.0.0:5000"

MAX_TRANSACTION_WAIT_TIME = 3600
MAX_TRANSACTION_WAIT_STEP = 5*60

class IllusiveMooseClient(object):
    """
    
    """
    def __init__(self, user_name: str=None, pwd: str=None, blockcypher_api_token:str=None, env:str="PROD"):
        """
        http://0.0.0.0:5000/docs#/auth/get_api_v1_auth_token
        """
        if env=="PROD":
            self.url = SERVER_URL_PROD
        elif env=="DEV":
            self.url = SERVER_URL_DEV
        else:
            raise Exception(f"Unknown environment '{env}', expecting either 'PROD' or 'DEV'")

        url = self.url + f"/api_v1/auth/token"
        
        if (not (user_name is None)) and (not (pwd is None)):
            res = requests.get(url, auth=HTTPBasicAuth(user_name, pwd))
            res.raise_for_status()
            self.token = res.json().get("token")
            self.headers = {'Authorization': self.token}
        elif (user_name is None) != (pwd is None):
            raise Exception("Please supply either both parameters user_name and pwd or none of them.")
        else:
            self.headers = {}

        self.blockcypher_api_token = blockcypher_api_token

    def get_current_user_info(self) -> dict:
        """
        http://0.0.0.0:5000/docs#/auth/get_api_v1_auth_current_user_info
        """
        url = self.url + f"/api_v1/auth/current_user_info"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()

        return res.json()

    def add_to_cart(self, product_id: int) -> None:
        """
        http://0.0.0.0:5000/docs#/cart/post_api_v1_add_to_cart__product_id_
        """
        url = self.url + f"/api_v1/add_to_cart/{product_id}"
        res = requests.post(url, headers=self.headers)
        res.raise_for_status()

    def remove_from_cart(self, product_id: int) -> None:
        """
        http://0.0.0.0:5000/docs#/cart/delete_api_v1_remove_from_cart__product_id_
        """
        url = self.url + f"/api_v1/remove_from_cart/{product_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def remove_all_from_cart(self, product_id: int=None) -> None:
        """
        http://0.0.0.0:5000/docs#/cart/delete_api_v1_remove_all_from_cart
        """

        url = self.url + f"/api_v1/remove_all_from_cart"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def get_cart_total_in_crypto(self, crypto_name) -> float:
        """
        http://0.0.0.0:5000/docs#/cart/get_api_v1_get_cart_total_in_crypto__crypto_name_
        """
        url = self.url + f"/api_v1/get_cart_total_in_crypto/{crypto_name}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("crypto_total")

    def list_cart(self) -> dict:
        """
        http://0.0.0.0:5000/docs#/cart/get_api_v1_list_cart
        """

        url = self.url + "/api_v1/list_cart"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("cart_items")

    def update_shipping(self, product_id: int, shipping: int) -> None:
        """
        http://0.0.0.0:5000/docs#/cart/patch_api_v1_update_shipping__product_id___shipping_
        """
        url = self.url + f"/api_v1/update_shipping/{product_id}/{shipping}"
        res = requests.patch(url, headers=self.headers)
        res.raise_for_status()

    def create_product(self, product_data: dict) -> int:
        """
        http://0.0.0.0:5000/docs#/product/patch_api_v1_product__product_id_
        """

        url = self.url + f"/api_v1/product"
        res = requests.put(url, headers=self.headers, json=product_data)
        res.raise_for_status()
        return res.json().get("product_id")

    def get_product(self, product_id: int) -> dict:
        """
        http://0.0.0.0:5000/docs#/product/get_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()

        return res.json()

    def update_product(self, product_id: int, product_data) -> int:
        """
        http://0.0.0.0:5000/docs#/product/patch_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.patch(url, headers=self.headers, json=product_data)
        res.raise_for_status()

        return res.json().get("product_id")

    def delete_product(self, product_id: int) -> None:
        """
        http://0.0.0.0:5000/docs#/product/delete_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def list_products(self, page=None, num_per_page=None, search_text=None, product_category=None, owner_id=None) -> dict:
        """
        http://0.0.0.0:5000/docs#/product/get_api_v1_list_products
        """
        url = self.url + f"/api_v1/list_products"
        res = requests.get(url, params={"page":page, "num_per_page":num_per_page, "search_text":search_text, "product_category":product_category, "owner_id":owner_id}, headers=self.headers)
        res.raise_for_status()
        return res.json().get("products")

    def list_my_products(self, page=None, num_per_page=None) -> dict:
        """
        http://0.0.0.0:5000/docs#/product/get_api_v1_list_my_products
        """
        url = self.url + f"/api_v1/list_my_products"
        res = requests.get(url, params={"page":page, "num_per_page":num_per_page}, headers=self.headers)
        res.raise_for_status()
        return res.json().get("products")

    def create_shop(self, shop_data: dict) -> int:
        """
        http://0.0.0.0:5000/docs#/shop/put_api_v1_shop
        """
        url = self.url + f"/api_v1/shop"
        res = requests.put(url, json=shop_data, headers=self.headers)
        res.raise_for_status()
        return res.json().get("shop_id")

    def get_shop(self, shop_id: int) -> dict:
        """
        http://0.0.0.0:5000/docs#/shop/get_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def update_shop(self, shop_id: int, shop_data: dict) -> None:
        """
        http://0.0.0.0:5000/docs#/shop/patch_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.patch(url, json=shop_data, headers=self.headers)
        res.raise_for_status()

    def delete_shop(self, shop_id: int) -> None:
        """
        http://0.0.0.0:5000/docs#/shop/delete_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def list_shops(self, page=None, num_per_page=None) -> dict:
        """
        http://0.0.0.0:5000/docs#/shop/get_api_v1_list_shops
        """
        url = self.url + f"/api_v1/list_shops"
        res = requests.get(url, params={"page":page, "num_per_page":num_per_page}, headers=self.headers)
        res.raise_for_status()

        return(res.json().get("shops"))

    def get_destination_crypto_address(self, crypto_name) -> str:
        """
        http://0.0.0.0:5000/docs#/cart/get_api_v1_get_destination_crypto_address__crypto_name_
        """
        url = self.url + f"/api_v1/get_destination_crypto_address/{crypto_name}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("pub_address")

    def purchase_products_in_cart_with_crypto(self, private_key, crypto_name) -> int:
        """
        
        """
        if self.blockcypher_api_token is None:
            raise Expection("blockcypher_api_token not spcified when initiating the class")
        
        pub_key_crypto_address = self.get_destination_crypto_address("btc")
        print(pub_key_crypto_address)
        
        send_amount = self.get_cart_total_in_crypto(crypto_name)
        print(send_amount)
        ballance = self.check_crypto_address(pub_key_crypto_address, crypto_name)
        print(ballance)
        
        print(self.list_cart())
        
        my_hash = blockcypher.simple_spend(
            private_key,
            pub_key_crypto_address,
            to_satoshis=int(send_amount*100e6),
            change_address=None,
            privkey_is_compressed=False,
            min_confirmations=6,
            coin_symbol="btc-testnet", 
            api_key=self.blockcypher_api_token
        )

        print(my_hash)

        transaction_processing = True
        time_waited = 0

        while transaction_processing and (MAX_TRANSACTION_WAIT_TIME>time_waited):
            ballance = self.check_crypto_address(pub_key_crypto_address, crypto_name)
            print(send_amount)
            print(ballance)
            if ((send_amount-ballance)>100/100e6):
                transaction_processing = False
            else:
                time.sleep(MAX_TRANSACTION_WAIT_STEP)
                time_waited = time_waited + MAX_TRANSACTION_WAIT_STEP

        if not (MAX_TRANSACTION_WAIT_TIME>time_waited):
            raise Exception("Amount sent but not received at the destination address")

        print(self.send_crypto_transaction(crypto_name))

    def check_crypto_address(self, pub_key_crypto_address, coin_symbol) -> None:
        
        if self.blockcypher_api_token is None:
            raise Expection("blockcypher_api_token not spcified when initiating the class")

        ballance = (
            blockcypher.get_total_balance(
                pub_key_crypto_address,
                coin_symbol='btc-testnet',
                api_key=self.blockcypher_api_token,
            )
        ) / 100e6

        return ballance

    def send_crypto_transaction(self, cryptocurrency_name: str) -> None:
        """
        http://0.0.0.0:5000/docs#/cart/post_api_v1_capture_crypto_transaction__cryptocurrency_name_
        """
        url = self.url + f"/api_v1/capture_crypto_transaction/{cryptocurrency_name}"
        res = requests.post(url, headers=self.headers)
        res.raise_for_status()
        

    def list_my_orders(self, page=None, num_per_page=None) -> dict:
        """
        http://0.0.0.0:5000/docs#/order/get_api_v1_list_my_orders
        """
        url = self.url + f"/api_v1/list_my_orders"
        res = requests.get(url, params={"page":page,"num_per_page":num_per_page}, headers=self.headers)
        res.raise_for_status()
        return(res.json())

    def list_my_shops_orders(self, page=None, num_per_page=None) -> dict:
        """
        http://0.0.0.0:5000/docs#/order/get_api_v1_list_my_shops_orders
        """
        url = self.url + f"/api_v1/list_my_shops_orders"
        res = requests.get(url, params={"page":page,"num_per_page":num_per_page}, headers=self.headers)
        res.raise_for_status()
        return(res.json())

    def get_order(self, order_id: int) -> dict:
        """
        http://0.0.0.0:5000/docs#/order/get_api_v1_order__order_id_
        """
        url = self.url + f"/api_v1/order/{order_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return(res.json())

    def update_order_status(self, order_id: int, new_status: int) -> dict:
        """
        http://0.0.0.0:5000/docs#/order/patch_api_v1_order__order_id__update_status__new_status_
        """
        url = self.url + f"/api_v1/order/{order_id}/update_status/{new_status}"
        res = requests.patch(url, headers=self.headers)
        res.raise_for_status()

    def utility_get_product_categories(self) -> dict:
        """
        http://0.0.0.0:5000/docs#/utility/get_api_v1_utility_product_categories
        """
        url = self.url + f"/api_v1/utility/order_statuses"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return(res.json())

    def utility_get_order_statuses(self) -> dict:
        """
        http://0.0.0.0:5000/docs#/utility/get_api_v1_utility_order_statuses
        """
        url = self.url + f"/api_v1/utility/product_categories"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return(res.json())

    def utility_get_shipping_options(self) -> dict:
        """
        http://0.0.0.0:5000/docs#/utility/get_api_v1_utility_shipping_options
        """
        url = self.url + f"/api_v1/utility/shipping_options"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return(res.json())