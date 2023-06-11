# see
# http://wiki.bitplan.com/index.php/Gremlin_python#Getting_Started
from tests.base_gremlin_test import BaseGremlinTest
from gremlin_python.process.graph_traversal import GraphTraversal

class TestTutorial(BaseGremlinTest):
    """
    test connection handling
    """
    
    def setUp(self, debug=False, profile=True):
        """
        setUp the test environment
        """
        BaseGremlinTest.setUp(self, debug=debug, profile=profile)
        # in TinkerGraph this is the first id
        # get id of Marko's vertex which is usually 1 but might be different e.g.
        # when Neo4j is used
        self.examples.load_by_name(self.g, "tinkerpop-modern")
        l=self.g.V().toList()
        self.id1=l[0].id

    def log(self,thing):
        """
        convert thing to string and print out for debugging
        """
        text=str(thing)
        if self.debug:
            print (text)
        return text

    def test_tutorial1(self):
        """
        g.V() //(1)
            ==>v[1]
            ==>v[2]
            ==>v[3]
            ==>v[4]
            ==>v[5]
            ==>v[6]
        """
        # get the vertices
        gV=self.g.V()
        # we have a traversal now
        self.assertTrue(isinstance(gV,GraphTraversal))
        # convert it to a list to get the actual vertices
        vList=gV.to_list()
        # there should be 6 vertices
        self.assertEqual(6,len(vList))
        # the default string representation of a vertex is showing the id
        # of a vertex
        vListStr=self.log(vList)
        expected=f"[v[{self.id1}], v[{self.id1+1}], v[{self.id1+2}], v[{self.id1+3}], v[{self.id1+4}], v[{self.id1+5}]]"
        self.assertEqual(vListStr,expected)
    
    def test_tutorial2(self):
        """
        gremlin> g.V(1) //(2)
            ==>v[1]
        """
        vListStr=self.log(self.g.V(self.id1).to_list())
        expected=f"[v[{self.id1}]]"
        self.assertEqual(vListStr,expected)
    
    
    def test_tutorial3(self):
        """
        gremlin> g.V(1).values('name') //3
          ==>marko
        """
        vListStr=self.log(self.g.V(self.id1).values('name').toList())
        expected="['marko']"
        self.assertEqual(vListStr,expected)
    
    def test_tutorial4(self):
        """
        gremlin> g.V(1).outE('knows') //4
            ==>e[7][1-knows->2]
            ==>e[8][1-knows->4]
        """
        vList=self.g.V(self.id1).outE("knows").to_list()
        vListStr=self.log(vList)
        if self.remote_traversal.server.name=="Neo4j":
            self.assertEqual(2,len(vList))
        else:
            expected= "[e[7][1-knows->2], e[8][1-knows->4]]"
            self.assertEqual(vListStr,expected)
    
    def test_tutorial5(self):
        """
        gremlin> g.V(1).outE('knows').inV().values('name') //5\
            ==>vadas
            ==>josh
        """
        vList=self.g.V(self.id1).outE("knows").inV().values("name").to_list()
        vListStr=self.log(vList)
        self.assertTrue(vListStr=="['vadas', 'josh']" or vListStr=="['josh', 'vadas']")
    
    def test_tutorial6(self):
        """
        gremlin> g.V(1).out('knows').values('name') //6\
            ==>vadas
            ==>josh
        """
        vList=self.g.V(self.id1).out("knows").values("name").to_list()
        vListStr=self.log(vList)
        self.assertTrue(vListStr=="['vadas', 'josh']" or vListStr=="['josh', 'vadas']")