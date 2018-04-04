# Throttling Service
An API Throttling service written in Flask, using Redis for data storage.


## Installation
The required python packages are provided in requirements.txt file. It can be installed by running the command
```python
pip install -r requirements.txt
```
Next, run app.py as a Flask application by running the command
```python
python app.py
```
This will start the application from a webserver running at localhost:5000  
For demo purposes, a Redis server is running from an Amazon EC2 instance. To use local Redis server, this can be reconfigured from app.py


## Usage
The Throttling Service has 3 APIs for the basic functionalities:
### Register 
The client API call can be registered with the throttling service using this API.
  
The Register API accepts a JSON POST request at `'/register'` which requires the following fields -  
`api_name` - This is the name of the function/API call that needs to be throttled.  
`api_scope` - This is the scope of the function/API call. The combination of api_name and api_scope should be unique. For example, if a user_id is given as scope, multiple throttlers can be registered for the same API call for multiple users.  
`limit` - This is the limit for the throttler. For example, to throttle at a rate of 50 times in 2 minutes, limit will be 50.  
`per` - This is the interval period for the throttler, in seconds. In the above example, per will be 120.  
  
Return value - The API key corresponding to the client API call is returned, which is used for calling other APIs.

### Unregister
The client API call can be removed from the throttling service using this API.
  
The Unregister API accepts a JSON POST request at `'/unregister'` which requires the following fields -   
`api_key` - This is the API key corresponding to the client API call, returned by the Register API.
  
Return value - 'Success' if the API key is successfully removed. Else 'Failure' is returned.

### Process
Each time before the registered API call is executed the client should call this API, with the API key. If the throttle limit is crossed, this will return 'Failure', otherwise it returns 'Success'.
  
The Process API accepts a JSON POST request at `'/process'` which requires the following fields -  
`api_key` - This is the API key corresponding to the client API call, returned by the Register API.
  
Return value - 'Success' if the limit is not crossed. Else 'Failure' is returned.


## Unit Testing

The unit test cases are provided in tests.py. 


## Demo

For quick demo, an instance of this application is running at an Amazon EC2 instance, available in   
http://ec2-18-188-68-114.us-east-2.compute.amazonaws.com/  
For example, the Register API can be called at http://ec2-18-188-68-114.us-east-2.compute.amazonaws.com/register.


## Future Enhancements
1. Currently, null JSON inputs are not handled properly.  
2. The application requires a unique combination of API name and scope. The causes issues when multiple clients try to register APIs with same name and scope. This can be overcome by generating random hashes and appending it to the API key.





