'''
Created on 2023-03-23

@author: wf
'''
from os.path import dirname, abspath
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
        script_path = dirname(abspath(__file__))
        self.remote_traversal=RemoteTraversal(config_path=f"{script_path}/../config")
        self.g=self.remote_traversal.g()
        self.data_path=abspath(f"{script_path}/../data")
        
    def tearDown(self):
        Basetest.tearDown(self)
        self.remote_traversal.close()
