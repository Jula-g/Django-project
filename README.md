# Django project

Academic Django project with a REST API for managing products, customers, and orders. It includes token-based authentication
using Django REST Framework and JWT.
It also provides a Swagger UI for easy API exploration.

This project was a part of the Software Engineering course to learn Django, REST API development and postgres.

## Features

- REST API for products, customers, and orders
- Token-based authentication using Django REST Framework and JWT
- Swagger UI for API documentation and testing
- Custom user model with JWT authentication
- Basic CRUD operations for products, customers, and orders

## Selected endpoints

To see detailed information, see Swagger on `/swagger`.

### GET /api/products

Returns a list of products.

Request body: none

Example output body:

```json
[
  {
    "id": 1,
    "name": "Jane Doe",
    "address": "123 Main St, Springfield"
  },
  {
    "id": 2,
    "name": "John Smith",
    "address": "456 Oak St, Shelbyville"
  },
  {
    "id": 3,
    "name": "Alice Johnson",
    "address": "789 Maple Ave, Capital City"
  },
  ...
]
```

### /api/products/\<int:id>

Returns detailed information about a product.

Request body: none

Output body:

```json
{
  "id": 2,
  "name": "Shampoo",
  "price": 10.49,
  "available": true
}
```

Example output body:

```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product Description",
  "price": 19.99,
  "stock": 100
}
```

### POST /api/token/

Creates and returns a token for the user.

Request body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response body:

```json
{
  "refresh": "[...]",
  "access": "[...]"
}
```

Make sure to include access token as Authorization Bearer.

## Running

Requirements: python, pip, postgres

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Running the server

```bash
python SElab4/manage.py runserver
```