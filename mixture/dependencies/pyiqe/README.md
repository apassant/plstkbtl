pyiqe
=====

pyiqe is a python module written to use the IQ Engines API v1.2. The documentation for the API is available on IQ Engines' developer portal

    Developer portal: http://http://developer.iqengines.com/
    Documentation: http://developer.iqengines.com/apidoc/1.2/

Requirements
------------

We require simplejson, a JSON encoder/decoder for python. To install simplejson:

    easy_install simplejson

Installation
------------

To install the pyiqe module run setup.py

    python setup.py install

or to install via pip or easy_install:
    
    pip install pyiqe

API Credentials
---------------

To use the IQ Engines API you will need an API key and a secret. You can request your key and secret in less than 60 seconds! (http://developer.iqengines.com/accounts/register/) 


Basic Usage
-----------

To use the API, you first create an API instance that handles the requests to the IQ Engines API. You can initialize it using your API key and secret:

    >>> from pyiqe import Api
    >>> api = Api(IQE_KEY, IQE_SECRET)

You can query an image by doing:

    >>> data, qid = api.query("/path/to/img.jpg")
    >>> data
    {u'data': {u'error': 0}}
    >>> qid
    '74235664e1f1fc643a15e44517a4cf3d3cbd6874'

The error code of 0 means that the image has been successfully uploaded to IQ Engines' server, and the qid is the unique identifier for the image you submitted.

You can retrieve the results using the Update API.

    >>> results = api.update()
    >>> results
    {u'data': {u'error': 0,
               u'results': [{u'qid': u'74235664e1f1fc643a15e44517a4cf3d3cbd6874',
                             u'qid_data': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                           u'labels': u'Duracell Batteries'}}]}}

Update API is a long-polling request. As soon as IQ Engines has tagged your image, it'll output your results!




