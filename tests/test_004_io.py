from gremlin import gremote
import os

# initialize a gremote traversal
g = gremote.RemoteTraversal().g()

# test loading a graph
def test_loadGraph():
   graphmlFile="air-routes-small.xml";
   # make the local file accessible to the server
   airRoutesPath=os.path.abspath(graphmlFile)
   # drop the existing content of the graph
   g.V().drop().iterate()
   # read the content from the air routes example
   g.io(airRoutesPath).read().iterate()
   vCount=g.V().count().next()
   print ("%s has %d vertices" % (graphmlFile,vCount))
   assert vCount==47

# test saving a graph
def test_saveGraph():
   graphmlPath="/tmp/A-Fish-Named-Wanda.xml"
   # drop the existing content of the graph
   g.V().drop().iterate()
   g.addV("Fish").property("name","Wanda").iterate()
   g.io(graphmlPath).write().iterate()
   print("wrote graph to %s" % (graphmlPath))
   # check that the graphml file exists
   assert os.path.isfile(graphmlPath)

test_loadGraph()
test_saveGraph()
