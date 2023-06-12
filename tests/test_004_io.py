import os
from tests.base_gremlin_test import BaseGremlinTest
class TestIo(BaseGremlinTest):
    """
    test Io handling
    """
    
    # test loading a graph
    def test_loadGraph(self):
        g=self.g
        airroutes="air-routes-small"
        self.examples.load_by_name(g,f"{airroutes}")
        graphmlFile=f"{self.volume.remote_path}/{airroutes}.xml";
        # make the local file accessible to the server
        airRoutesPath=os.path.abspath(graphmlFile)
        # drop the existing content of the graph
        g.V().drop().iterate()
        # read the content from the air routes example
        g.io(airRoutesPath).read().iterate()
        vCount=g.V().count().next()
        if self.debug:
            print (f"{graphmlFile} has {vCount} vertices")
        assert vCount==47
    
    # test saving a graph
    def test_saveGraph(self):
        g=self.g
        graphMl="/tmp/a_fish_named_wanda.xml"
        # drop the existing content of the graph
        g.V().drop().iterate()
        g.addV("Fish").property("name","Wanda").iterate()
        g.io(graphMl).write().iterate()
        if self.debug:
            print(f"wrote graph to {graphMl}")
        g.V().drop().iterate()
        g.io(graphMl).read().iterate()
        vCount=g.V().count().next()
        debug=self.debug
        debug=True
        if debug:
            print (f"{graphMl} has {vCount} vertices")
        assert vCount==1
        # check that the graphml file exists
        # unfortunately this doesn't work as of 2023-06-11
        # in the github CI
        #assert os.path.isfile(self.volume.local(graphMl))