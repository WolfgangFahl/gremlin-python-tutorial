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
        l=self.g.V().toList()
        self.id1=l[0].id

    def log(self,thing):
        """
        convert thing to string and print out for debugging
        """
        text=str(thing)
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
        vList=gV.toList()
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
        vListStr=self.log(self.g.V(self.id1).toList())
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
        vList=self.g.V(self.id1).outE("knows").toList()
        if remoteTraversal.server.name=="Neo4j":
          assert(len(vList)==2)
        else:
          assert asString(l) == "[e[7][1-knows->2], e[8][1-knows->4]]"
    
    #    gremlin> g.V(1).outE('knows').inV().values('name') //5\
    #    ==>vadas
    #    ==>josh
    def test_tutorial5(self):
        l=g.V(id1).outE("knows").inV().values("name").toList()
        assert asString(l)=="['vadas', 'josh']" or asString(l)=="['josh', 'vadas']"
    
    #     gremlin> g.V(1).out('knows').values('name') //6\
    #    ==>vadas
    #    ==>josh
    def test_tutorial6(self):
        l=g.V(id1).out("knows").values("name").toList()
        assert asString(l)=="['vadas', 'josh']" or asString(l)=="['josh', 'vadas']"

