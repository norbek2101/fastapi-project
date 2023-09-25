#README.md for fastapi-project
##fastapi-project is a FastAPI project with JWT token authentication.

Requirements
Python 3.7+
FastAPI
Python-jose
Installation
To install the dependencies, run the following command:

pip install -r requirements.txt
Running the application
To run the application, run the following command:

uvicorn main:app --host 0.0.0.0 --port 8000
Usage
To use the application, you need to generate a JWT token and provide it to Swagger UI when you first open the page. You can generate a JWT token by making a POST request to the /login endpoint with your username and password.

Once you have a JWT token, you can use it to authorize all subsequent requests to the application. To do this, open Swagger UI and click the Authorize button. In the Authorization dialog box, select the Bearer option and enter your JWT token in the Value field. Click the Authorize button to save your JWT token.

Swagger UI will now authorize all subsequent requests with your JWT token. You can now test the API endpoints.

Documentation
To view the API documentation, open Swagger UI at http://localhost:8000/docs.
