#!/usr/bin/python
"""
Seevl API for python 3.

You can use it in two ways :
 - You can make low-level API Calls by using the function api_call.
 - You can use the search function to get a list of Entity objects : These objects are very easy to use, and contain methods to transparently get what you need.

For more informations, see : http://data.developers.seevl.net/wiki
"""

import json
import os

try: # Python 3
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
    from urllib.request import HTTPError
except ImportError: # Python 2
    import urllib2 as urllib_request
    import urllib as urllib_parse
    from urllib2 import HTTPError


# Settings
# You can give your api_credentials here, or you can put them in SEEVL_APP_ID and SEEVL_APP_KEY environment variables.
# Or, if you use only the api_call() function to directly call the api, you can pass them as parameters of this functino.

#########################
### Errors
#########################

class SeevlError(Exception): 
    def __init__(self, error):
        self.code = error.code
        self.args = ['seevl endpoint access error (%s): %s' %(self.code, self.getMessage())]
    
    def getMessage(self):
        if self.code == 401:
            return 'Please make sure your endpoint credentials are correcly set-up'
        if self.code == 402:
            return 'You have excessed your query limits'
        if self.code == 404:
            return 'The requested resource has not been found'
        else:
            return ''
            
#########################
### Entity
#########################

class SeevlEntity():

    def __init__(self, uri, values=False, api_credentials=False):
        self.uri = uri
        SEEVL_ENDPOINT = os.environ.get('SEEVL_ENDPOINT', 'http://data.seevl.net/')
        if values:
            self.id = values.get('id', False)
            self.prefLabel = values.get('prefLabel', False)
            self.description = values.get('description', False)
            self.thumbnail = values.get('thumbnail', False)
            self.depiction = values.get('depiction', False)
        else:
            self.id = self.uri[len(SEEVL_ENDPOINT+'entity')+1:-3]
        self.api_credentials = api_credentials

    def __eq__(self, other):
        return self.uri == other.uri
    __ne__ = lambda self, other: not self == other

    def __str__(self):
        return self.prefLabel

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.uri)

    def _make_dict(self, data):
        """ This function convert entities in an API call result in entities objects """
        d = {}
        for name, value in data.items():
            if isinstance(value, list) and len(value) > 0 and 'id' in value[0]:
                d[name] = [SeevlEntity(v['uri'], v, self.api_credentials) for v in value]
            else:
                d[name] = value
        return d

    # Methods and property you can call
    def api_call(self, call):
        """ Do an API call for this entity """
        return querySeevlEndpoint('entity/{}/{}'.format(self.id, call), self.api_credentials)
    
    ############
    ## Infos    
    ############
    @property
    def infos(self):
        return self.api_call('infos')

#    @cached_property
    @property
    def facts(self):
        """ Return a list of facts about this entity 
        
        >>> entity = search({'genre': 'A2FtdpRA'})[0]
        >>> bool( entity.facts )
        True
        """
        return self.api_call('facts')
#        return self._make_dict(self.api_call('facts'))

#    @cached_property
    @property
    def links(self):
        """ Return a list of links pointing to external sites for this entity """
        return self.api_call('links')

#    @cached_property
    @property
    def related(self):
        """ Return a list of related entities

        >>> results = search_by_name('the beatles')[0]
        >>> lennon = search_by_name('john lennon')[0]
        >>> lennon in results.related
        True
        """
        return [SeevlEntity(i['object']['uri'], i['object']) for i in self.api_call('related')['association']]

    def relations(self, other):
        """ Return a structure explaining the relationship between two entities 

        >>> entity = search_by_name('pendulum')[0]
        >>> bool( entity.relationship_with(entity.related[0]) )
        True
        """
        assert isinstance(other, self.__class__)
        return [self._make_dict(i) for i in self.api_call('related/{}'.format(other.id))['data']]

#########################
### Entity search
#########################
        
class SeevlEntitySearch(object):
            
    def __init__(self, filters, api_credentials=False):
        self.filters = filters
        self.api_credentials = api_credentials
        
    def run(self):
        """
    Run a search query over the seevl endpoint.
    
    This function takes a dictionnary of "filters" as parameter, and return a list of entities.

    >>> entities = search_by_name('pendulum')
    >>> str(entities[0].name) # str() is for python2 : we don't want unicode object
    'Pendulum'
    >>> len(  search( {'genre': Entity('A2FtdpRA')} )  ) > 0
    True
    """
        result = querySeevlEndpoint('entity/?' + urllib_parse.urlencode(self.filters), self.api_credentials)
        return [SeevlEntity(result['uri'], result, self.api_credentials) for result in result['results']] if result.get('results') else []
    
#########################
### Helper methods
#########################

def querySeevlEndpoint(query, api_credentials=False):
    """ Run remote calls to the seevl endpoint """
    
    SEEVL_APP_ID = api_credentials[0] if api_credentials else os.environ.get('SEEVL_APP_ID', False)
    SEEVL_APP_KEY = api_credentials[1] if api_credentials else os.environ.get('SEEVL_APP_KEY', False)
    SEEVL_ENDPOINT = os.environ.get('SEEVL_ENDPOINT', 'http://data.seevl.net/')

    opener = urllib_request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'seevl-python'),
        ('Accept', 'application/json'),
        ('X_APP_ID', SEEVL_APP_ID), 
        ('X_APP_KEY', SEEVL_APP_KEY)
    ]
    
    ## Run query
    try:
        request = opener.open(SEEVL_ENDPOINT + query)
    except HTTPError as error:
        raise SeevlError(error)

    ## Get JSON data
    response = request.read().decode()
    return json.loads(response)