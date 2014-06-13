import json
import martian

from grokcore.component import adapts
from grokcore.component import baseclass
from grokcore.component import implementer
from grokcore.component import MultiAdapter

from webob.exc import HTTPNotFound
from bb.extjs.datamanager.interfaces import IModel
from bb.extjs.datamanager.interfaces import IModelHandler


implementer(IModel)
class ExtBaseModel(object):
    """ Base model for all model used in extjs.
        All model inherit form this class will automatically grokked.
        
        You will know what a grokker is? So read: https://pypi.python.org/pypi/martian
    """
    martian.baseclass()


class ModelTransfomerUtility(object):
    """ this utility transform a json-request to a
        model. Each model as his named utility.
    """
    
    def __init__(self, class_, schema):
        self.class_ = class_
        self.schema = schema
    
    def model(self, request):
        """ return a instance of Model
        """
        model = self.class_()
        if request.method == 'GET':
            return model
        self.readjson(request, model)
        return model

    def json(self, model):
        data = dict()
        for fieldname in self.schema:
            field = self.schema.get(fieldname)
            data[fieldname] = field.get(model)
        return data
    
    def readjson(self, request, model):
        data = json.loads(request.text)['data']
        for fieldname in self.schema:
            field = self.schema.get(fieldname)
            if fieldname in data:
                field.set(model, data[fieldname])


@implementer(IModelHandler)
class AbstractModelHandler(MultiAdapter):
    adapts()
    baseclass()
    
    def __init__(self, model, request):
        self.model = model
        self.request = request
        self.method = dict(GET=self.get,
                           PUT=self.put,
                           DELETE=self.delete,
                           UPDATE=self.update)
    
    def __call__(self, model):
        return self.method[self.request.method](model)

    def get(self, model):
        raise NotImplemented('get method is not implemented')

    def put(self, model):
        raise NotImplemented('put method is not implemented')

    def delete(self, model):
        raise NotImplemented('delete method is not implemented')
    
    def update(self, model):
        raise NotImplemented('update method is not implemented')




