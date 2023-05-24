'''
Created on 2023-03-23

@author: wf
'''
from tests.basetest import Basetest
from gremlin.remote import RemoteTraversal

class BaseGremlinTest(Basetest):
    """
    Basetest for Gremlin Python
    """
    
    def setUp(self, debug=False, profile=True):
        """
        prepare the test environment
        """
        Basetest.setUp(self, debug, profile)
        self.rt=RemoteTraversal()
        self.g=self.rt.g()
        
    def tearDown(self):
        Basetest.tearDown(self)
        self.rt.close()
