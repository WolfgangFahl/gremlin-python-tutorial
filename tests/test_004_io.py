import os
from tests.base_gremlin_test import BaseGremlinTest
import tempfile
class TestIo(BaseGremlinTest):
    """
    test Io handling
    """
    
    # test loading a graph
    def test_loadGraph(self):
        g=self.g
        airroutes="air-routes-small"
        self.examples.load_by_name(g,f"{airroutes}")
        graphmlFile=f"{self.data_path}/{airroutes}.xml";
        # make the local file accessible to the server
        airRoutesPath=os.path.abspath(graphmlFile)
        # drop the existing content of the graph
        g.V().drop().iterate()
        # read the content from the air routes example
        g.io(airRoutesPath).read().iterate()
        vCount=g.V().count().next()
        print (f"{graphmlFile} has {vCount} vertices")
        assert vCount==47
    
    # test saving a graph
    def test_saveGraph(self):
        g=self.g
        graphmlPath = os.path.join(tempfile.mkdtemp(), 'A-Fish-Named-Wanda.xml')
        # drop the existing content of the graph
        g.V().drop().iterate()
        g.addV("Fish").property("name","Wanda").iterate()
        g.io(graphmlPath).write().iterate()
        print(f"wrote graph to {graphmlPath}")
        # check that the graphml file exists
        assert os.path.isfile(graphmlPath)


