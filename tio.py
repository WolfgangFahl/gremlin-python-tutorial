from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import os

g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

# test loading a graph
def test_loadGraph():
   # make the local file accessible to the server
   airRoutesPath=os.path.abspath("air-routes-small.xml")
   # drop the existing content of the graph
   g.V().drop().iterate()
   # read the content from the air routes example
   g.io(airRoutesPath).read().iterate()
   vCount=g.V().count().next()
   assert vCount==1000
