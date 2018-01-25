# lite_google_oauth

get your google client_secrets.json, put it in the same folder

Example:
```python
from author import Author
```
Create an object that signs your requests. 
```python
doc = Author(scopes_list)
```
This little object takes care of the authentication, and then finally when you're about to create a request you do: 
```python
headers = {'Content-type': 'application/json',  'Authorization' : 'Bearer %s' % doc.sign({})['access_token']}
```
and pass the headers in with your requests: 
```python
r = requests.post(url,data = json.dumps(params),  headers = headers)
```
