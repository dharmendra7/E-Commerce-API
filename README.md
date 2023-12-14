# E-Commerce-API

## Index

- [Index](#index)
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Installation](#installation)
- [For client use](#for-client-use)
- [Setup using docker](#setup-using-docker)

### Introduction

- Supports latest version of Python i.e. Python 3.11.1  along with Django 4.2.5 :zap:
- This is a simple E-commerce API built using Django Rest Framework. It allows you to manage customers, orders, and products.

### Prerequisites

| Plugin | *Version*|
| ------ | ------ |
|  pip   | 22.3.1 |
| Python | 3.11  |
| Django | 4.2.5 |

### Features

- Create, retrieve and update customers
- Create, retrieve and update products
- Create, retrieve and update orders with multiple products
- List orders based on products or customer names
- Validations for customer and product names, weight, cumulative order weight, and order date
- Auto-generation of order numbers

### Installation

> ##### 1. Clone repository

```bash
git clone https://github.com/dharmendra7/E-Commerce-API.git
```

> ##### 2. Create virtual environment and activate

```bash
python -m venev your-venv-name
```

- On Windows:
```bash
.\venv\Scripts\activate
```

- On macOS and Linux:
```bash
source venv/bin/activate
```

> ##### 3. Setup The Project

```bash
pip install -r requirements.txt
```

> ##### 4. Apply migrations:

```bash
python manage.py migrate
```

> ##### 6. Start the development server

```bash
python manage.py runserver
```


### API Endpoints

> ### Customers

-   List all customers: GET /api/get-customers/
-   Create a new customer: POST /api/create-customer/
-   Update an existing customer: PUT /api/update-customer/<id>/

> ### Products

-   List all products: GET /api/get-products/
-   Create a new product: POST /api/create-product/

> ### Products

-   List all orders: GET /api/get-orders/
-   Create a new order: POST /api/create-order/
-   Edit an existing order: PUT /api/update-order/<id>/
-   List orders based on products: GET /api/get-order-by-name/?products=Book,Pen
-   List orders based on the customer: GET /api/get-order-by-customer-name/?customer=Sam

Orders:



<br />
