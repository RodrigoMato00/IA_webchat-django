ChatBot API
A Django project that provides a chat interface and API. The bot takes in a URL and user message and responds based on the content of the provided URL. The bot is designed to be aware of the content of the provided URL and will generate a response accordingly.

Features:
Web chat interface where users can input a URL and chat based on the content.
API endpoint to chat programmatically, given a URL and user message.
User authentication using tokens.
Installation & Setup:
Requirements:
Python
Django
Steps:
Clone the Repository:

bash
Copy code
git clone [your-repository-link]
cd [your-repository-directory]
Set Up a Virtual Environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:

Copy code
pip install -r requirements.txt
Migrate Database:

Copy code
python manage.py migrate
Create Superuser (for Django Admin):

Copy code
python manage.py createsuperuser
Run the Development Server:

Copy code
python manage.py runserver
Usage:
Web Chat Interface:
Visit http://127.0.0.1:8000/chatapp/chat-interface/ to access the chat interface.

API Usage:
Authenticate:

Send a POST request to http://127.0.0.1:8000/chatapp/login/ with your username and password to obtain a token.

Example request body:

json
Copy code
{
  "username": "your_username",
  "password": "your_password"
}
The response will include a token.

Chat API:

Send a POST request to http://127.0.0.1:8000/chatapp/chat-api/ with the token in the header and the URL and user message in the body.

Example request headers:

makefile
Copy code
Authorization: Token your_token
Example request body:

json
Copy code
{
  "url": "https://example.com",
  "user_message": "Tell me about this."
}
Swagger Documentation:
For detailed API documentation, visit http://127.0.0.1:8000/swagger/.
