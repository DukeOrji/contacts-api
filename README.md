**Contact Management REST API**

**PROJECTS AIM:**
Manages users and their contact information (phone, email, address).
Demonstrate concepts like API design, authentication, database management, and structured error handling.

**AUTHENTICATION:**

This API uses API Key authentication to secure endpoints.

Requests must include the following header:

x-api-key: 0000

If the API key is missing or incorrect, the server will return:

401 Unauthorized


**TECHNOLOGIES:**

**Languages:** python

**Frameworks:** Flask

**Database:** SQLite

**Tools:** Git, GitHub, Vs code, postman


**FEATURES:**
Full CRUD functionality for managing users and contacts

Relational database design using SQLite

API key authentication for secure endpoints

Input validation and structured error handling

Standardized JSON API responses

Version control with Git


**LAUNCH:**
run python app.py

**using postman or preffered API tester, paste:** 

GET
http://127.0.0.1:5000  to check API health

**Add user contact info:**

POST
http://127.0.0.1:5000/users

**List complete table:**

GET
http://127.0.0.1:5000/users/contacts/list

**List User contact info:**

GET
http://127.0.0.1:5000/users/<user_id>/contacts/list

**Update user contact info:**

PUT
http://127.0.0.1:5000/users/<user_id>/contacts

**clear database / Delete table:**

DELETE
http://127.0.0.1:5000/users/contacts/del

**Delete per user:**

DELETE
http://127.0.0.1:5000/users/<user_id>/contacts/del

**TESTING**

example test:

POST http://127.0.0.1:5000/users

Body:

{

  "name": "John Doe",
  
  "number": "1234567890",
  
  "email": "john@example.com",
  
  "address": "123 Main St"
  
}
