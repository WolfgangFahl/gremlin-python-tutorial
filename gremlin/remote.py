'''
Created on 2019-09-17

@author: wf
'''
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import os.path
from os.path import dirname, abspath
import io
import yaml
import socket
from contextlib import closing

class RemoteTraversal:
    """
    helper class for Apache Tinkerpop Gremlin Python GLV remote access
    """

    def __init__(self,server):
        """
        constructor
        
        """
        self.server=server
        
    @classmethod
    def fromYaml(cls,serverName='server',config_path:str=None)->"RemoteTraversal":
        """
        create a server from the given yaml file
        
        Args:
            serverName(str): the servername to use
            config_path(str): the path to the server configuration file
        """
        server=Server.read(serverName,config_path)
        rt=RemoteTraversal(server)
        return rt
   
    def g(self):
        """
        get the graph traversal
        """
        server=self.server
        url=f'ws://{server.host}:{server.port}/gremlin' 
        # https://github.com/orientechnologies/orientdb-gremlin/issues/143
        #username="root"
        #password="rootpwd"
        self.remoteConnection=DriverRemoteConnection(url,server.alias,username=server.username,password=server.password)
        g = traversal().with_remote(self.remoteConnection)
        return g
    
    def close(self):
        """
        close my connection
        """
        self.remoteConnection.close()

    @classmethod
    def load(self,g,graphmlFile):
        """
        load the given graph from the given graphmlFile
        """
        # make the local file accessible to the server
        xmlPath=os.path.abspath(graphmlFile)
        # drop the existing content of the graph
        g.V().drop().iterate()
        # read the content from the graphmlFile
        g.io(xmlPath).read().iterate()
        
    @classmethod
    def clear(cls,g):
        g.V().drop().iterate()

class Server:
    """
    Server description
    """
    debug=False

    # construct me with the given alias
    def __init__(self,host='localhost',port=8182,alias='g',name='TinkerGraph',username=None,password=None,debug=False,helpUrl='http://wiki.bitplan.com/index.php/Gremlin_python#Connecting_to_Gremlin_enabled_graph_databases'):
        self.host=host
        self.port=port
        self.alias=alias
        self.name=name
        self.username=username
        self.password=password
        Server.debug=debug
        self.helpUrl=helpUrl
        
    def check_socket(self)->bool:
        """
        check my socket
        
        Returns:
            True if socket is open
        """
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            is_open=sock.connect_ex((self.host, self.port)) == 0
            return is_open

    # return a readable representation of me
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    @staticmethod
    def read(name:str,config_path:str=None):
        """
        read me from a yaml file
        """
        if config_path is None:
            script_path = dirname(abspath(__file__))
            config_path=abspath(f"{script_path}/../config")
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
    def write(self):
        yamlFile=self.name+".yaml"
        with io.open(yamlFile,'w',encoding='utf-8') as stream:
            yaml.dump(self,stream)
            if Server.debug:
                print (yaml.dump(self))
