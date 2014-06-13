from zope import interface



class IModel(interface.Interface):
    """ markerinterface
    """


class IModelHandler(interface.Interface):
    
    def __call__(self, model):
        """ Handle the model like save it on a database. After
            that return the json result.
        """


class IModelTransformer(interface.Interface):

    def model(self, request):
        """ return a instance of ext.Models with all
            filled json attributes.
        """
    
    def json(self, model):
        """ return a dict with the data from model. This can
            easily parsed to json.
        """