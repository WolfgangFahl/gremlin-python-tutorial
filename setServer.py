# set the server configuration
import argparse
from gremlin import gremote

# https://docs.python.org/2/library/argparse.html
# prepare command line argument accepted
parser = argparse.ArgumentParser(description='set the server configuration for gremlin_python')
parser.add_argument('--debug',action="store_true",help='show debug info')
parser.add_argument('--rewrite',action="store_true",help='write a new server configuration')
parser.add_argument('--host', default="localhost", help='the host name of the server')
parser.add_argument('--port',type=int, default=8182,help='the port to be used')
parser.add_argument('--alias', default="g", help='the default alias to use')
parser.add_argument('--name', default="TinkerGraph", help='the name of the server')
parser.add_argument('--username', default=None, help='the username to use for authentication')
parser.add_argument('--password', default=None, help='the password to use for authentication')
parser.add_argument('--helpUrl', default="http://wiki.bitplan.com/index.php/Gremlin_python#Connecting_to_Gremlin_enabled_graph_databases", help='the url for help on this server configuration')

# parse the command line arguments
args = parser.parse_args()

# uncomment to debug
gremote.Server.debug=True
# try reading the server description from the yaml file with the given name
server=gremote.Server.read(args.name)
if server is None or args.rewrite:
  server=gremote.Server(host=args.host,port=args.port,alias=args.alias,name=args.name,username=args.username,password=args.password,debug=args.debug)
  server.write()
