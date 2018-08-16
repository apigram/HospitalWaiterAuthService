# HospitalWaiterAuthService
Single sign-on authentication microservice for the HospitalWaiter app.

## Deployment for development/testing

It is best to run the microservice using a virtual Python environment (virtualenv). The following steps assume the creation of a virtual python environment.

1. Clone this repository into your document root folder for your web server.
2. Create a Python virtual environment by using the virtualenv command (eg. virtualenv venv)
3. Start the virtual environment.
4. From the command-line, run pip install -r requirements.txt. This will install all required dependencies.
5. Set the following environment variables using the SET command:
    * SECRET_KEY - The secret key used for token authentication. This should be the same secret key used for the SSO microservice.
    * DATABASE_URL - The URL of the database to interface with. This should include the schema, host, port and password where applicable.
6. Run the following command: flask run -p [PORT] (where [PORT] is the port from which to run the microservice. This defaults to 5000 but may need to change if multiple microservices are running from the same machine). This will start the server.

## API Specification

|Endpoint URL        |Available actions|
|--------------------|-----------------|
|`/authservice/token`|`GET`            |

## Usage
This microservice provides a single endpoint which will retrieve an authentication token upon a successful login using 
basic login authentication (ie. username and password). Simply make a request to `/authservice/token`,
including the username and password in the auth header of your request. The returned token can then be attached to the 
Authorization header under the 'Bearer' scheme for any requests to other microservices in the HospitalWaiter suite.
