# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_005_graphviz.py
from graphviz import Digraph
import os.path
import platform
from gremlin_python.process.traversal import T
from tests.base_gremlin_test import BaseGremlinTest

class TestGraphvizGraph(BaseGremlinTest):
    """
    test creating a graphviz graph from the tinkerpop graph
    """

    def test_createGraphvizGraph(self):
        # make sure we re-load the tinkerpop modern example
        g=self.g
        self.examples.load_by_name(g,f"tinkerpop-modern")
        # start a graphviz
        dot = Digraph(comment='Modern')
        # get vertice properties including id and label as dicts
        for vDict in g.V().valueMap(True).toList():
            # uncomment to debug
            # print vDict
            # get id and label
            vId=vDict[T.id]
            vLabel=vDict[T.label]
            # greate a graphviz node label
            # name property is alway there
            gvLabel=r"%s\n%s\nname=%s" % (vId,vLabel,vDict["name"][0])
            # if there is an age property add it to the label
            if "age" in vDict:
                gvLabel=gvLabel+r"\nage=%s" % (vDict["age"][0])
            # create a graphviz node
            dot.node("node%d" % (vId),gvLabel)
        # loop over all edges
        for e in g.E():
            # get the detail information with a second call per edge (what a pitty to be so inefficient ...)
            eDict=g.E(e.id).valueMap(True).next()
            # uncomment if you'd like to debug
            # print (e,eDict)
            # create a graphviz label
            geLabel=r"%s\n%s\nweight=%s" % (e.id,e.label,eDict["weight"])
            # add a graphviz edge
            dot.edge("node%d" % (e.outV.id),"node%d" % (e.inV.id),label=geLabel)
        # modify the styling see http://www.graphviz.org/doc/info/attrs.html
        dot.edge_attr.update(arrowsize='2',penwidth='2')
        dot.node_attr.update(style='filled',fillcolor="#A8D0E4")
        # print the source code
        if self.debug:
            print (dot.source)
        if platform.system() == "Darwin":  # Darwin represents macOS
            os.environ["PATH"] += os.pathsep + '/opt/local/bin'

        # render without viewing - default is creating a pdf file
        dot.render('/tmp/modern.gv', view=False)
        # check that the pdf file exists
        assert os.path.isfile('/tmp/modern.gv.pdf')