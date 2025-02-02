# FAQ Translation API

A Django-based API that provides FAQ management functionality with automatic translations and caching. This API allows you to manage FAQs in multiple languages, supporting CRUD operations and automatic translation of both questions and answers using the `googletrans` library. The translations are cached in Redis for better performance.

---

## Installation

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.8+
- Django 3.x or higher
- Redis (for caching)
- pip (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Pavan8421/bharat-fd
   cd bharat-fd
   ```

# API Setup and Documentation

## Setup Instructions

### 1. Create a virtual environment
```bash
python -m venv venv
```

### 2. Activate the virtual environment
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Redis (if not already installed)
You will need Redis running on your system for caching. To install Redis:
- On macOS, use Homebrew:
```bash
brew install redis
```
- On Ubuntu:
```bash
sudo apt-get install redis-server
```

Start Redis:
```bash
redis-server
```

### 5. Setup your database
Run the following commands to apply the migrations:
```bash
python manage.py migrate
```

### 6. Create a superuser (optional)
If you want to create an admin user for the Django admin interface:
```bash
python manage.py createsuperuser
```

## API Usage

The API provides endpoints to manage FAQs in different languages and perform CRUD operations.

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. GET /faqs/
List all FAQs. You can filter FAQs by language using the `lang` query parameter.

**Example request:**
```http
GET http://localhost:8000/faqs/?lang=hi
```

**Response:**
```json
[
  {
    "id": 1,
    "question": "क्या आपका नाम क्या है?",
    "answer": "मेरा नाम जॉन है।"
  },
  {
    "id": 2,
    "question": "आप क्या करते हैं?",
    "answer": "मैं एक सॉफ़्टवेयर डेवलपर हूं।"
  }
]
```

#### 2. GET /faq/{id}/
Retrieve a single FAQ by its ID. You can filter the FAQ by language using the `lang` query parameter.

**Example request:**
```http
GET http://localhost:8000/faq/1/?lang=te
```

**Response:**
```json
{
  "id": 1,
  "question": "మీ పేరు ఏమిటి?",
  "answer": "నా పేరు జాన్."
}
```

#### 3. POST /faq/
Create a new FAQ.

**Example request:**
```http
POST http://localhost:8000/faq/
Content-Type: application/json

{
  "question": "What is your name?",
  "answer": "My name is John."
}
```

**Response:**
```json
{
  "id": 3,
  "question": "What is your name?",
  "answer": "My name is John.",
  "question_hi": "आपका नाम क्या है?",
  "answer_hi": "मेरा नाम जॉन है।"
}
```

#### 4. PUT /faq/{id}/
Update an existing FAQ.

**Example request:**
```http
PUT http://localhost:8000/faq/1/
Content-Type: application/json

{
  "question": "What is your full name?",
  "answer": "My full name is John Doe."
}
```

**Response:**
```json
{
  "id": 1,
  "question": "What is your full name?",
  "answer": "My full name is John Doe.",
  "question_hi": "आपका पूरा नाम क्या है?",
  "answer_hi": "मेरा पूरा नाम जॉन डो है।"
}
```

#### 5. DELETE /faq/{id}/
Delete an FAQ by ID.

**Example request:**
```http
DELETE http://localhost:8000/faq/1/
```

**Response:**
```json
{
  "message": "FAQ deleted successfully."
}
```

## Contribution Guidelines

We welcome contributions to this project! Here's how you can contribute:

1. **Fork the repository**: Fork this repository to your GitHub account.
2. **Create a feature branch**: Create a new branch for your feature or bug fix.
3. **Make changes**: Implement your changes or fixes.
4. **Test your changes**: Ensure everything works as expected.
5. **Commit your changes**: Commit your changes with a clear message.
6. **Push your branch**: Push your changes to your forked repository.
7. **Create a pull request**: Open a pull request to the main repository. Make sure to provide a detailed explanation of the changes you made.

### **Code style**: Please follow the PEP 8 guidelines for Python code.
