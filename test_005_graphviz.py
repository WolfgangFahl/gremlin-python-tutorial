# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from tutorial import remote
from graphviz import Digraph
import os.path


# initialize a remote traversal
g = remote.RemoteTraversal().g()

# test the number of vertices
def test_createGraphvizGraph():
    remoteTraversal=remote.RemoteTraversal()
    remoteTraversal.load("tinkerpop-modern.xml")
    dot = Digraph(comment='Modern')
    for v in g.V().toList():
        # quirky way to get properties see https://github.com/nedlowe/gremlin-python-example/blob/master/app.py
        vProps=g.V(v.id).valueMap().next()
        #print (vProps)
        dot.node("node%d" % (v.id),vProps["name"][0])
    for e in g.E():
        dot.edge("node%d" % (e.inV.id),"node%d" % (e.outV.id))
    print (dot.source)
    dot.render('/tmp/modern.gv', view=False)
    assert os.path.isfile('/tmp/modern.gv.pdf')

# call the test
test_createGraphvizGraph()
