# CouchDB [WIP]
#### A simple python module for basic couchdb operations

## Scope
Currently, this module can perform

- find query
- get
- save


## How to
```python
from couchdb import CouchDB
couch = CouchDB('http://localhost:5984', 'username', 'password')
couch.get_databases() #lists all databases

db = couch.use('my_custom_db')
db.find({
    'age': {'$gt': 17} 
})

doc = db.get('single-document-id')
doc.set(newValue='my custom new value')
doc.save()
print(doc.newValue) # my custom new value
```