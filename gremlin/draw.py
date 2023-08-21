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
from dataclasses import dataclass
from aenum import Enum

@dataclass
class GremlinDrawConfig:
    """
    draw configuration parameters
    """
    fontname: str="arial"
    fillcolor:str ="#ADE1FE"
    output_format:str ='pdf'
    edge_line_width: int=3
    dash_width: int=5 # number of dashes to apply
    v_limit:int=10 # maximum number of vertices to show
    e_limit:int=10 # maximum number of edges to show
    # optionally set the properties to be displayed
    vertex_properties: List[str] = None  # New filter for vertex properties
    edge_properties: List[str] = None  # New filter for edge properties

class GremlinDraw:
    """
    helper class to draw Gremlin Graphs via Graphviz
    """
    
    def __init__(self,g: GraphTraversalSource,title:str,config:GremlinDrawConfig=None):
        """
        constructor
        """
        self.g=g
        self.title=title
        if config is None:
            config=GremlinDrawConfig()
        self.config=config
        self.gviz: graphviz.Digraph = graphviz.Digraph(title, format=config.output_format)
        # keep track of the vertices and edges drawn
        self.v_drawn={}
        self.e_drawn={}
        
    def __as_label(self,head,body:str)->str:
        """
        create a label from head and body separated by a dash
        with the configured width
        """
        # note the UTF-8 dash ...
        dash="─"*self.config.dash_width
        label=f"{head}\n{dash}\n{body}"
        return label
    
    def get_vertex_properties(self,vertex:Vertex)->list:
        """
        get the properties for a given vertex
        """
        # developer note: see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/python/gremlin_python/structure/graph.py#LL58C23-L58C23
        # has properties but these are not set as for gremlin-python 3.7.0 
        
        # get the properties of the vertex (work around)
        kvp_list = list(next(self.g.V(vertex).element_map()).items())
        # non-property items are of type aenum
        properties = [item for item in kvp_list if not isinstance(item[0], Enum)]
        assert len(properties) == len(kvp_list) - 2 # ID and label are not properties
        if self.config.vertex_properties is not None:
            properties = [item for item in properties if item[0] in self.config.vertex_properties]
        return properties
    
    def get_edge_properties(self,edge:Edge)->list:
        # developer note: see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/python/gremlin_python/structure/graph.py#L66
        # when gremlin-python 3.7.0 is released, the following code might be improved (get the properties using edge.properties)
        # e_props=edge.properties
        # 2023-08-21: WF tested - but properties are not set ...
        # then, g can also be removed as a parameter
        # get the properties of the edge
        edge_t=self.g.E(edge)
        try: 
            edge_map=edge_t.element_map().next()
            kvp_list = list(edge_map.items())
        except StopIteration:
            pass
            return[]
        
        # Workaround, because the above line does not work due to inconsistencies / bugs in the gremlin-python library
        #kvp_list = [edge_element_map for edge_element_map in self.g.E().element_map().to_list() if edge_element_map[T.id] == edge.id][0].items()
        # non-property items are of type aenum
        properties = [item for item in kvp_list if not isinstance(item[0], Enum)]
        assert len(properties) == len(kvp_list) - 4 # ID, label, in, and out are not properties
        if self.config.edge_properties is not None:
            properties = [item for item in properties if item[0] in self.config.edge_properties]
        return properties
    
    def draw_vertex(self, vertex: Vertex):
        """
        draw a single given vertex
        """
        # avoid drawing to many vertices
        if len(self.v_drawn)>=self.config.v_limit:
            return
        if vertex.id in self.v_drawn:
            return
        properties=self.get_vertex_properties(vertex)
        properties_label = "\n".join(f"{key}: {value}" for key, value in properties)
        head=f"{str(vertex.id)}\n{vertex.label}"
        body=f"{properties_label}"
        label=self.__as_label(head, body)
        # draw the vertex
        self.gviz.node(
            name=str(vertex.id),
            label=f"{label}",
            fillcolor = f"{self.config.fillcolor}",
            style = "filled",
            fontname = f"{self.config.fontname}"
        )
        self.v_drawn[vertex.id]=vertex
    
    def draw_edge(self, edge: Edge,with_vertices:bool=True):
        """
        draw a single given edge
        """
        # avoid drawing to many vertices
        if len(self.e_drawn)>=self.config.e_limit:
            return
        if edge.id in self.e_drawn:
            return
        if with_vertices:
            self.draw_vertex(edge.inV)
            self.draw_vertex(edge.outV)
            pass
        properties=self.get_edge_properties(edge)
        properties_label = "\n".join(f"{key}: {value}" for key, value in properties)
        head=f"{str(edge.id)}\n{edge.label}"
        body=properties_label
        label=self.__as_label(head,body)
        # get the image of the edge by id
        in_vertex_id = edge.inV.id
        out_vertex_id = edge.outV.id
        
        # draw the edge
        self.gviz.edge(
            tail_name = str(out_vertex_id),
            head_name = str(in_vertex_id),
            label = f"{label}",
            style = f"setlinewidth({self.config.edge_line_width})",
            fontname = f"{self.config.fontname}"
        )
        self.e_drawn[edge.id]=edge
        
    def draw_g(self):
        # draw vertices
        vlist = self.g.V().to_list()
        vlist = vlist[:self.config.v_limit]
        
        for v in vlist:
            self.draw_vertex(v)

        #draw edges
        elist = self.g.E().to_list()
        elist = elist[:self.config.e_limit]
        
        for e in elist:
            self.draw_edge(e)
            
    def draw(self,gt: Union[GraphTraversal, Any]):
        # developer note: when moving the minimum supported version up to 3.10, the following code can be greatly improved by using match statements
        worklist: List[Any] = gt.to_list() if isinstance(gt, GraphTraversal) else list(gt) if isinstance(gt, Iterable) else [gt]

        while len(worklist) > 0:
            # move any vertices to the front of the worklist (draw them first)
            worklist = [item for item in worklist if not isinstance(item, Vertex)] + [item for item in worklist if isinstance(item, Vertex)]

            result = worklist.pop(0)

            if isinstance(result, Vertex):
                self.draw_vertex(result)
            elif isinstance(result, Edge):
                self.draw_edge(result)
            elif isinstance(result, Path):
                for item in result.objects:
                    worklist.append(item)
            elif isinstance(result, dict):
                if T.id in result:
                    # check if the id is a vertex or an edge
                    if self.g.V(result[T.id]).hasNext():
                        self.draw_vertex(next(self.g.V(result[T.id])))
                    elif self.g.E(result[T.id]).hasNext():
                        self.draw_edge(self.g.E(result[T.id]).next())
                    else:
                        #raise Exception("id not found")
                        pass # silent skip
                else:
                    #raise Exception("id not found")
                    pass # silent skip
            else:
                #raise Exception(f"unknown type: {type(result)}")
                pass # silent skip
        
    @staticmethod
    def show(g: GraphTraversalSource, title:str="Gremlin", v_limit:int=10, e_limit:int=10) -> graphviz.Digraph:
        """
        draw the given graph
        """
        gd=GremlinDraw(g=g,title=title)
        gd.config.v_limit=v_limit
        gd.config.e_limit=e_limit
        gd.draw_g()
        return gd.gviz

    @staticmethod
    def show_graph_traversal(g: GraphTraversalSource, gt: Union[GraphTraversal, Any], title: str="Gremlin") -> graphviz.Digraph:
        """
        draw the given graph traversal
        """
        gd=GremlinDraw(g=g,title=title)
        gd.draw(gt)
        return gd.gviz
