import json
from datetime import datetime

from zope import schema
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.component import getMultiAdapter
from grokcore.component import adapts
from grokcore.component import implementer
from grokcore.component import MultiAdapter

from bb.extjs.datamanager.interfaces import IModel
from bb.extjs.datamanager.interfaces import IFieldTransformer

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

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
            data[fieldname] = getMultiAdapter((model, field), IFieldTransformer).get()
        return data
    
    def readjson(self, request, model):
        data = json.loads(request.text)['data']
        for fieldname in self.schema:
            field = self.schema.get(fieldname)
            if fieldname in data:
                getMultiAdapter((model, field), IFieldTransformer).set(data[fieldname])


@implementer(IFieldTransformer)
class GenericFieldTransfomer(MultiAdapter):
    adapts(IModel, schema.interfaces.IField)
    
    def __init__(self, model, field):
        self.model = model
        self.field = field
    
    def get(self):
        return self.field.get(self.model)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        elif IFromUnicode.providedBy(self.field):
            self.field.set(self.model, self.field.fromUnicode(value))
        else:
            self.field.set(self.model, value)


class DateFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IDate)
    
    def get(self):
        date = self.field.get(self.model)
        if date is None:
            return date
        return date.strftime(DATETIME_FORMAT)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            value = datetime.strptime(value, DATETIME_FORMAT)
            self.field.set(self.model, value)


class IdFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IId)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            self.field.set(self.model, int(value))


class BoolFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IBool)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            if not isinstance(value, bool):
                raise TypeError('The value %s is not a boolean' % value)
            self.field.set(self.model, value)


