import requests

from .base import Base


class Connection:
    url = []
    auth = None

    @staticmethod
    def get(endpoint):
        url = Connection.form_url(endpoint)
        return requests.get(url=url, auth=Connection.auth).json()

    @staticmethod
    def post(endpoint, **kwargs):
        url = Connection.form_url(endpoint)
        return requests.post(url, auth=Connection.auth, **kwargs).json()

    @staticmethod
    def put(endpoint, **kwargs):
        url = Connection.form_url(endpoint)
        return requests.put(url, auth=Connection.auth, **kwargs).json()

    @staticmethod
    def form_url(*args):
        url_parts = Connection.url + list(args)
        url = '/'.join(url_parts)
        return url


class Document(Base):

    def save(self):
        if self._id:
            instance = self._update()
        else:
            instance = self._create()
        return instance

    def refresh(self):
        latest = Connection.get(self._id)
        self.set(**latest)

    def _update(self):
        req = Connection.put(self._id, json=self.attributes)
        self.set(_id=req.get('id'), _rev=req.get('rev'))
        return req

    def _create(self):
        req = Connection.post('', json=self.attributes)
        self.set(_id=req.get('id'), _rev=req.get('rev'))
        return req


class Database(object):

    def __init__(self, name):
        self.name = name

    def find(self, query):
        response = Connection.post('_find', json={"selector": query})
        for doc in response['docs']:
            yield Document(**doc)

    def get(self, id):
        doc = Connection.get(id)
        if doc.get('error'):
            raise LookupError(doc)
        else:
            return Document(**doc)

    def create(self, **kwargs):
        doc = Document(**kwargs)
        doc.save()
        return doc


class CouchDB:

    def __init__(self, url: str, username: str, password: str):
        Connection.url.append(url)
        Connection.auth = (username, password)

    def get_databases(self):
        return Connection.get('_all_dbs')

    def create(self, database: str, **params):
        db = self.use(database)
        state = Connection.put('', params=params)
        if state.get('ok'):
            return db
        else:
            raise ValueError(state)

    def use(self, database: str):
        if len(Connection.url) > 1:
            Connection.url[1] = database
        else:
            Connection.url.append(database)
        return Database(database)
