import time
import unittest    
from pprint import pprint 
import os.path as P
CWD = P.abspath(P.dirname(__file__))

def test_basic_imports():
    """ Make sure we can atleast import everything """
    from pyiqe import Api
    api = Api()


class TestApi(unittest.TestCase):
    
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")
        
    def test_QueryExtra(self):
        """ Make sure we pass back extra argument is returned"""
        import json
        device_id = "pyiqe.test.%s" % time.time()
        response, qid = self.api.query('testdata/dole1.jpeg', extra={'a':1}, device_id=device_id)
        
        # update method
        result = self.api.update(device_id=device_id)
        pprint(result)
        result = result['data']['results']
        pprint(result)
        assert "extra" in result[0] and result[0]['extra'] == json.dumps({'a':1}), "Extra Argument mismatch %s" % result
        
        # result method
        response = self.api.result(qid)
        result = response['data']
        pprint(result)
        assert "extra" in result and result['extra'] == json.dumps({'a':1}), "Extra Argument mismatch %s" % result
    
    # def test_QueryMultipleResult(self):
    #     # retrieve a result known to have multiple results
    #     device_id = "pyiqe.test.%s" % time.time()
    #     response, qid = self.api.query('testdata/multipleresult.jpeg', extra={'a':1}, device_id=device_id, multiple_results=True)
    #     print qid
    #     
    #     result = self.api.update(device_id=device_id)
    #     pprint(result)
    #     self.assertTrue(len(result['data']['results'][0]['qid_data']) > 1, "Invalid Multiple Result Return")

class TestTrainingAPI(unittest.TestCase):
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")
        self.prev_upload = P.join(CWD, "uploaded.txt")
        


    def tearDown(self):
        import os
        rs_delete = self.api.objects.delete(self.obj_id)
        print rs_delete
        self.assertTrue(rs_delete['error'] == 0)
        if P.exists(self.prev_upload):
            os.remove(self.prev_upload)
    
    def test_CreateObjectandDelete(self):
        import time
        import os.path as P

        # parameters

        imgpath = P.join(P.dirname(P.abspath(__file__)), "testdata/fox.jpeg")
        name = str(time.time())
        
        # check if we didn't clean up from last test

        if P.exists(self.prev_upload):
            print "removing previous upload"
            prev_oid = open(self.prev_upload, "r").read().strip()
            self.api.objects.delete(prev_oid)
            
            
        
        # train the system
        rs_training = self.api.objects.create(
            name = name,
            images = [imgpath], 
            custom_id = "123"
        )
        
        print "Training API response =", rs_training
        self.assertTrue(rs_training['error'] == 0, "Training API request failed")
        
        
        
        
        # try retrieving it
        obj_id = rs_training['obj_id']
        self.obj_id = obj_id
        rs_get = self.api.objects.get(obj_id)
        self.assertTrue(rs_get['object']['obj_id'] == obj_id, "Retrieval Failed")
        
        # write to previous upload file
        print "writing upload file"
        with open(self.prev_upload, "w") as fh:
            fh.write(obj_id)
        
        time.sleep(200)
        # try retrieving related_image
        img_id = rs_get['object']['related_images']['images'][0]['img_id']
        print(rs_get)
        rs_img_get = self.api.images.get(img_id)
        print rs_img_get
        self.assertTrue(rs_img_get['image']['related_object']['obj_id'] == obj_id)
        
        # wait 10 seconds before querying
        time.sleep(20)

        # query the system for the image
        rs_query, qid = self.api.query(imgpath=imgpath)
        print "Query API response =", rs_query
        print "qid =", qid
        self.assertTrue(rs_query['data']['error'] == 0, "Query API request failed")
        
        # retrieve the results
        for i in range(20):
            rs_result = self.api.result(qid)
            print "Result API response =", rs_result
            assert rs_result['data']['error'] == 0, "Result API request failed"
            if rs_result['data'].has_key('results'):
                break
            time.sleep(2)

        self.assertTrue(rs_result['data'].has_key('results'), "Result API did not return any result after 20 tries")
        self.assertTrue(rs_result['data']['results']['labels'] == name, "Result API does not return correct labels")
        self.assertTrue(rs_result['data']['results']['obj_id'] == rs_training['obj_id'], "Result API does not return correct labels")



class RestfulImagesApi(unittest.TestCase):
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")
        
    def testGetImage(self):
        rs_get = self.api.images.get('cc16e9b6f1be4013b53a817a1eea5bdd')
        self.assertTrue(rs_get['error'] == 0, "Unsucessfully retrieve image")
        self.assertTrue(rs_get['image']['img_id'] == 'cc16e9b6f1be4013b53a817a1eea5bdd', "mismatched image id")
    
    def testNonExistentImage(self):
        rs_get = self.api.images.get('cc16e9b6f1be7773b53a817a1eea5bdd')
        self.assertTrue(rs_get['error'] == 1, "No error was thrown for a non-existing image")
    
