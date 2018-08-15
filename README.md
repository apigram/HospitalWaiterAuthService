# HospitalWaiterAuthService
Single sign-on authentication microservice for the HospitalWaiter app.

# Usage
This microservice provides a single endpoint which will retrieve an authentication token upon a successful login using basic login authentication (ie. username and password). Simply make a request to http://ENDPOINT_URL/authservice/token, including the username and password in the auth header of your request. The returned token can then be attached to the Authorization header under the 'Bearer' scheme for any requests to other microservices in the HospitalWaiter suite.
