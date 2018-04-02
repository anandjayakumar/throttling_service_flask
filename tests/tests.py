import unittest
import time

from config import SERVER_URL


class TestThrottleService(unittest.TestCase):
    
	process_url = SERVER_URL + 'process'
	
    def test_no_throttling(self):        
		#TODO
	
	def test_throttle_once(self):
		#TODO
	
	def test_wait_and_retry(self):
		#TODO