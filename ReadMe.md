Readme.md

# Illusive Moose python client

This is a python implementation of a client for Illusive Moose API.

Illusive Moose is an online marketplace intended for small Canadian businesses offering a variety of products from different categories. You can find the store here https://shop.illusive-moose.ca/ . You can find the API documentation here https://shop.illusive-moose.ca/docs#/

Illusive Moose supports crypto payments. Right now Bitcoin, Dogecoin, Dash and Litecoin are supported.

## Required credentials

In order to initiate the client you will need two sets of credentials.

```
im_client = IllusiveMooseClient(user_name="my_username", pwd="my_pwd", blockcypher_api_token = 'my_blockcypher_token')
```

### Illusive moose credentials

In order to be able to initiate the client as a logged-in user you will have to visit https://shop.illusive-moose.ca/auth/register and register as a new user. Use the username and password to initiate the client object.

The API allows guest access and this step is only required if you wish to create new products or new shops. 

### Blockcypher credentials

In order to be able to buy items with this client you will have to get a token for blockcypher API

https://www.blockcypher.com/



