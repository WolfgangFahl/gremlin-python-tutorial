# minimal imports
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
# get the remote graph traversal
g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))
vCount=g.V().count().next()
print("The modern graph has %d vertices" % (vCount))
