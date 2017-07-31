from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        for key, value in json_data.items():
            setattr(self, key, value)
        

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        resource = cls.__name__.lower()
        return cls(getattr(api_client, 'get_' + resource)(resource_id))
 
        

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        # return generator from derived class iterator
        resource = cls.__name__
        Querysetclass = resource + 'QuerySet()'
        return eval(Querysetclass)


class People(BaseModel):
    """Representing a single person"""
    pass


class Films(BaseModel):
    """Representing a single film"""
    pass


class BaseQuerySet(object):

    def __init__(self):
        #0-9
        self._current_record = 0
        #1-10
        self._current_page = 0
        
        resource = type(self).__name__
        self.resource_name = resource.replace('QuerySet', '')
        self.method_name = "get_" + self.resource_name.lower()
        self._count = 0
        self._results =[]
        

    def __iter__(self):
        self._current_record = 0
        self._current_page = 1
        self._count = None
        
        return self.__class__()

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """

        while True:
            
            if self._current_record + 1 > len(self._results):
                try:
                    self.get_next_record()
                except SWAPIClientError:
                    raise StopIteration()
            elem = self._results[self._current_record]
            self._current_record += 1
            return elem
            
        
    def get_next_record(self):
        
        self._current_page += 1
        
        method_to_call = getattr(api_client,self.method_name)
        json_data = method_to_call(**{'page': self._current_page})
        if self._current_page == 1:
            self._count = json_data['count']
        list_of_dicts = json_data['results']
        
        for item in list_of_dicts:
            model_obj = eval(self.resource_name)(item)
            self._results.append(model_obj)
         
        
    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        if not self._count:
            method_to_call = getattr(api_client, self.method_name)
            json_data = method_to_call(page=1)
            self._count = json_data['count'] 
            return self._count
        else:
            return self._count


class PeopleQuerySet(BaseQuerySet):
    pass


class FilmsQuerySet(BaseQuerySet):
    pass
