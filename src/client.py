import base64
import json
import time

import blockcypher
import requests
from requests.auth import HTTPBasicAuth

SERVER_URL_PROD = "https://shop.illusive-moose.ca"
SERVER_URL_DEV = (
    "http://illusivemoosedev4-env.eba-3tc32p7e.us-east-1.elasticbeanstalk.com"
)
MAX_TRANSACTION_WAIT_TIME = 3600
MAX_TRANSACTION_WAIT_STEP = 5 * 60


class IllusiveMooseClient(object):
    """
    Client class for the website https://shop.illusive-moose.ca
    """

    def __init__(
        self,
        illusive_moose_api_token: str = None,
        blockcypher_api_token: str = None,
        env: str = "PROD",
    ):
        """
        Initiate the clinet and test the connection

        Args:
            illusive_moose_api_token [str] - API key for the website illusive moose,
                to get the token you first need to register here https://shop.illusive-moose.ca/auth/register
                then log in here https://shop.illusive-moose.ca/auth/login and then visit
                https://shop.illusive-moose.ca/api_v1/auth/token
            blockcypher_api_token [str] - API clinet for the blockcypher website
            env [str] - environment, can be iether 'DEV' or 'PROD'
        """
        if env == "PROD":
            self.url = SERVER_URL_PROD
        elif env == "DEV":
            self.url = SERVER_URL_DEV
        else:
            raise Exception(
                f"Unknown environment '{env}', expecting either 'PROD' or 'DEV'"
            )

        self.env = env

        url = self.url + f"/api_v1/ping"

        if not (illusive_moose_api_token is None):
            self.headers = {"Authorization": illusive_moose_api_token}
            self.ping()
        elif (user_name is None) != (pwd is None):
            raise Exception(
                "Please supply either both parameters user_name and pwd or none of them."
            )
        else:
            self.headers = {}

        self.blockcypher_api_token = blockcypher_api_token

    def ping(self) -> None:
        """
        Test the connection to server

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/test/ping
        """
        url = self.url + f"/api_v1/ping"
        res = requests.get(url, headers=self.headers)
        assert res.text == "pong", "API connectivity cannot be verified"

    def get_current_user_info(self) -> dict:
        """
        Get information associated with thecurrent user

        Returns:
            dictionary representing the current user information

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/auth/get_api_v1_auth_current_user_info
        """
        url = self.url + f"/api_v1/auth/current_user_info"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()

        return res.json()

    def add_to_cart(self, product_id: int) -> None:
        """
        Add a new item to the shopping cart

        Args:
            product_id [str] - The ID of the product you with to add to the shopping cart

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/post_api_v1_add_to_cart__product_id_
        """
        url = self.url + f"/api_v1/add_to_cart/{product_id}"
        res = requests.post(url, headers=self.headers)
        res.raise_for_status()

    def remove_from_cart(self, product_id: int) -> None:
        """
        Remove and item from the shopping cart

        Args:
            product_id [str] - The ID of the product you want to remove from the shoping cart

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/post_api_v1_add_to_cart__product_id_
        """
        url = self.url + f"/api_v1/remove_from_cart/{product_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def remove_all_from_cart(self) -> None:
        """
        Remove all items

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/delete_api_v1_remove_all_from_cart
        """

        url = self.url + f"/api_v1/remove_all_from_cart"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def get_cart_total_in_crypto(self, crypto_name: str) -> float:
        """
        Get the total to be paid for items in the shopping cart in the selected
        cryptocorrency.

        Args:
            crypto_name [str] - The smbol for the cryptocurrency you wish to get the
                total for

        Returns:
            Cart total

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/get_api_v1_get_cart_total_in_crypto__crypto_name_
        """
        url = self.url + f"/api_v1/get_cart_total_in_crypto/{crypto_name}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("crypto_total")

    def list_cart(self) -> dict:
        """
        List all items in the shopping cart

        Returns:
            dictionary representing the shopping cart contents

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/get_api_v1_list_cart
        """

        url = self.url + "/api_v1/list_cart"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("cart_items")

    def update_shipping(self, product_id: int, shipping: int) -> None:
        """
        Update the shipping for an item in the shopping cart

        Args:
            product_id [int] - The ID of the product you wish to modify the shipping for
            shipping [int] - The number of the shipping method you wish to assign to the items

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/patch_api_v1_update_shipping__product_id___shipping_
        """
        url = self.url + f"/api_v1/update_shipping/{product_id}/{shipping}"
        res = requests.patch(url, headers=self.headers)
        res.raise_for_status()

    def create_product(self, product_data: dict) -> int:
        """
        Create a new product under your shop

        Args:
            product_data [dict] - The patameters of the new product you wish to add

        Returns:
            The id of the newly created product

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/patch_api_v1_product__product_id_
        """

        url = self.url + f"/api_v1/product"
        res = requests.put(url, headers=self.headers, json=product_data)
        res.raise_for_status()
        return res.json().get("product_id")

    def get_product(self, product_id: int) -> dict:
        """
        Get product info

        Args:
            product_id [int] - The id of the product you want to display the info for

        Returns:
            dictionary containing the product details

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/get_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()

        return res.json()

    def update_product(self, product_id: int, product_data) -> int:
        """
        Get product info

        Args:
            product_id [int] - The id of the product you want to display the info for

        Returns:
            id of the updated product

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/patch_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.patch(url, headers=self.headers, json=product_data)
        res.raise_for_status()

        return res.json().get("product_id")

    def delete_product(self, product_id: int) -> None:
        """
        Delete product belonging to your shop

        Args:
            product_id [int] - The ID of the product you wish to delete

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/delete_api_v1_product__product_id_
        """
        url = self.url + f"/api_v1/product/{product_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def list_products(
        self,
        page=None,
        num_per_page=None,
        search_text=None,
        product_category=None,
        owner_id=None,
    ) -> dict:
        """
        List products by either searcihing by text, category or owner id

        Args:
            page [int] - page number of the product results
            num_per_page [int] - the number of product per page
            search_text [str] - text to search for
            product_category [int] - product category to search for
            owner_id [int] - the owner to display product for

        Returns:
            list containing the information of all products listed

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/get_api_v1_list_products
        """
        url = self.url + f"/api_v1/list_products"
        res = requests.get(
            url,
            params={
                "page": page,
                "num_per_page": num_per_page,
                "search_text": search_text,
                "product_category": product_category,
                "owner_id": owner_id,
            },
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json().get("products")

    def list_my_products(self, page=None, num_per_page=None) -> dict:
        """
        List products in my shop

        Args:
            page [int] - page number of the product results
            num_per_page [int] - the number of product per page

        Returns:
            list of products sold by the shop owned by current user

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/product/get_api_v1_list_my_products
        """
        url = self.url + f"/api_v1/list_my_products"
        res = requests.get(
            url,
            params={"page": page, "num_per_page": num_per_page},
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json().get("products")

    def create_shop(self, shop_data: dict) -> int:
        """
        Create new shop

        Args:
            shop_data [dict] - properties of the new store you wish to create

        Returns:
            the id of the newly created shop

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/shop/put_api_v1_shop
        """
        url = self.url + f"/api_v1/shop"
        res = requests.put(url, json=shop_data, headers=self.headers)
        res.raise_for_status()
        return res.json().get("shop_id")

    def get_shop(self, shop_id: int) -> dict:
        """
        Get shop info

        Args:
            shop_id [int] - the ID of the shop to display

        Returns:
            dict containing shop info

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/shop/get_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def update_shop(self, shop_id: int, shop_data: dict) -> None:
        """
        Update shop info

        Args:
            shop_id [int] - the ID of the shop you vish to update
            shop_data [dict] - the properties you wish to update

        Returns:
            THe id of the updated shop

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/shop/patch_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.patch(url, json=shop_data, headers=self.headers)
        res.raise_for_status()

    def delete_shop(self, shop_id: int) -> None:
        """
        Delete the shop belonging to current user as well as all created products

        Args:
            shop_id [int] - the ID of the shop you vish to delete

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/shop/delete_api_v1_shop__shop_id_
        """
        url = self.url + f"/api_v1/shop/{shop_id}"
        res = requests.delete(url, headers=self.headers)
        res.raise_for_status()

    def list_shops(self, page: int = None, num_per_page: int = None) -> dict:
        """
        List all shops

        Args:
            page [int] - page number of the product results
            num_per_page [int] - the number of product per page

        Returns:
            Paginated list of shops

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/shop/get_api_v1_list_shops
        """
        url = self.url + f"/api_v1/list_shops"
        res = requests.get(
            url,
            params={"page": page, "num_per_page": num_per_page},
            headers=self.headers,
        )
        res.raise_for_status()

        return res.json().get("shops")

    def get_destination_crypto_address(self, crypto_name: str = "btc") -> str:
        """
        List all shops

        Args:
            crypto_name [str] - the symbol of the cryptocurrency to get
                the address for

        Returns:
            Crypto address to be used for payment for the current shopping cart

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/get_api_v1_get_destination_crypto_address__crypto_name_
        """
        url = (
            self.url + f"/api_v1/get_destination_crypto_address/{crypto_name}"
        )
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json().get("pub_address")

    def purchase_products_in_cart_with_crypto(
        self, private_key: str, crypto_name: str = "btc"
    ) -> int:
        """
        List all shops

        Args:
            private_key [str] - The private key to use in the transaction, note that this value
                is only used locally
            crypto_name [str] - the symbol of the cryptocurrency to use in payment

        Returns:
            paginated list of shops

        API enpoint Swagger doc:
            http://0.0.0.0:5000/docs#/cart/get_api_v1_get_destination_crypto_address__crypto_name_
        """
        if self.blockcypher_api_token is None:
            raise Expection(
                "blockcypher_api_token not spcified when initiating the class"
            )

        pub_key_crypto_address = self.get_destination_crypto_address(
            crypto_name
        )

        send_amount = self.get_cart_total_in_crypto(crypto_name)

        ballance = self.check_crypto_address(
            pub_key_crypto_address, crypto_name
        )

        my_hash = blockcypher.simple_spend(
            private_key,
            pub_key_crypto_address,
            to_satoshis=int(send_amount * 100e6),
            change_address=None,
            privkey_is_compressed=False,
            min_confirmations=6,
            coin_symbol="btc-testnet" if self.env == "DEV" else crypto_name,
            api_key=self.blockcypher_api_token,
        )

        transaction_processing = True
        time_waited = 0

        while transaction_processing and (
            MAX_TRANSACTION_WAIT_TIME > time_waited
        ):
            ballance = self.check_crypto_address(
                pub_key_crypto_address, crypto_name
            )
            if (send_amount - ballance) > 100 / 100e6:
                transaction_processing = False
            else:
                time.sleep(MAX_TRANSACTION_WAIT_STEP)
                time_waited = time_waited + MAX_TRANSACTION_WAIT_STEP

        if not (MAX_TRANSACTION_WAIT_TIME > time_waited):
            raise Exception(
                "Amount sent but not received at the destination address"
            )

        return self.send_crypto_transaction(crypto_name)

    def check_crypto_address(self, pub_key_crypto_address, coin_symbol) -> int:
        """
        Check the ballance on a specific publick crypto address

        Args:
            pub_key_crypto_address [str] - the address you wish to check
            coin_symbol [str] - the cryptocurrency the address belongs to

        Returns:
            bannalnce in satoshis or in 1/100e6 units
        """
        if self.blockcypher_api_token is None:
            raise Expection(
                "blockcypher_api_token not spcified when initiating the class"
            )

        ballance = (
            blockcypher.get_total_balance(
                pub_key_crypto_address,
                coin_symbol="btc-testnet",
                api_key=self.blockcypher_api_token,
            )
        ) / 100e6

        return ballance

    def send_crypto_transaction(self, cryptocurrency_name: str) -> None:
        """
        Indicate that crypto funds have beed sent to the destination address

        Args:
            cryptocurrency_name [str] - the symbol of the cryptocurrency used in payment

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/cart/post_api_v1_capture_crypto_transaction__cryptocurrency_name_
        """
        url = (
            self.url
            + f"/api_v1/capture_crypto_transaction/{cryptocurrency_name}"
        )
        res = requests.post(url, headers=self.headers)
        res.raise_for_status()

    def list_my_orders(self, page=None, num_per_page=None) -> dict:
        """
        List all previous orders made by the current user

        Args:
            page [int] - page number of the order results
            num_per_page [int] - the number of order per page

        Returns:
            Paginated list of orders

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/order/get_api_v1_list_my_orders
        """
        url = self.url + f"/api_v1/list_my_orders"
        res = requests.get(
            url,
            params={"page": page, "num_per_page": num_per_page},
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()

    def list_my_shops_orders(self, page=None, num_per_page=None) -> dict:
        """
        List all previous orders for the current users shop

        Args:
            page [int] - page number of the order results
            num_per_page [int] - the number of order per page

        Returns:
            Paginated list of orders

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/order/get_api_v1_list_my_shops_orders
        """
        url = self.url + f"/api_v1/list_my_shops_orders"
        res = requests.get(
            url,
            params={"page": page, "num_per_page": num_per_page},
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()

    def get_order(self, order_id: int) -> dict:
        """
        Get information of a single order

        Args:
            order_id [int] - id of the order you want to get info for

        Returns:
            Dict containing the order information

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/order/get_api_v1_order__order_id_
        """
        url = self.url + f"/api_v1/order/{order_id}"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def update_order_status(self, order_id: int, new_status: int) -> None:
        """
        Update order status

        Args:
            order_id [int] - id of the order you with to update
            new_status [int] - new status you wish to assign to the order

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/order/patch_api_v1_order__order_id__update_status__new_status_
        """
        url = self.url + f"/api_v1/order/{order_id}/update_status/{new_status}"
        res = requests.patch(url, headers=self.headers)
        res.raise_for_status()

    def utility_get_product_categories(self) -> dict:
        """
        Get a list of all possible product category values

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/utility/get_api_v1_utility_product_categories
        """
        url = self.url + f"/api_v1/utility/order_statuses"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def utility_get_order_statuses(self) -> dict:
        """
        Get a list of all possible order statuses

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/utility/get_api_v1_utility_order_statuses
        """
        url = self.url + f"/api_v1/utility/product_categories"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()

    def utility_get_shipping_options(self) -> dict:
        """
        Get a list of all possible shipping options

        API enpoint Swagger doc:
            https://shop.illusive-moose.ca/docs#/utility/get_api_v1_utility_shipping_options
        """
        url = self.url + f"/api_v1/utility/shipping_options"
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res.json()
