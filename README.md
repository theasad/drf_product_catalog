# Product Catalog API

## Installation Guide

### Prerequisites for running the API

* [Python3.8](https://www.python.org/downloads/release/python-3810/)
* [Redis](https://redis.io/)

### 1. Clone the repository

       $ git clone https://github.com/theasad/drf_product_catalog.git

### 2. Create a virtual environment based on Python 3.8 and activate it

### 3. Go to "**drf_product_catalog**" folder and install dependencies

       $ pip install -r requirements.txt # for dependencies
       $ pip install -r requirements_dev.txt # for development dependencies

### 4. Copy the .env.example file to .env and fill in the required values

       $ cp .env.example .env 

### 5. Prepare the database

       $ python manage.py migrate

### 6. Start the development server:

       $ python manage.py runserver

### 7. Start Celery Worker and Beat scheduler:

       $ celery -A apps.core.celeryconf worker -B -l DEBUG -E

## API Documentation

* [API Documentation (Swagger)](http://127.0.0.1:8000/)
* [API Documentation (Redoc)](http://127.0.0.1:8000/redoc)

### API Endpoints

| Endpoint             | Method | Query Params                                                       | Description           |
|----------------------|--------|--------------------------------------------------------------------|-----------------------|
| /products/images     | GET    | 1. product_url (required)<br>2.Size (small,medium,large)<br>3.page | Get product images    |
| /products/images/:id | GET    | 2. Size (small,medium,large)                                       | Retrieve single image |


### Example

---

#### 1. Get product images
```Shell
  curl --location --request GET 'http://127.0.0.1:8000/products/images/?product_url=https%3A%2F%2Fwww.aarong.com%2Fcatalog%2Fproduct%2Fview%2Fid%2F656192%2Fs%2Fyellow-half-silk-jamdani-saree%2Fcategory%2F233%2F&size=small'
```

### API Responses
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 161,
            "image": "http://127.0.0.1:8000/media/__sized__/catalog/product/63/0550000127310-thumbnail-256x341-70.jpg",
            "position": 1,
            "created_at": "2022-05-21T08:01:08.931170Z"
        },
        {
            "id": 160,
            "image": "http://127.0.0.1:8000/media/__sized__/catalog/product/63/0550000127310_1-thumbnail-256x341-70.jpg",
            "position": 2,
            "created_at": "2022-05-21T08:01:08.931137Z"
        },
        {
            "id": 159,
            "image": "http://127.0.0.1:8000/media/__sized__/catalog/product/63/0550000127310_2-thumbnail-256x341-70.jpg",
            "position": 3,
            "created_at": "2022-05-21T08:01:08.931099Z"
        },
        {
            "id": 158,
            "image": "http://127.0.0.1:8000/media/__sized__/catalog/product/63/0550000127310_3-thumbnail-256x341-70.jpg",
            "position": 4,
            "created_at": "2022-05-21T08:01:08.931020Z"
        }
    ]
}
```


### 2. Retrieve single image
```Shell
curl --location --request GET 'http://127.0.0.1:8000/products/images/159/?size=small'
```

### API Response
```json
{
    "id": 159,
    "image": "http://127.0.0.1:8000/media/__sized__/catalog/product/63/0550000127310_2-thumbnail-256x341-70.jpg",
    "position": 3,
    "created_at": "2022-05-21T08:01:08.931099Z"
}
```