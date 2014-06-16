import json

from webob.exc import HTTPNotFound

from zope.component import getUtility
from zope.component import getMultiAdapter

from bb.extjs.core import ext
from bb.extjs.core.interfaces import IApplicationContext

from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.wsgi.interfaces import IRootDispatcher

from bb.extjs.datamanager.interfaces import IModelHandler
from bb.extjs.datamanager.interfaces import IModelTransformer


@ext.implementer(IRootDispatcher)
class DataManagerEntryPoint(ext.MultiAdapter):
    """ manager all ajax request with CRUD options.
    """
    ext.name('data')
    ext.adapts(IApplicationContext, IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        self.request.response.content_type='application/javascript'
        
        try:
            self.request.path_info_pop()
            entity = self.request.path_info_pop()
            transformer = getUtility(IModelTransformer, entity)
            model = transformer.model(self.request)
            handler = getMultiAdapter((model, self.request,), IModelHandler)
            results = handler(model)
            if not isinstance(results, (list, tuple,)):
                data = transformer.json(results)
            else:
                data = [transformer.json(i) for i in results]
            self.successresponse('Data loaded from class %s' % model, data)
        except Exception as e:
            self.errorresponse(str(e))

    def errorresponse(self, message):
        self.request.response.status_code = 400
        self.request.response.write(json.dumps(dict(success=False,
                                           message=message,
                                           total=0,
                                           data=list()), indent=' '*4))
    
    def successresponse(self, message, data):
        length = 1
        if isinstance(data, (list, tuple,)):
            length = len(data)
        elif data is None:
            length = 0
        self.request.response.write(json.dumps(dict(success=True,
                                           message=message,
                                           total=length,
                                           data=data), indent=' '*4))


