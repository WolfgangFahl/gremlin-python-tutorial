# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_005_graphviz.py
from tutorial import remote
from graphviz import Digraph
import os.path
from gremlin_python.process.traversal import T

# initialize a remote traversal
g = remote.RemoteTraversal().g()

# test the number of vertices
def test_createGraphvizGraph():
    remoteTraversal=remote.RemoteTraversal()
    remoteTraversal.load("tinkerpop-modern.xml")
    dot = Digraph(comment='Modern')
    # get vertice properties including id and label
    for vDict in g.V().valueMap(True).toList():
        # print vDict
        vId=vDict[T.id]
        vLabel=vDict[T.label]
        gvLabel="%s\n%s\nname=%s" % (vId,vLabel,vDict["name"][0])
        if "age" in vDict:
            gvLabel=gvLabel+"\nage=%s" % (vDict["age"][0])
        dot.node("node%d" % (vId),gvLabel)
    for e in g.E():
        eDict=g.E(e.id).valueMap(True).next()
        print (e,eDict)
        geLabel="%s\n%s\nweight=%s" % (e.id,e.label,eDict["weight"])
        dot.edge("node%d" % (e.outV.id),"node%d" % (e.inV.id),label=geLabel)
    dot.edge_attr.update(arrowsize='2',penwidth='2')
    dot.node_attr.update(style='filled',fillcolor="#A8D0E4")
    print (dot.source)
    dot.render('/tmp/modern.gv', view=False)
    assert os.path.isfile('/tmp/modern.gv.pdf')

# call the test
test_createGraphvizGraph()
