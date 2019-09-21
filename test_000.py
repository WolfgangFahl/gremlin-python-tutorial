# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from tutorial import remote

# initialize a remote traversal
g = remote.RemoteTraversal().g()

# test the number of vertices
def test_LoadModern():
    remoteTraversal=remote.RemoteTraversal()
    remoteTraversal.load("tinkerpop-modern.xml")

# call the loadModern test
test_LoadModern()
