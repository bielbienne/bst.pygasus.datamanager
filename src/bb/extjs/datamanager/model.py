import json
import martian

from zope.interface import implementer

from grokcore.component import adapts
from grokcore.component import baseclass
from grokcore.component import MultiAdapter

from webob.exc import HTTPNotFound
from bb.extjs.datamanager.interfaces import IModel
from bb.extjs.datamanager.interfaces import IModelHandler


@implementer(IModel)
class ExtBaseModel(object):
    """ Base model for all model used in extjs.
        All model inherit form this class will automatically grokked.
        
        You will know what a grokker is? So read: https://pypi.python.org/pypi/martian
    """
    martian.baseclass()
    
    def instance(self):
        """ return new object of same class
        """
        return self.__class__()


@implementer(IModelHandler)
class AbstractModelHandler(MultiAdapter):
    adapts()
    baseclass()
    
    def __init__(self, model, request):
        self.model = model
        self.request = request
        self.method = dict(GET=self.get,
                           POST=self.create,
                           DELETE=self.delete,
                           PUT=self.update)
    
    def __call__(self, model):
        return self.method[self.request.method](model)

    def get(self, model):
        raise NotImplemented('get method is not implemented')

    def create(self, model):
        raise NotImplemented('put method is not implemented')

    def delete(self, model):
        raise NotImplemented('delete method is not implemented')
    
    def update(self, model):
        raise NotImplemented('update method is not implemented')




