'''
Created on 2023-05-15

@author: wf
'''
import unittest
from gremlin.examples import Examples
from gremlin.draw import GremlinDraw
from tests.base_gremlin_test import BaseGremlinTest

class TestDraw(BaseGremlinTest):
    """
    test graphviz draw access
    """

    def testDraw(self):
        """
        test creating a graphviz graph from a gremlin graph
        """
        g=self.g
        self.examples.load_by_name(g, "tinkerpop-modern")
        gviz=GremlinDraw.show(g)
        self.assertEqual(12,len(gviz.body))
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()