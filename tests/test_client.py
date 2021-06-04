
import base64
import io

from client import IllusiveMooseClient
from PIL import Image

USER_NAME = ""
PWD = ""
BC_API_TOKEN = ""

def quest_example():
    print("Initializing the client, logging in as a guest user...")
    im_client = IllusiveMooseClient()

    product_info = im_client.list_products()[0]
    print("Product info:")
    print(product_info)    

def cart_example():

    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    # Find a product
    product_info = im_client.list_products()[0]
    print("Product info:")
    print(product_info)

    # Add the product to cart
    print(f"Adding product {product_info['id']} to cart")
    im_client.add_to_cart(product_info["id"])

    # List cart
    print(f"Cart contents:")
    print(im_client.list_cart())
    
    print(f"Updating product shipping...")
    im_client.update_shipping(product_info["id"], product_info["delivery_options"][0])

    # List cart
    print(f"Cart contents:")
    print(im_client.list_cart())

    # Remove the product from cart
    print(f"Removing product {product_info['id']} from cart")
    im_client.remove_from_cart(product_id=product_info["id"])

    # List cart again
    print(f"Cart contents:")
    print(im_client.list_cart())

    #print(im_client.get_product(product_id=product_info["id"]))

def product_example():

    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    # Create sample image data
    image_data = io.BytesIO()
    image = Image.new('RGBA', size=(50,50), color=(256,0,0))
    image.save(image_data, 'png')
    base64_img_data = base64.encodebytes( image_data.getvalue() ).decode('utf-8')
    print("Image data:")
    print(base64_img_data)

    # Define product data
    product_data = {
                "product_name": "Test product",
                "product_desc": "Test product description",
                "product_category": 1,
                "delivery_options": [1],
                "product_price": 100,
                "delivery_price": 15,
                "product_hst": 13,
                "product_pst":0,
                "picture_id": base64_img_data,
                "picture1_id":base64_img_data,
                "picture2_id":base64_img_data,
                "picture3_id":base64_img_data
    }

    print("Creating a new product...")
    # Create product capturing the product id
    new_product_id = im_client.create_product(product_data)
    print(f"Created a new product with the id {new_product_id}")

    print("Parameters of the newly created product:")
    # Get info of the product that was just created
    product_info = (im_client.get_product(product_id=new_product_id))
    print(product_info)

    print("Update the newly created product")
    # Update the product info changing the name
    im_client.update_product(new_product_id, product_data={'product_name': 'Test product 2'})

    print("Updated product info:")
    # Get info of the changed product
    product_info = (im_client.get_product(product_id=new_product_id))
    print(product_info)

    print("List of all products belonging to the newly created user:")
    # List products created by the current user
    product_list = (im_client.list_my_products(page=0, num_per_page=10))
    print(product_list)

    print(f"Deleting product {new_product_id}")
    # Delete the newly created product
    im_client.delete_product(product_id=new_product_id)


# print(im_client.list_products( page=10, num_per_page=10, search_text=None, product_category=None, owner_id=None))
# print(im_client.list_products( page=1, num_per_page=10, search_text='test', product_category=None, owner_id=None))
# print(im_client.list_products( page=None, num_per_page=None, search_text=None, product_category=2, owner_id=None))
# print(im_client.list_products( page=None, num_per_page=None, search_text=None, product_category=None, owner_id=4))

def shop_example():

    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    print("Check if the current user already has a shop")
    # check if current user has a shop and delete it if it exists
    my_shop_id = ((im_client.get_current_user_info())["shop_id"])

    if my_shop_id:
        print(f"Current user has a shop with id {my_shop_id}")
        print("Deleting the shop...")
        print(im_client.delete_shop(shop_id=my_shop_id))
    else:
        print("Current suer has no shop")

    # Create sample image data
    image_data = io.BytesIO()
    image = Image.new('RGBA', size=(50,50), color=(256,0,0))
    image.save(image_data, 'png')
    base64_img_data = base64.encodebytes( image_data.getvalue() ).decode('utf-8')
    print("Image data:")
    print(base64_img_data)

    # Define shop data
    shop_data = {
        "shop_name": "Test shop name",
        "shop_desc": "Test shop description",
        "picture_id":base64_img_data,
        "picture1_id":base64_img_data,
        "picture2_id":base64_img_data,
        "picture3_id":base64_img_data,
        "addr1": "400 Kent St W",
        "addr2": "apt 123",
        "city":"Lindsay",
        "zip_code":"K9V 6E3",
        "state":"ON",
        "country":"Canada",
        "hst_gst_number":"",
        "phone_number":"",
        "email":"test@test.ca"
    }

    # create a new shop
    new_shop_id = im_client.create_shop(shop_data)

    # get shop info 
    print("Shop info:")
    shop_info = (im_client.get_shop(new_shop_id))
    print(shop_info)

    # Update the shop name
    im_client.update_shop(new_shop_id, {"shop_name": "Test shop name 2"})

    # get shop info
    print("Shop info:")
    shop_info = (im_client.get_shop(new_shop_id))
    print(shop_info)


#print(im_client.list_shops())

# print(im_client.api_v1_list_my_orders())

# print(im_client.api_v1_list_my_shops_orders())

def purchase_product_example():

    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    print("Removing all items from cart...")
    im_client.remove_all_from_cart()
    product_list = im_client.list_products()
    p_ids = [i for i, p in enumerate(product_list) if p['product_price']<10][0]
    
    print(f"Adding product {product_list[p_ids]['id']} to cart")
    im_client.add_to_cart(product_list[p_ids]["id"])

    crypto_name = 'btc'
    private_key = '92274Yz9Fzz52YPzksopL1yTCgtNhZhxWazYDGMqMnrCzGdgWb8'

    print(f"Purchasing the item {product_list[p_ids]['id']} with {crypto_name} paying via the private key '{private_key}'")
    print("the payment will take aproximatelly 20 minutes on the testnet until there is enough confirmations this should be faster on live blockchain")
    im_client.purchase_products_in_cart_with_crypto(private_key, crypto_name)

    print("There should be a new order now:")
    print(im_client.list_my_orders())

def orders_example():  

    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    print("List or orders made by the current user")
    print(im_client.list_my_orders()['orders'])

    print("List or orders made in current users shop")
    print(im_client.list_my_shops_orders()['orders'])


    if len(im_client.list_my_orders()['orders'])>0:
        order_id = im_client.list_my_orders()['orders'][0]["id"]

        print("Order info:")
        order_info = im_client.get_order(order_id)
        print(order_info)

    if len(im_client.list_my_shops_orders()['orders'])>0:
        
        my_shops_order_id = im_client.list_my_shops_orders()['orders'][0]
        
        print("Irder info:")
        order_info = im_client.get_order(order_id)
        print(order_info)

        print("Changing the order status to shipped")
        im_client.update_order_status(my_shops_order_id, 2)

        print("Order info:")
        order_info = im_client.get_order(order_id)
        print(order_info)

def utility_example():
    print("Initializing the client...")
    im_client = IllusiveMooseClient(user_name=USER_NAME, pwd=PWD, blockcypher_api_token = BC_API_TOKEN)

    print("Available product categories:")
    print(im_client.utility_get_product_categories())
    
    print("Available order statuses:")
    print(im_client.utility_get_order_statuses())

    print("Available shipping options:")
    print(im_client.utility_get_shipping_options())

if __name__ == "__main__":
    # cart_example()
    # shop_example()
    # product_example()
    # orders_example()
    # utility_example()
    # purchase_product_example()
    quest_example()