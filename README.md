# Project API Documentation

## User Registration and Token Generation Endpoints

### 1. Create a new user
- Endpoint: `/api/users`
- Role: No role required
- Method: POST
- Purpose: Creates a new user with name, email, and password

### 2. Display current user
- Endpoint: `/api/users/me/`
- Role: Anyone with a valid user token
- Method: GET
- Purpose: Displays only the current user

### 3. Generate access tokens
- Endpoint: `/token/login/`
- Role: Anyone with a valid username and password
- Method: POST
- Purpose: Generates access tokens for other API calls

## Menu Items Endpoints

### 1. List all menu items
- Endpoint: `/api/menu-items`
- Role: Customer, delivery crew
- Method: GET
- Purpose: Lists all menu items (Returns 200 – Ok HTTP status code)

### 2. Access Denied for CRUD operations
- Endpoint: `/api/menu-items`
- Role: Customer, delivery crew
- Method: POST, PUT, PATCH, DELETE
- Purpose: Denies access and returns 403 – Unauthorized HTTP status code

### 3. Get single menu item
- Endpoint: `/api/menu-items/{menuItem}`
- Role: Customer, delivery crew
- Method: GET
- Purpose: Lists a single menu item

### 4. Unauthorized for CRUD operations
- Endpoint: `/api/menu-items/{menuItem}`
- Role: Customer, delivery crew
- Method: POST, PUT, PATCH, DELETE
- Purpose: Returns 403 - Unauthorized

### 5. CRUD operations allowed for Manager
- Endpoint: `/api/menu-items`
- Role: Manager
- Method: GET, POST, PUT, PATCH, DELETE
- Purpose: CRUD operations for menu items

## User Group Management Endpoints

### 1. Get all managers
- Endpoint: `/api/groups/manager/users`
- Role: Manager
- Method: GET
- Purpose: Returns all managers

### 2. Assign user to manager group
- Endpoint: `/api/groups/manager/users`
- Role: Manager
- Method: POST
- Purpose: Assigns the user in the payload to the manager group and returns 201-Created

### 3. Remove user from manager group
- Endpoint: `/api/groups/manager/users/{userId}`
- Role: Manager
- Method: DELETE
- Purpose: Removes a user from the manager group and returns 200 – Success if everything is okay. Returns 404 – Not found if the user is not found.

### 4. Get all delivery crew
- Endpoint: `/api/groups/delivery-crew/users`
- Role: Manager
- Method: GET
- Purpose: Returns all delivery crew

### 5. Assign user to delivery crew group
- Endpoint: `/api/groups/delivery-crew/users`
- Role: Manager
- Method: POST
- Purpose: Assigns the user in the payload to the delivery crew group and returns 201-Created HTTP

### 6. Remove user from delivery crew group
- Endpoint: `/api/groups/delivery-crew/users/{userId}`
- Role: Manager
- Method: DELETE
- Purpose: Removes a user from the delivery crew group and returns 200 – Success if everything is okay. Returns 404 – Not found if the user is not found.

## Cart Management Endpoints

### 1. Get current items in the cart
- Endpoint: `/api/cart/menu-items`
- Role: Customer
- Method: GET
- Purpose: Returns current items in the cart for the current user token

### 2. Add menu item to the cart
- Endpoint: `/api/cart/menu-items`
- Role: Customer
- Method: POST
- Purpose: Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items

### 3. Delete all cart items
- Endpoint: `/api/cart/menu-items`
- Role: Customer
- Method: DELETE
- Purpose: Deletes all menu items created by the current user token

## Order Management Endpoints

### 1. Get all orders by the customer
- Endpoint: `/api/orders`
- Role: Customer
- Method: GET
- Purpose: Returns all orders with order items created by this user

### 2. Create a new order
- Endpoint: `/api/orders`
- Role: Customer
- Method: POST
- Purpose: Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.

### 3. Get items for a specific order
- Endpoint: `/api/orders/{orderId}`
- Role: Customer
- Method: GET
- Purpose: Returns all items for this order id. Displays an appropriate HTTP error status code if the order ID doesn’t belong to the current user.

### 4. Get all orders by all users
- Endpoint: `/api/orders`
- Role: Manager
- Method: GET
- Purpose: Returns all orders with order items by all users

### 5. Update order details
- Endpoint: `/api/orders/{orderId}`
- Role: Manager
- Method: PUT, PATCH
- Purpose: Updates the order. A manager can use this endpoint to set a delivery crew to this order and also update the order status to 0 or 1.

### 6. Delete an order
- Endpoint: `/api/orders/{orderId}`
- Role: Manager
- Method: DELETE
- Purpose: Deletes this order

### 7. Get orders assigned to a delivery crew
- Endpoint: `/api/orders`
- Role: Delivery crew
- Method: GET
- Purpose: Returns all orders with order items assigned to the delivery crew

### 8. Update order status by delivery crew
- Endpoint: `/api/orders/{orderId}`
- Role: Delivery crew
- Method: PATCH
- Purpose: A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.
