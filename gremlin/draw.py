'''
Created on 2023-05-15

@author: jv
'''
import graphviz
class GremlinDraw:
    @classmethod
    def show(cls,g,title:str="Gremlin", v_limit:int=10, e_limit:int=10):
        G = graphviz.Digraph(title,format="pdf")
        
        # draw vertices
        vlist = g.V().toList()
        vlist = vlist[:v_limit]
        
        for v in vlist:
            kvp_list = list(g.V(v).elementMap().next().items())
            kvp_list.pop(0) # pop ID
            kvp_list.pop(0) # pop label
            vertex_properties = ""
            for key,val in kvp_list:
                vertex_properties += "\n " + str(key) + ": " + str(val);
            
            G.node(name=str(v.id), label=str(v.id) + "\n" + v.label + "\n" + '─' * 5 + vertex_properties, fillcolor = "#ADE1FE", style = "filled", fontname = "arial")
            
        #draw edges
        elist = g.E().elementMap().toList()
        elist = elist[:e_limit]
        
        for e in elist:
            kvp_list = list(e.items())
            kvp_list.pop(0) # pop ID
            kvp_list.pop(0) # pop label
            kvp_list.pop(0) # pop in
            kvp_list.pop(0) # pop out
            edge_properties = ""
            for key,val in kvp_list:
                edge_properties += "\n " + str(key) + ": " + str(val);
                
                # list(list(e.values())[2].values())[0]
                # str(g.E(e).inV().next().id)
                # str(g.E(e).outV().next().id)
                # list(e.values())[0]
            
            G.edge(tail_name = str(list(list(e.values())[3].values())[0]), head_name = str(list(list(e.values())[2].values())[0]), style = "setlinewidth(3)", label = str(list(e.values())[0]) + "\n" + str(list(e.values())[1]) +  "\n" + '─' * 5 + edge_properties, fontname = "arial")
        return G