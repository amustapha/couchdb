class Base(object):

    def __init__(self, **kwargs):
        self.num = 100
        self.attributes = kwargs

    def __getattr__(self, item):
        return self.attributes.get(item, None)

    def set(self, **kwargs):
        self.attributes.update(kwargs)
