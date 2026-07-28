TDD Hints and Solutions
This page contains the remaining hints and solutions for the Update, Delete , List all , List By Name, List By Category, List By Availability REST APIs, now that you have implemented Read.

Update
First write a test for the Update function:

python

    def test_update_product(self):
         """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        # send a self.client.post() request to the BASE_URL with a json payload of test_product.serialize()
        # assert that the resp.status_code is status.HTTP_201_CREATED
        # UPDATE THE PRODUCT
        # get the data from resp.get_json() as new_product
        # change new_account["description"] to unknown
        # send a self.client.put() request to the BASE_URL with a json payload of new_product
        # assert that the resp.status_code is status.HTTP_200_OK
        # get the data from resp.get_json() as updated_product
        # assert that the updated_product["description"] is whatever you changed it to
Here is starter code to test update a product:
python

    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        new_product["description"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "unknown")
This is a complete test case for update a product:

Now write the code to make the Update test case pass:

python

######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update an Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    # use the Product.find() method to retrieve the product by the product_id
    # abort() with a status.HTTP_404_NOT_FOUND if it cannot be found
    # call the deserialize() method on the product passing in request.get_json()
    # call product.update() to update the product with the new data
    # return the serialize() version of the product with a return code of status.HTTP_200_OK

    return {product as json + 200}
Here is a starter code for the REST API for update a product:
python

######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK
This is a complete REST API implementation for update a product:
Delete
First write a test for the Delete function:

python

    def test_delete_product(self):
        """It should Delete a Product"""

        # create a list products containing 5 products using the _create_products() method. 
        products = self._create_products(5)
        # call the self.get_product_count() method to retrieve the initial count of products before any deletion
        # assign the first product from the products list to the variable test_product
        # send a self.client.delete() request to the BASE_URL with test_product.id
        # assert that the resp.status_code is status.HTTP_204_NO_CONTENT
        # check if the response data is empty 
        # send a self.client.get request to the same endpoint that was deleted to retrieve the deteled product
        # assert that the resp.status_code is status.HTTP_404_NOT_FOUND to confirm deletion of the product
        # retrieve the count of products after the deletion operation
        # check if the new count of products is one less than the initial count
Here is starter code to test delete a product:
python

    def test_delete_product(self):
        """It should Delete a Product"""
        products = self._create_products(5)
        product_count = self.get_product_count()
        test_product = products[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)
This is a complete test case for delete a product:
Now write the code to make the Delete test case pass:

python

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to Delete a product with id [%s]", product_id)

    # use the Product.find() method to retrieve the product by the product_id
    # if found, call the delete() method on the product
    # return and empty body ("") with a return code of status.HTTP_204_NO_CONTENT

    return {empty string + 204}
Here is starter code for the REST API for delete a product:
python

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to Delete a product with id [%s]", product_id)

    product = Product.find(product_id)
    if product:
        product.delete()

    return "", status.HTTP_204_NO_CONTENT
This is a complete REST API implementation for delete a product:
List All
First write a test for the List All function:

python

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        # send a self.client.get() request to the BASE_URL
        # assert that the resp.status_code is status.HTTP_200_OK
        # get the data from resp.get_json()
        # assert that the len() of the data is 5 (the number of products you created)
Here is starter code to test the list for all products:
python

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)
This is a complete test case for list all products:

Now write the code to make the List All test case pass:

python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    # use the Product.all() method to retrieve all products
    # create a list of serialize() products
    # log the number of products being returned in the list 
    # return the list with a return code of status.HTTP_200_OK

    return {list of products as json here + 200}
Here is starter code for the REST API for list all products:
python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
This is a complete REST API implementation for list all products:
List By Name
First write a test for the List By Name function:

python

    def test_query_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(5)
        # extract the name of the first product in the products list and assigns it to the variable test_name
        # count the number of products in the products list that have the same name as the test_name
        # send an HTTP GET request to the URL specified by the BASE_URL variable, along with a query parameter "name"
        # assert that response status code is 200, indicating a successful request (HTTP 200 OK)
        # retrieve the JSON data from the response
        # assert that the length of the data list (i.e., the number of products returned in the response) is equal to name_count
        # use a for loop to iterate through the products in the data list and checks if each product's name matches the test_name
Here is starter code to test the List By Name function:
python

    def test_query_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(5)
        test_name = products[0].name
        name_count = len([product for product in products if product.name == test_name])
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["name"], test_name)
This is a complete test case for List By Name function:

Note: Please import quote_plus by including the below line in the test_routes.py to ensure the query by name test case passes. Please add it above import app

from urllib.parse import quote_plus

Now write the code to make the List By Name test case pass:

Note: List by name is an extension of List All. You are going to add a filter to the code that lists all products to check if the name parameter has been passed in and filter by name if it is, and return all if it doesn't:

python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    # Initialize an empty list to hold the products.
    # Get the `name` parameter from the request (hint: use `request.args.get()`
    # test to see if you received the "name" query parameter
    # If you did, call the Product.find_by_name(name) method to retrieve products that match the specified name
    # If you didn't call list all
    products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
Here is starter code for the REST API for List By Name function:
python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = []
    name = request.args.get("name")

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
This is a complete REST API implementation for List By Name function:
List By Category
First write a test for the List By Category function:

python

    def test_query_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)
        # retrieves the category of the first product in the products list and assigns it to the variable category
        # create a list named found, containing products from the products list whose category matches the category variable
        # check the count of products match the specified category and assign it to the variable found_count
        # Log a debug message indicating the count and details of the products found
        # send an HTTP GET request to the URL specified by the BASE_URL variable, along with a query parameter "category"
        # assert that response status code is 200, indicating a successful request (HTTP 200 OK)
        # retrieve the JSON data from the response
        # assert that the length of the data list (i.e., the number of products returned in the response) is equal to found_count
        # use a for loop to check each product in the data list and verify that all returned products belong to the queried category
Here is starter code to test the List By Category function:
python

    def test_query_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)
        category = products[0].category
        found = [product for product in products if product.category == category]
        found_count = len(found)
        logging.debug("Found Products [%d] %s", found_count, found)

        # test for available
        response = self.client.get(BASE_URL, query_string=f"category={category.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), found_count)
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["category"], category.name)
This is a complete test case for List By Category function:

Now write the code to make the List By Category test case pass:

Note: List by Category is an extension of List All. You are going to add a filter to the code that lists all products to check if the category parameter has been passed in and filter by category if it is, and return all if it doesn't:

python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = []
    name = request.args.get("name")
    # Get the `category` parameter from the request (hint: use `request.args.get()`

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)

    # test to see if you received the "category" query parameter
    # If you did, convert the category string retrieved from the query parameters to the corresponding enum value from the Category enumeration
    # call the Product.find_by_category(category_value) method to retrieve products that match the specified category_value

    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
Here is starter code for the REST API for List By Category function:
python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = []
    name = request.args.get("name")
    category = request.args.get("category")

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Find by category: %s", category)
        # create enum from string
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
This is a complete REST API implementation for List By Category function:
Note: Please import Category from service.models by including the below line in the routes.py to ensure the query by category test case passes.

from service.models import Product, Category

List By Availability
First write a test for the List By Availability function:

python

    def test_query_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(10)
        # list named available_products is initialized to store the products based on their availability status
        # store the  count of available products.
        # Log a debug message indicating the count and details of the available products
        # send an HTTP GET request to the URL specified by the BASE_URL variable, along with a query parameter "available" set to true.
        # assert that response status code is 200, indicating a successful request (HTTP 200 OK)
        # retrieve the JSON data from the response
        # assert that the length of the data list (i.e., the number of products returned in the response) is equal to available_count
        # use a for loop to check each product in the data list and verify that the "available" attribute of each product is set to True
Here is starter code to test the List By Availability function:
python

    def test_query_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(10)
        available_products = [product for product in products if product.available is True]
        available_count = len(available_products)        
        # test for available
        response = self.client.get(
            BASE_URL, query_string="available=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["available"], True)
This is a complete test case for List By Availability function:

Now write the code to make the List By Availability test case pass:

Note: List by Availability is an extension of List All. You are going to add a filter to the code that lists all products to check if the available parameter has been passed in and filter by available if it is, and return all if it doesn't:

python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    # Get the `available` parameter from the request (hint: use `request.args.get()`

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Find by category: %s", category)
        # create enum from string
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)

    # test to see if you received the "available" query parameter
    # If you did, convert the available string retrieved from the query parameters to a boolean value
    # call the Product.find_by_availability(available_value) method to retrieve products that match the specified available_value
    # otherwise list all products

    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
Here is starter code for the REST API for List By Availability function:
python

######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")

    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Find by category: %s", category)
        # create enum from string
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        app.logger.info("Find by available: %s", available)
        # create bool from string
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        app.logger.info("Find all")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
This is a complete REST API implementation for List By Availability function: