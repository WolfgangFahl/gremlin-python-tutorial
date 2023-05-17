# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from gremlin import gremote

# initialize a gremote traversal
g = gremote.RemoteTraversal().g()

# test the number of vertices
def test_LoadModern():
    remoteTraversal=gremote.RemoteTraversal()
    remoteTraversal.load("tinkerpop-modern.xml")

# call the loadModern test
test_LoadModern()
