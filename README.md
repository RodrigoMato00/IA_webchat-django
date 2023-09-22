# ChatBot API

A Django project that provides a chat interface and API. The bot takes in a URL and user message and responds based on the content of the provided URL. The bot is designed to be aware of the content of the provided URL and will generate a response accordingly.
## Features:
1. Web chat interface where users can input a URL and chat based on the content.
2. API endpoint to chat programmatically, given a URL and user message.
3. User authentication using tokens.
## Installation & Setup:
### Requirements:
- Python
- Django
### Steps: 
1. **Clone the Repository:** 

```bash
   git clone [your-repository-link](https://github.com/RodrigoMato00/IA_webchat-django.git)
   cd IA_webchat-django
```
2. **Set Up a Virtual Environment (optional but recommended):** 

```bash

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
``` 
3. **Install Dependencies:** 

```

pip install -r requirements.txt
``` 
4. **Migrate Database:** 

```

python3 manage.py migrate
``` 
5. **Create Superuser (for Django Admin):** 

```

python3 manage.py createsuperuser
``` 
6. **Run the Development Server:** 

```

python3 manage.py runserver
```
## Usage:
### Web Chat Interface:

Visit `http://127.0.0.1:8000/chatapp/chat-interface/` to access the chat interface.
### API Usage: 
1. **Authenticate:** 

Send a `POST` request to `http://127.0.0.1:8000/chatapp/login/` with your username and password to obtain a token.

Example request body:

```json

{
  "username": "your_username",
  "password": "your_password"
}
```



The response will include a token. 
2. **Chat API:** 

Send a `POST` request to `http://127.0.0.1:8000/chatapp/chat-api/` with the token in the header and the URL and user message in the body.

Example request headers:

```makefile

Authorization: Token your_token
```



Example request body:

```json

{
  "url": "https://example.com",
  "user_message": "Tell me about this."
}
```
### Swagger Documentation:

For detailed API documentation, visit `http://127.0.0.1:8000/swagger/`.
## Support:

For any queries, reach out to `RodrigoMato00`.---
