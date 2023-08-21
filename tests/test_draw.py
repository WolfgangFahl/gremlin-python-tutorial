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
    
    def check_draw(self,gviz):
        """
        """
        debug=self.debug
        debug=True
        if debug:
            print(gviz.source)

    def testDraw(self):
        """
        test creating a graphviz graph from a gremlin graph
        """
        g=self.g
        self.examples.load_by_name(g, "tinkerpop-modern")
        gviz=GremlinDraw.show(g)
        self.check_draw(gviz)
        self.assertEqual(12,len(gviz.body))
    
    def testDrawTraversal(self):
        """
        test drawing a traversal
        """
        g=self.g
        self.examples.load_by_name(g, "tinkerpop-modern")
        traversal=g.E().hasLabel("created").toList()
        gviz=GremlinDraw.show_graph_traversal(g, traversal, "software")
        self.check_draw(gviz)
        
    def testGremlinDraw(self):
        g=self.g
        self.examples.load_by_name(g, "tinkerpop-modern")
        traversal=g.E().hasLabel("created").toList()
        gd=GremlinDraw()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()