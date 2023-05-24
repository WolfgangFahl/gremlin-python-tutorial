'''
Created on 2023-05-15

@author: wf
'''
import unittest
from gremlin.remote import RemoteTraversal
from gremlin.examples import Examples
from gremlin.draw import GremlinDraw

class TestDraw(unittest.TestCase):
    """
    test graphviz draw access
    """

    def testDraw(self):
        """
        test creating a graphviz graph from a gremlin graph
        """
        rt=RemoteTraversal()
        g=rt.g()
        Examples.load_modern(g)
        gviz=GremlinDraw.show(g)
        self.assertEqual(12,len(gviz.body))
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()