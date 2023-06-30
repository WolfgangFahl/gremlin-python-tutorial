'''
Created on 2023-05-15

@author: jv
'''
from collections.abc import Iterable
from typing import Any, List, Union

import graphviz

from gremlin_python.process.anonymous_traversal import GraphTraversalSource
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.process.traversal import T
from gremlin_python.structure.graph import Vertex, Edge, Path

from aenum import Enum


class GremlinDraw:
    @staticmethod
    def __draw_vertex(digraph: graphviz.Digraph, g: GraphTraversalSource, vertex: Vertex) -> graphviz.Digraph:
        """
        draw a single given vertex
        """
        # developer note: see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/python/gremlin_python/structure/graph.py#LL58C23-L58C23
        # when gremlin-python 3.7.0 is released, the following code can be improved (get the properties using vertex.properties)
        # then, g can also be removed as a parameter
        
        # get the properties of the vertex
        kvp_list = list(next(g.V(vertex).element_map()).items())
        # non-proerty items are of type aenum
        properties = [item for item in kvp_list if not isinstance(item[0], Enum)]
        assert len(properties) == len(kvp_list) - 2 # ID and label are not properties
    
        properties_label = "\n".join(f"{key}: {value}" for key, value in properties)

        # draw the vertex
        digraph.node(
            name=str(vertex.id),
            label=f"{str(vertex.id)}\n{vertex.label}\n{'─' * 5}\n{properties_label}",
            fillcolor = "#ADE1FE",
            style = "filled",
            fontname = "arial"
        )

        return digraph

    
    @staticmethod
    def __draw_edge(digraph: graphviz.Digraph, g: GraphTraversalSource, edge: Edge) -> graphviz.Digraph:
        """
        draw a single given edge
        """
        # developer note: see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/python/gremlin_python/structure/graph.py#L66
        # when gremlin-python 3.7.0 is released, the following code can be improved (get the properties using edge.properties)
        # then, g can also be removed as a parameter

        # get the properties of the edge
        #kvp_list = list(next(g.E(edge).element_map()).items())
        # Workaround, because the above line does not work due to inconsistencies / bugs in the gremlin-python library
        kvp_list = [edge_element_map for edge_element_map in g.E().element_map().to_list() if edge_element_map[T.id] == edge.id][0].items()
        # non-proerty items are of type aenum
        properties = [item for item in kvp_list if not isinstance(item[0], Enum)]
        assert len(properties) == len(kvp_list) - 4 # ID, label, in, and out are not properties
        
        properties_label = "\n".join(f"{key}: {value}" for key, value in properties)
        
        # get the image of the edge by id
        in_vertex_id = edge.inV.id
        out_vertex_id = edge.outV.id

        # draw the edge
        digraph.edge(
            tail_name = str(out_vertex_id),
            head_name = str(in_vertex_id),
            label = f"{str(edge.id)}\n{edge.label}\n{'─' * 5}\n{properties_label}",
            style = "setlinewidth(3)",
            fontname = "arial"
        )

        return digraph


    @staticmethod
    def show(g: GraphTraversalSource, title:str="Gremlin", v_limit:int=10, e_limit:int=10) -> graphviz.Digraph:
        """
        draw the given graph
        """
        G: graphviz.Digraph = graphviz.Digraph(title, format="pdf")
        
        # draw vertices
        vlist = g.V().to_list()
        vlist = vlist[:v_limit]
        
        for v in vlist:
            G = GremlinDraw.__draw_vertex(G, g, v)

        #draw edges
        elist = g.E().to_list()
        elist = elist[:e_limit]
        
        for e in elist:
            G = GremlinDraw.__draw_edge(G, g, e)
        
        return G

    @staticmethod
    def show_graph_traversal(g: GraphTraversalSource, gt: Union[GraphTraversal, Any], title: str="Gremlin") -> graphviz.Digraph:
        """
        draw the given graph traversal
        """
        # developer note: when moving the minium supported version up to 3.10, the following code can be greatly improved by using match statements

        G: graphviz.Digraph = graphviz.Digraph(title, format="pdf")

        worklist: List[Any] = gt.to_list() if isinstance(gt, GraphTraversal) else list(gt) if isinstance(gt, Iterable) else [gt]

        while len(worklist) > 0:
            # move any vertices to the front of the worklist (draw them first)
            worklist = [item for item in worklist if not isinstance(item, Vertex)] + [item for item in worklist if isinstance(item, Vertex)]

            result = worklist.pop(0)

            if isinstance(result, Vertex):
                G = GremlinDraw.__draw_vertex(G, g, result)
            elif isinstance(result, Edge):
                G = GremlinDraw.__draw_edge(G, g, result)
            elif isinstance(result, Path):
                for item in result.objects:
                    worklist.append(item)
            elif isinstance(result, dict):
                if T.id in result:
                    # check if the id is a vertex or an edge
                    if g.V(result[T.id]).hasNext():
                        G = GremlinDraw.__draw_vertex(G, g, next(g.V(result[T.id])))
                    elif g.E(result[T.id]).hasNext():
                        G = GremlinDraw.__draw_edge(G, g, g.E(result[T.id]).next())
                    else:
                        #raise Exception("id not found")
                        pass # silent skip
                else:
                    #raise Exception("id not found")
                    pass # silent skip
            else:
                #raise Exception(f"unknown type: {type(result)}")
                pass # silent skip

        return G


