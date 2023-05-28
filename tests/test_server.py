'''
Created on 2023-05-17

@author: wf
'''
from tests.base_gremlin_test import BaseGremlinTest

class TestServer(BaseGremlinTest):
    """
    test server is available
    """

    def testSocket(self):
        """
        test socket open
        """
        is_open=self.remote_traversal.server.check_socket()
        self.assertTrue(is_open)
        pass