# see
# http://wiki.bitplan.com/index.php/Gremlin_python#Getting_Started
from gremlin import gremote
from gremlin_python.process.graph_traversal import GraphTraversal

# initialize a gremote traversal
remoteTraversal=gremote.RemoteTraversal()
g = remoteTraversal.g()
# in TinkerGraph this is the first id
id1=1

# convert object to string and print out for debugging
def asString(object):
  text=str(object)
  print (text)
  return text

# get id of Marko's vertex which is usually 1 but might be different e.g.
# when Neo4j is used
def test_tutorial0():
   global id1
   l=g.V().toList()
   id1=l[0].id
   # Marko's id might not be 1
   # print (id1)

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
  assert asString(vList)=="[v[%d], v[%d], v[%d], v[%d], v[%d], v[%d]]" % (id1,id1+1,id1+2,id1+3,id1+4,id1+5)

#gremlin> g.V(1) //(2)
#    ==>v[1]
def test_tutorial2():
   assert asString(g.V(id1).toList())=="[v[%d]]" % (id1)

#gremlin> g.V(1).values('name') //3
#  ==>marko
def test_tutorial3():
    assert asString( g.V(id1).values('name').toList())=="['marko']"

#     gremlin> g.V(1).outE('knows') //4
#    ==>e[7][1-knows->2]
#    ==>e[8][1-knows->4]
def test_tutorial4():
    l=g.V(id1).outE("knows").toList()
    if remoteTraversal.server.name=="Neo4j":
      assert(len(l)==2)
    else:
      assert asString(l) == "[e[7][1-knows->2], e[8][1-knows->4]]"

#    gremlin> g.V(1).outE('knows').inV().values('name') //5\
#    ==>vadas
#    ==>josh
def test_tutorial5():
    l=g.V(id1).outE("knows").inV().values("name").toList()
    assert asString(l)=="['vadas', 'josh']" or asString(l)=="['josh', 'vadas']"

#     gremlin> g.V(1).out('knows').values('name') //6\
#    ==>vadas
#    ==>josh
def test_tutorial6():
    l=g.V(id1).out("knows").values("name").toList()
    assert asString(l)=="['vadas', 'josh']" or asString(l)=="['josh', 'vadas']"

test_tutorial0()
test_tutorial1()
test_tutorial2()
test_tutorial3()
test_tutorial4()
test_tutorial5()
test_tutorial6()
