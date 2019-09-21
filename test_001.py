# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from tutorial import remote

# initialize a remote traversal
g = remote.RemoteTraversal().g()

# test the number of vertices
def test_VCount():
  vCount=g.V().count().next()
  print ("g.V().count=%d" % (vCount))
  assert vCount == 6

# test the number of edges
def test_ECount():
  eCount=g.E().count().next()
  print ("g.E().count=%d" % (eCount))
  assert eCount == 6

# call the vertice count test
test_VCount()
# call the edge count test
test_ECount()
