# see
# http://wiki.bitplan.com/index.php/Gremlin_python#Getting_Started
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import GraphTraversal

g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

# http://wiki.bitplan.com/index.php/Gremlin_python#g.V.28.29_-_the_vertices
#gremlin> g.V() //(1)
#    ==>v[1]
#    ==>v[2]
#    ==>v[3]
#    ==>v[4]
#    ==>v[5]
#    ==>v[6]
def test_tutorial1():
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

#gremlin> g.V(1) //(2)
#    ==>v[1]
def test_tutorial2():
   assert str(g.V(1).toList())=="[v[1]]"

#gremlin> g.V(1).values('name') //3
#  ==>marko
def test_tutorial3():
    assert str( g.V(1).values('name').toList())=="['marko']"

#     gremlin> g.V(1).outE('knows') //4
#    ==>e[7][1-knows->2]
#    ==>e[8][1-knows->4]
def test_tutorial4():
    assert str(g.V(1).outE("knows").toList()) == "[e[7][1-knows->2], e[8][1-knows->4]]"

#    gremlin> g.V(1).outE('knows').inV().values('name') //5\
#    ==>vadas
#    ==>josh
def test_tutorial5():
    assert str(g.V(1).outE("knows").inV().values("name").toList())=="['vadas', 'josh']"

#     gremlin> g.V(1).out('knows').values('name') //6\
#    ==>vadas
#    ==>josh
def test_tutorial6():
    assert str(g.V(1).out("knows").values("name").toList())=="['vadas', 'josh']"
