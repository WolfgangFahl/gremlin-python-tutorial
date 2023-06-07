'''
Created on 2023-01-15

@author: wf
'''
from tests.base_gremlin_test import BaseGremlinTest
from gremlin.examples import Examples

class TestExamples(BaseGremlinTest):
    """
    test the Examples

    """
    
    def setUp(self, debug=True, profile=True):
        BaseGremlinTest.setUp(self, debug=debug, profile=profile)
        self.examples=Examples(remote_path=self.data_path,debug=self.debug)
        if not self.inPublicCI():
            self.examples.remote_examples_path=self.examples.local_examples_path
                
    def test_modern(self):
        """
        test loading the modern graph
        """
        g=self.g
        self.examples.load_by_name(g,"tinkerpop-modern")
        v_count=g.V().count().next()
        g.V().toList()
        if self.debug:
            print (f"graph imported has {v_count} vertices")
        assert v_count==6
        
    def test_grateful_dead(self):
        """
        test loading grateful dead example
        """
        g=self.g
        self.examples.load_by_name(g, "grateful-dead")
        v_count=g.V().count().next()
        g.V().toList()
        print (f"graph imported has {v_count} vertices")
        assert v_count==808
        
    def test_air_routes_small(self):
        """
        test air routes example
        """
        g=self.g
        self.examples.load_by_name(g, "air-routes-small")
        v_count=g.V().count().next()
        g.V().toList()
        print (f"graph imported has {v_count} vertices")
        assert v_count==47
        
    def test_air_route_latest(self):
        """
        test air route latest
        """
        g=self.g
        self.examples.load_by_name(g, "air-routes-latest")
        v_count=g.V().count().next()
        g.V().toList()
        print (f"graph imported has {v_count} vertices")
        assert v_count==3749