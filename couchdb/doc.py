import requests

from base import Base


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
        Connection.put(self._id, json=self.attributes)


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
            if doc.get('reason') == 'missing':
                raise NotFound('error')
        else:
            return Document(**doc)


class CouchDB:

    def __init__(self, url: str, username: str, password: str):
        Connection.url.append(url)
        Connection.auth = (username, password)

    def get_databases(self):
        return Connection.get('_all_dbs')

    def use(self, database: str):
        if len(Connection.url) > 1:
            Connection.url[1] = database
        else:
            Connection.url.append(database)
        return Database(database)
