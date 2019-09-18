from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

def test_VCount():
  vCount=g.V().count().next()
  assert vCount == 6

def test_ECount():
  eCount=g.E().count().next()
  assert eCount == 6
