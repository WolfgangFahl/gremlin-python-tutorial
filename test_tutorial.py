# see
# http://wiki.bitplan.com/index.php/Gremlin_python#Getting_Started
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import GraphTraversal

g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

# http://wiki.bitplan.com/index.php/Gremlin_python#g.V.28.29_-_the_vertices
def test_gV():
  # get the vertices
  gV=g.V()
  # we have a traversal now
  assert isinstance(gV,GraphTraversal)
  # convert it to a list to get the actual vertices
  vList=gV.toList()
  # there should be 6 vertices
  assert len(vList)==6
  # the default string representation of a vertex is showing the id
  # of a vertex
  assert str(vList)=="[v[1], v[2], v[3], v[4], v[5], v[6]]"
