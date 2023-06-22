from os.path import abspath, dirname
import urllib.request
import os
from pathlib import Path

from gremlin_python.process.anonymous_traversal import GraphTraversalSource
from gremlin.remote import RemoteTraversal
from dataclasses import dataclass

@dataclass
class Volume:
    """
    map a local path on the client to a remote
    path on a server e.g. when using a Volume in a docker
    container
    """
    local_path: str
    remote_path: str
    
    def local(self,file_name:str):
        """
        return the local mapping of the given file_name
        
        Args:
            file_name(str): the file name to map
        Returns:
            str: the local path
        """
        path=f"{self.local_path}/{file_name}"
        return path
    
    def remote(self,file_name:str):
        """
        return the remote mapping of the given file_name
        
        Args:
            file_name(str): the file name to map
        Returns:
            str: the remote path
        """
        path=f"{self.remote_path}/{file_name}"
        return path
        
    
    @staticmethod
    def docker()->"Volume":
        """
        get the default docker volume mapping
        
        Returns:
            Volume: the local_path/remote_path mapping
        """
        home = str(Path.home())
        local_path=f"{home}/.gremlin-examples"
        os.makedirs(local_path, exist_ok=True)  
        remote_path="/opt/gremlin-server/data/examples"
        volume=Volume(local_path=local_path,remote_path=remote_path)
        return volume
    
    @staticmethod
    def local() -> "Volume":
        """
        get the default local volume mapping

        Returns:
            Volume: the local_path/remote_path mapping
        """
        home = str(Path.home())
        local_path=f"{home}/.gremlin-examples"
        os.makedirs(local_path, exist_ok=True)
        remote_path=str(abspath(f"{dirname(abspath(__file__))}/data"))
        volume=Volume(local_path=local_path,remote_path=remote_path)
        return volume
    
@dataclass
class Example:
    name:str
    url:str
    
    def load(
        self,
        g: GraphTraversalSource,
        volume: Volume,
        force: bool = False,
        debug: bool = False,
    ) -> None:
        """
        download graph from remote_path to local_path depending on force flag
        and load graph into g
        
        Args:
            g(GraphTraversalSource): the target graph (inout)
            volume:Volume
            force(bool): if True download even if local copy already exists
            debug(bool): if True show debugging information
        """
        self.download(volume.local_path, force=force,debug=debug)
        graph_xml=f"{volume.remote_path}/{self.name}.xml"
        RemoteTraversal.load(g, graph_xml)
    
    def download(self,path,force:bool=False,debug:bool=False)->str:
        """
        load the graphml xml file from the given url and store it to the given file_name (prefix)
        
        Args:
            url(str): the url to use
            file_name(str): the name of the file to load
            force(bool): if True overwrite
            debug(bool): if True show debugging information
            
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
            if debug:
                print(f"{graph_xml}(size {size}) already downloaded ...")
        if not os.path.exists(graph_xml) or force:
            if debug:
                print(f"downloading {self.url} to {graph_xml} ...")
            graph_data = urllib.request.urlopen(self.url).read().decode("utf-8")
            print(graph_data,  file=open(graph_xml, 'w'))
        return graph_xml
    
class Examples:
    """
    Examples 
    """
    
    def __init__(self,volume:Volume,debug:bool=False):
        """
        Constructor
        
        Args:
            volume:Volume
            debug(bool): if true switch on debugging
        
        """
        self.debug=debug
        self.volume=volume
        self.examples_by_name={}
        for example in [
            Example(name="tinkerpop-modern",url="https://raw.githubusercontent.com/apache/tinkerpop/master/data/tinkerpop-modern.xml"),
            Example(name="grateful-dead",url="https://raw.githubusercontent.com/apache/tinkerpop/master/data/grateful-dead.xml"),
            Example(name="air-routes-small",url="https://raw.githubusercontent.com/krlawrence/graph/master/sample-data/air-routes-small.graphml"),
            Example(name="air-routes-latest",url="https://raw.githubusercontent.com/krlawrence/graph/master/sample-data/air-routes-latest.graphml")
        ]:
            self.examples_by_name[example.name]=example
        
    def load_by_name(self, g: GraphTraversalSource, name: str) -> None:
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
            example.load(g,self.volume,debug=self.debug)
        else:
            raise Exception(f"invalid example {name}")
