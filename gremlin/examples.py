import urllib.request
import os
from pathlib import Path

from gremlin_python.process.anonymous_traversal import GraphTraversalSource
from gremlin.remote import RemoteTraversal
from dataclasses import dataclass

@dataclass
class Example:
    name:str
    url:str
    
    def load(
        self,
        g: GraphTraversalSource,
        local_path: str,
        remote_path: str,
        force: bool = False
    ) -> None:
        """
        download graph from remote_path to local_path depending on force flag
        and load graph into g
        
        Args:
            g(GraphTraversalSource): the target graph (inout)
            local_path(str): the path to the local copy
            remote_path(str): the path to the remote copy (e.g. in a docker container)
            force(bool): if True download even if local copy already exists
        """
        self.download(local_path, force)
        graph_xml=f"{remote_path}/{self.name}.xml"
        RemoteTraversal.load(g, graph_xml)
    
    def download(self, path, force: bool = False) -> str:
        """
        load the graphml xml file from the given url and store it to the given file_name (prefix)
        
        Args:
            url(str): the url to use
            file_name(str): the name of the file to load
            force(bool): if True overwrite
            
        Returns:
            str: the filename loaded
        """
        graph_xml=f"{path}/{self.name}.xml"
        # check whether file exists and is size 0 which indicates
        # a failed download attempt
        if os.path.exists(graph_xml):
            stats=os.stat(graph_xml)
            size=stats.st_size
            force=force or size==0
        if not os.path.exists(graph_xml) or force:
            graph_data = urllib.request.urlopen(self.url).read().decode("utf-8")
            print(graph_data,  file=open(graph_xml, 'w'))
        return graph_xml
    
class Examples:
    """
    Examples 
    """
    
    def __init__(self, remote_path = "/opt/gremlin-server/data"):
        home = str(Path.home())
        self.local_examples_path=f"{home}/.gremlin-examples"
        os.makedirs(self.local_examples_path, exist_ok=True)  
        self.remote_examples_path=remote_path
        self.examples_by_name={}
        for example in [
            Example(name="tinkerpop-modern",url="https://raw.githubusercontent.com/apache/tinkerpop/master/data/tinkerpop-modern.xml"),
            Example(name="grateful-dead",url="https://raw.githubusercontent.com/apache/tinkerpop/master/data/grateful-dead.xml"),
            Example(name="air-routes-small",url="https://raw.githubusercontent.com/krlawrence/graph/master/sample-data/air-routes-small.graphml"),
            Example(name="air-routes-latest",url="https://raw.githubusercontent.com/krlawrence/graph/master/sample-data/air-routes-latest.graphml")
        ]:
            self.examples_by_name[example.name]=example
        
    def load_by_name(self,g: GraphTraversalSource, name: str) -> None:
        """
        load an example by name to the given graph
        
        Args:
            g(GraphTraversalSource): the target graph (inout)
            name(str): the name of the example

        Raises:
            Exception: if the example does not exist
        """
        if name in self.examples_by_name:
            example=self.examples_by_name[name]
            example.load(g,self.local_examples_path,self.remote_examples_path)
        else:
            raise Exception(f"invalid example {name}")
