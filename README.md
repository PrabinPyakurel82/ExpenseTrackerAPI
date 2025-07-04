# ExpenseIncome API

A Django REST API to manage personal income and expenses — built with JWT authentication, custom permissions, and clean RESTful endpoints.

---

##  Setup Instructions

### Requirements

- Python 3.10+
- Django 4.x
- Django REST Framework
- djangorestframework-simplejwt
- SQLite (default) or PostgreSQL

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/PrabinPyakurel82/ExpenseTrackerAPI.git
cd ExpenseTrackerAPI

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

## API Endpoints
All api endpoints are prefixed with 'api/'

### Authentication Endpoints

| Method | Endpoint              | Description                      | 
|--------|-----------------------|----------------------------------|
| POST   | `/auth/register/`     | Register a new user              |
| POST   | `/auth/login/`        | Login and get JWT tokens         |
| POST   | `/auth/refresh/`      | Refresh your JWT access token    | 

---

### Expense & Income Endpoints

| Method | Endpoint              | Description                            | 
|--------|-----------------------|----------------------------------------|
| GET    | `/expenses/`          | List user's expense/income records     |
| POST   | `/expenses/`          | Create a new expense/income record     | 
| GET    | `/expenses/{id}/`     | Retrieve a specific record             | 
| PUT    | `/expenses/{id}/`     | Update an existing record              | 
| DELETE | `/expenses/{id}/`     | Delete a record                        |

##  Sample API Requests & Responses

---

###  User Registration

**POST** `/api/auth/register/`

```json
{
  "username": "prabin",
  "email": "prabin@example.com",
  "password": "mypassword123"
}
```

**Response**
```json
{
  "message": "User registered successfully"
}
```


### User Login
**POST** `/api/auth/login/`
```json
{
  "username": "prabin",
  "password": "mypassword123"
}
```

**Response**
```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}

```

### Refresh JWT Token
**POST** `/api/auth/refresh/`

```json
{
    "refresh": "your_refresh_token",
}
```

**Response**
```json
{
  
  "access": "your_access_token"
}

```

### CREATE RECORD
**POST** `/api/expenses`

**Headers:**
Authorization: Bearer <access_token>
Content-Type: application/json

**Request:**
```json
{
  "title": "Grocery Shopping",
  "description": "Weekly groceries",
  "amount": 100.00,
  "transaction_type": "debit",
  "tax": 10.00,
  "tax_type": "flat"
}
```

**Response**
```json
{
    "id": 5,
    "title": "Grocery Shopping",
    "description": "Weekly groceries",
    "amount": "100.00",
    "transaction_type": "debit",
    "tax": "10.00",
    "tax_type": "flat",
    "total": 110.0,
    "created_at": "2025-07-04T16:41:25.322120Z",
    "updated_at": "2025-07-04T16:41:25.322141Z"
}


```

### RETRIEVE RECORD
**GET** `/api/expenses`

**Headers:**
Authorization: Bearer <access_token>
Content-Type: application/json

**Response**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "title": "hello",
            "amount": "1000.00",
            "transaction_type": "credit",
            "total": 1100.0,
            "created_at": "2025-07-04T13:43:00.959055Z"
        },
        {
            "id": 5,
            "title": "Grocery Shopping",
            "amount": "100.00",
            "transaction_type": "debit",
            "total": 110.0,
            "created_at": "2025-07-04T16:41:25.322120Z"
        }
    ]
}






