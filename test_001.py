from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

def test_VCount():
  g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
  vCount=g.V().count().next()
  print(vCount)
  assert vCount == 6 
