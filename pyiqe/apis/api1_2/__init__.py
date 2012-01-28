# -*- coding: UTF-8 -*-
import os
import simplejson
import hmac
from hashlib import sha1
from datetime import datetime
from utils import multipart_call

class __BaseAPI__(object):
    """
    Handles requests to the IQ Engines API. An API object is 
    initialized using the API key and secret::
    """

    host     = "api.iqengines.com"
    protocol = "http"
    selector = "/v1.2/%s/"

    def __init__(self, key=None, secret=None):
        super(__BaseAPI__,self).__init__()
        self.key = key if key else os.environ.get('IQE_KEY')
        self.secret = secret if secret else os.environ.get('IQE_SECRET')
        assert self.secret and self.key, "Please provide BOTH a secret and a key"

    def _now(self):
        t = datetime.utcnow()
        return t.strftime("%Y%m%d%H%M%S")

    def _build_signature(self, fields, files=None):
        params = [(key, value) for key, value in fields]

        # put the parameters in a dictionary
        if files:
            for f in files:
                param_name = f[0]
                filename = os.path.split(f[1])[1]
                params.append((param_name, filename))

        # reorder the parameters and join key value pairs together
        sorted_params = sorted( ( key,value ) for key,value in params )
        raw_string = u"".join([u"".join(x) for x in sorted_params])

        # compute secret
        digest_maker = hmac.new(self.secret, raw_string.encode("utf-8"), sha1)
        return digest_maker.hexdigest()


    def _signed_call(self, method, selector, fields=None, 
                     files=None, json=False):

        fields = fields if fields else []
        files  = files if files else []
        fields.append(("time_stamp", self._now()))
        fields.append(("api_key", self.key))
        if json: 
            fields += [("json", "1")]

        # build signature
        sig = self._build_signature(fields, files)
        fields.append(("api_sig", sig))

        # unicode these fields
        fields = [(i.encode("utf-8"), j.encode("utf-8")) for i,j in fields]
        files  = [(i.encode("utf-8"), j.encode("utf-8"), k) for i,j,k in files]

        # POST the form
        res = multipart_call( method,
                              self.host, 
                              self.protocol, 
                              self.selector % selector, 
                              fields, 
                              files).read()
        if json:
            res = simplejson.loads(res)
        return res, sig

    def _signed_get(self, method, selector, fields=None, 
                     files=None, json=False):

        fields = fields if fields else []
        files = files if files else []
        fields.append(("time_stamp", self._now()))
        fields.append(("api_key", self.key))
        if json: fields.append(("json", "1"))

        # build signature
        sig = self._build_signature(fields, files)
        fields.append(("api_sig", sig))

        import urllib
        params = urllib.urlencode(dict(fields))

        # SEND the formdata
        url = self.protocol
        url += "://"
        url += self.host
        url += self.selector % selector
        url += "?" 
        url += params
        res = urllib.urlopen(url).read()
        print res
        if json:
            res = simplejson.loads(res)
        return res, sig




class __IQObjects__(__BaseAPI__):
    """\
    This class is a handle to the restful objects upload API

    USAGE
    =====

    >>> from pyiqe import Api
    >>> iqe = Api(version="1.2", key="blah", secret="blah")
    >>> iqe.objects.create( 
            name   = "Back to the future DVD"
            images = [
                "a.jpg",
                "b.jpg",
                "c.jpg",
            ],
            meta = {
                sku: "123123",
                url: "http://retailer.com/123123/"
            }
            collection = "DVDs",
            custom_id  = "123123"
        )
    [out] : {"obj_id": "foobar"}

    # Equivalent Get statements

    >>> obj = iqe.objects.get(custom_id="123123", collection="default")
    >>> obj = iqe.objects.get(id="foobar")
    """


    def __init__(self, key, secret):
        super(__IQObjects__, self).__init__(key=key, secret=secret)


    def create(self, images, name="", meta=None, collection=None, custom_id=None):
        """
        This api-call will upload an image to the IQ Engines servers
        where it will be indexed by the computer vision system. Multiple 
        images may be associated to a single object by making repeated 
        upload calls using the same 'name' attribute.

        :type name: string
        :param name: This is a *unique* name for the object you want to 
            associate to the image

        :type images: list
        :param imgpath: A list of paths to the images you want to have indexed

        :type meta: dictionary
        :param meta: A dictionary holding extra meta information about the object

        :type collection: string
        :param meta: A name for the collection you want to upload to, by default
                     it is set to "_default"

        :type custom_id: string
        :param custom_id: An id that you can assign to this object that you can
                          later use to look up the object.

        Submit an image for Indexing by the IQE Computer Vision System ::
        """

        files  = [("images", i, open(i).read()) for i in images]
        fields = [("name", name)]

        if meta:
            meta = meta or {}
            meta_json = simplejson.dumps(meta)
            fields += [("meta",meta_json)]

        if collection:
            fields += [("collection", collection)]

        if custom_id:
            fields += [("custom_id", custom_id)]

        res, sig = self._signed_call( method="POST", 
                                      selector="object", 
                                      fields=fields, 
                                      files=files, 
                                      json=True)
        return res

    def get(self, obj_id=None, custom_id=None, collection=None):
        """
        Retrieves an object using either the object_id OR a custom_id
        and a collection name 
        """

        assert obj_id or (custom_id and collection), \
            "Either provide an obj_id or a custom_id and a collection name"

        fields = []
        if obj_id:
            selector = "object/%s" % obj_id
        elif custom_id and collection:
            selector = "object"
            fields += [("custom_id", custom_id)]
            fields += [("collection", collection)]

        res, sig = self._signed_call( method="GET", 
                                      selector=selector,
                                      fields=fields,
                                      json=True)
        return res

    def delete(self, obj_id):
        """
        deletes an object
        """
        res, sig = self._signed_call(method="DELETE", 
                                     selector="object/%s/" % obj_id, 
                                     json=True)
        return res

class __IQImages__(__BaseAPI__):


    def get(self, img_id):
        """ Retrieves an image and a collection name """
        fields = []
        if img_id:
            selector = "image/%s/" % img_id
        res, sig = self._signed_call( method="GET", 
                                      selector=selector,
                                      fields=fields,
                                      json=True)
        return res

    def delete(self, obj_id):
        """
        deletes an object
        """
        res, sig = self._signed_call(method="DELETE", 
                                     selector="object/%s/" % obj_id, 
                                     json=True)
        return res
    
    

class Api(__BaseAPI__):
    """ Api 1.2 Handle """


    def __init__(self, key=None, secret=None):
        super(Api, self).__init__(key, secret)
        self.objects = __IQObjects__(key, secret)
        self.images  = __IQImages__(key, secret)


    def query(self, imgpath=None, imgdata=None, webhook=None, extra=None, modules=None, json=True, device_id=None, multiple_results=False):
        """
        :type imgpath: string
        :param imgpath: Path to the image you want to have tagged

        :type imgdata: string
        :param imgpath: binary image data

        :type webhook: string
        :param webhook: url to post the labels

        :type extra: string
        :param extra: JSON encoded extra information
        
        :type device_id: string
        :param device_id: arbitrary string to represent separate devices

        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML
        
        :type multiple_result: boolean
        :param multiple_result: If True the results will contain all possible matches for the given query

        Submit an image to the IQ Engines image labeling engine using the Query API::

            >>> data, qid = api.query('/path/to/img.jpg')
            >>> data
            {u'data': {u'error': 0}}
            >>> qid
            '74235664e1f1fc643a15e44517a4cf3d3cbd6874'

        """
        assert imgpath is not None or imgdata is not None, "either imgpath or imgdata required!"
        if imgdata is None: imgdata = open(imgpath).read()
        files  = [ ("img", imgpath or sha1(imgdata).hexdigest(), imgdata) ]
        fields = []
        if webhook:
            fields += [("webhook", webhook)]
        if modules:
            fields += [("modules", simplejson.dumps(modules))]
        if extra:
            fields += [("extra", simplejson.dumps(extra))]
        if device_id:
            fields += [("device_id", device_id)]
        if multiple_results:
            fields += [("multiple_results", "1")]
        
            
        fields = fields if fields else None
        data, sig = self._signed_call(method="POST", selector="query", fields=fields, files=files, json=json)
        return data, sig


    def update(self, json=True, device_id=None):
        """
        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML

        Start a long-polling request to wait for resutls using the Update API::

            >>> results = api.update()
            >>> results
            {u'data': {u'error': 0,
                       u'results': [{u'qid': u'74235664e1f1fc643a15e44517a4cf3d3cbd6874',
                                     u'qid_data': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                                   u'labels': u'Duracell Batteries'}}]}}

        """
        fields = []
        if device_id:
            fields=[("device_id", device_id)]
        data, _ = self._signed_call(method="POST", selector="update", fields=fields, json=json)
        return data


    def result(self, qid, json=True):
        """
        :type qid: string
        :param qid: The QID corresponding to the image for which you want to retrieve the labels

        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML

        Retrieve the results for a specific QID using the Result API::

            >>> result = api.result(qid="74235664e1f1fc643a15e44517a4cf3d3cbd6874")
            >>> result
            {u'data': {u'error': 0,
                       u'results': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                    u'labels': u'Duracell Batteries'}}}

        """
        data, _  = self._signed_call(method="POST", 
                                    selector="result", 
                                    fields=[("qid", qid)], 
                                    json=json)
        return data

