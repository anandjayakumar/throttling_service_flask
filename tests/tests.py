from __future__ import print_function
import sys
import unittest
import time
import requests

from config import SERVER_URL


class TestThrottleService(unittest.TestCase):
    
    
    def setUp(self):
        self.register_url = SERVER_URL + 'register'
        self.unregister_url = SERVER_URL + 'unregister'
        self.process_url = SERVER_URL + 'process'       
        self.test_name = "test_api_name"
        self.test_scope = "default_scope"
    
    
    def test_unregister_endpoint(self):
        #register an API with limit 5 times per 10 seconds
        api_key = call_register_api(self.register_url,"test_api_name1",self.test_scope,5,10)
        
        #call the throttling service once and check the response
        json_data = {"api_key":api_key}
        response = requests.post(self.unregister_url, json=json_data).json()
        
        self.assertEqual(response['status'], "success")
    
    
    def test_no_throttling(self):
        #register an API with limit 5 times per 10 seconds
        api_key = call_register_api(self.register_url,"test_api_name2",self.test_scope,5,10)
        
        #call the throttling service 5 times and check the response
        json_data = {"api_key":api_key}
        res = list()
        for i in range(5):
            res.append(requests.post(self.process_url, json=json_data).json())
        
        for r in res:
            self.assertEqual(r['status'], "success")
        
        #unregister the API
        response = requests.post(self.unregister_url, json=json_data).json()
        self.assertEqual(response['status'], "success")
    
    
    def test_throttle_once(self):
        #register an API with limit 5 times per 10 seconds
        api_key = call_register_api(self.register_url,"test_api_name3",self.test_scope,5,10)
        
        #call the throttling service 5 times and check the response
        json_data = {"api_key":api_key}
        res = list()
        for i in range(5):
            res.append(requests.post(self.process_url, json=json_data).json())
        
        for r in res:
            self.assertEqual(r['status'], "success")
        
        #call the throttling service once and check the response
        response = requests.post(self.process_url, json=json_data).json()
        self.assertEqual(response['status'], "failure")
        
        #unregister the API
        response = requests.post(self.unregister_url, json=json_data).json()
        self.assertEqual(response['status'], "success")
    
    
    def test_wait_and_retry(self):
        #register an API with limit 5 times per 10 seconds
        api_key = call_register_api(self.register_url,"test_api_name4",self.test_scope,5,10)
        
        #call the throttling service 5 times and check the response
        json_data = {"api_key":api_key}
        res = list()
        for i in range(5):
            res.append(requests.post(self.process_url, json=json_data).json())
        
        for r in res:
            self.assertEqual(r['status'], "success")
        
        #wait 10 seconds and retry
        time.sleep(10)
        response = requests.post(self.process_url, json=json_data).json()
        self.assertEqual(response['status'], "success")
        
        #unregister the API
        response = requests.post(self.unregister_url, json=json_data).json()
        self.assertEqual(response['status'], "success")
        


def call_register_api(register_url,api_name,scope,limit,per):
    json_data = {"api_name":api_name,"api_scope":scope,"limit":limit,"per":per}
    res = requests.post(register_url, json=json_data)
    return res.json()['api_key']


if __name__ == '__main__':
  unittest.main()