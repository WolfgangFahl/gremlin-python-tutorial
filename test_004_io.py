from tutorial import remote
import os

# initialize a remote traversal
g = remote.RemoteTraversal().g()

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

test_loadGraph()
