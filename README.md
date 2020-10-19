DOKKA's REST API
================
this project includes a rest api which exposes two methods.
getAddress and getResult

### getAddress
the method getAddress requires a csv as an input and returns a dictionary.
the csv should have 3 columns, Point, Latitude, Longitude and should look like this: <br></br>
<img src="https://i.imgur.com/hUTaCIl.png" width=500 /> <br></br>
if the csv is valid, the api will return a dictionary containing the keys: points, links
e.g.: <br></br>
<img src="https://i.imgur.com/gvaKH7j.png" width=500 /> <br></br>
if the csv is not valid the api will return the following dictionary: <br></br>
<img src="https://i.imgur.com/Hl5ixnm.png" width=500 />

### getResult
the method getResult takes a uuid as a parameter and returns the points and links of the uuid.
if the uuid does not exist in the database the dictionary will be empty.

How to install
==============
clone the reopsitory into your directory. <br></br>
cd into the server directory and run the following command in the terminal: <br></br>
export FLASK_APP=REST.py <br></br>
to run the flask framework run flask run in the terminal. <br></br>

How to use
============
### cURL
(to use the commands to query the api the flask app needs to be running)
you can use the cURL command through the terminal to query the api. <br></br>
e.g.:
<br></br>
to interact with getAddress: curl -F "file=@</PATH/TO/YOUR/CSV/FILE>" http://127.0.0.1:5000/api/getAddress  <br></br>
to interact with getResult: curl http://127.0.0.1:5000/api/getResult?result_id=<RESULT_ID> 


Compatibility
=============
DOKKA's rest api requires Python 3.6+


Requirements
===========
flask, flask-alchemy, SQLAlchemy, pandas


