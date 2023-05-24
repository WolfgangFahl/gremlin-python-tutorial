# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from tests.base_gremlin_test import BaseGremlinTest

class TestModern(BaseGremlinTest):
    """
    test Remote Traversal
    """

    def test_LoadModern(self):
        """
        test loading the tinkerpop-modern graph
        """
        g=self.g
        self.rt.load(g,"../data/tinkerpop-modern.xml")
        vCount=g.V().count().next()
        if self.debug:
            print ("g.V().count=%d" % (vCount))
        self.assertEqual(6,vCount)
        eCount=g.E().count().next()
        if self.debug:
            print ("g.E().count=%d" % (eCount))
        self.assertEquals(6,eCount)

