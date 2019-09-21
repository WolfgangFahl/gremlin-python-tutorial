from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import os.path
import io
import yaml

# Helper class for remote Graph Access
class RemoteTraversal:

    # construct me with the given alias
    def __init__(self,serverName='server'):
        self.server=Server.read(serverName)
        if self.server is None:
           raise Exception("%s.yaml is missing" % (serverName))

    # get the graph traversal
    def g(self):
        server=self.server
        url='ws://%s:%d/gremlin' % (server.host,server.port)
        # https://github.com/orientechnologies/orientdb-gremlin/issues/143
        #username="root"
        #password="rootpwd"
        self.remoteConnection=DriverRemoteConnection(url,server.alias,username=server.username,password=server.password)
        g = traversal().withRemote(self.remoteConnection)
        return g

    # load the graph from the given graphmlFile
    def load(self,graphmlFile):
         g=self.g()
         # make the local file accessible to the server
         xmlPath=os.path.abspath(graphmlFile)
         # drop the existing content of the graph
         g.V().drop().iterate()
         # read the content from the graphmlFile
         g.io(xmlPath).read().iterate()

# a Server description
class Server:
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

    # return a readable representation of me
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    # read me from a yaml file
    @staticmethod
    def read(name):
       yamlFile=name+".yaml"
       # is there a yamlFile for the given name
       if os.path.isfile(yamlFile):
          with io.open(yamlFile,'r') as stream:
             if Server.debug:
                print ("reading %s" % (yamlFile))
             server=yaml.load(stream,Loader=yaml.Loader)
             if (Server.debug):
                 print (server)
             return server

    # write me to my yaml file
    def write(self):
        yamlFile=self.name+".yaml"
        with io.open(yamlFile,'w',encoding='utf-8') as stream:
            yaml.dump(self,stream)
            if Server.debug:
                print (yaml.dump(self))
