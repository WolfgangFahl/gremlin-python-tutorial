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
        self.remote_traversal=RemoteTraversal()
        self.g=self.remote_traversal.g()
        script_path = dirname(abspath(__file__))
        self.data_path=abspath(f"/opt/gremlin-server/data/examples/")
        
    def tearDown(self):
        """
        tear down
        """
        Basetest.tearDown(self)
        self.remote_traversal.close()
