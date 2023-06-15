'''
Created on 2023-03-23

@author: wf
'''
from tests.basetest import Basetest
from gremlin.remote import RemoteTraversal, Server
from gremlin.examples import Examples, Volume

class BaseGremlinTest(Basetest):
    """
    Basetest for Gremlin Python
    """
    
    def setUp(self, debug=False, profile=True):
        """
        prepare the test environment
        """
        Basetest.setUp(self, debug, profile)
        self.server=Server()
        self.remote_traversal=RemoteTraversal(self.server)
        self.g=self.remote_traversal.g()
        self.volume=Volume.docker()
        self.examples=Examples(volume=self.volume,debug=self.debug)
        
    def tearDown(self):
        """
        tear down
        """
        Basetest.tearDown(self)
        self.remote_traversal.close()
