'''
Created on 2019-09-17

@author: wf
'''
from __future__ import annotations
from gremlin_python.process.anonymous_traversal import GraphTraversalSource, traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.aiohttp.transport import AiohttpTransport
import os.path
from os.path import dirname, abspath
import io
import yaml
import socket
from contextlib import closing

from typing import Optional


class RemoteTraversal:
    """
    helper class for Apache Tinkerpop Gremlin Python GLV remote access
    """

    def __init__(self, server:Server, in_jupyter: bool = False) -> None:
        """
        constructor
        
        """
        self.server=server
        self.in_jupyter=in_jupyter
        
    @staticmethod
    def fromYaml(serverName='server',config_path:Optional[str]=None, in_jupyter: bool = False)->"RemoteTraversal":
        """
        create a server from the given yaml file
        
        Args:
            serverName(str): the servername to use
            config_path(str): the path to the server configuration file
        """
        server=Server.read(serverName,config_path)
        rt=RemoteTraversal(server, in_jupyter=in_jupyter)
        return rt
   
    def g(self) -> GraphTraversalSource:
        """
        get the graph traversal source

        Returns:
            the graph traversal source
        """
        server=self.server
        url=f'ws://{server.host}:{server.port}/gremlin' 
        # https://github.com/orientechnologies/orientdb-gremlin/issues/143
        #username="root"
        #password="rootpwd"
        if self.in_jupyter:
            self.remoteConnection=DriverRemoteConnection(url,server.alias,username=server.username,password=server.password, transport_factory=lambda: AiohttpTransport(call_from_event_loop=True))
        else:
            self.remoteConnection=DriverRemoteConnection(url,server.alias,username=server.username,password=server.password)
        g = traversal().withRemote(self.remoteConnection)
        return g
    
    def close(self) -> None:
        """
        close my connection
        """
        self.remoteConnection.close()

    @staticmethod
    def load(g: GraphTraversalSource, graphmlFile) -> None:
        """
        load the given graph from the given graphmlFile
        """
        # make the local file accessible to the server
        xmlPath=os.path.abspath(graphmlFile)
        # drop the existing content of the graph
        g.V().drop().iterate()
        # read the content from the graphmlFile
        g.io(xmlPath).read().iterate()
    
    @staticmethod
    def clear(g: GraphTraversalSource) -> None:
        """
        clear the given graph
        """
        g.V().drop().iterate()

class Server:
    """
    Server description
    """
    debug=False

    # construct me with the given alias
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 8182,
        alias: str ='g',
        name: str = 'TinkerGraph',
        username: str = '',
        password: str = '',
        debug: bool = False,
        helpUrl: str = 'http://wiki.bitplan.com/index.php/Gremlin_python#Connecting_to_Gremlin_enabled_graph_databases'
    ) -> None:
        """
        constructor

        Args:
            host(str): the host to connect to
            port(int): the port to connect to
            alias(str): the alias to use
            name(str): the name of the server
            username(Optional[str]): the username to use
            password(Optional[str]): the password to use
            debug(bool): True if debug output should be generated
            helpUrl(str): the help url to use
        """
        self.host=host
        self.port=port
        self.alias=alias
        self.name=name
        self.username=username
        self.password=password
        Server.debug=debug
        self.helpUrl=helpUrl
        
    def check_socket(self) -> bool:
        """
        check my socket
        
        Returns:
            True if socket is open
        """
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            is_open=sock.connect_ex((self.host, self.port)) == 0
            return is_open

    # return a readable representation of me
    def __repr__(self) -> str:
        return "%s(%r)" % (self.__class__, self.__dict__)

    @staticmethod
    def read(name:str, config_path: Optional[str] = None) -> "Server":
        """
        read me from a yaml file

        Args:
            name(str): the name of the server
            config_path(str): the path to the config files

        Returns:
            the server

        Raises:
            Exception: if the yaml file is missing
        """
        if config_path is None:
            script_path = dirname(abspath(__file__))
            config_path=abspath(f"{script_path}/config")
        yamlFile=f"{config_path}/{name}.yaml"
        # is there a yamlFile for the given name
        if os.path.isfile(yamlFile):
            with io.open(yamlFile,'r') as stream:
                if Server.debug:
                    print ("reading %s" % (yamlFile))
                server=yaml.load(stream,Loader=yaml.Loader)
                if (Server.debug):
                    print (server)
                return server
        else:
            raise Exception(f"{yamlFile} is missing")


    # write me to my yaml file
    def write(self) -> None:
        """
        write me to my yaml file
        """
        yamlFile=self.name+".yaml"
        with io.open(yamlFile,'w',encoding='utf-8') as stream:
            yaml.dump(self,stream)
            if Server.debug:
                print (yaml.dump(self))
