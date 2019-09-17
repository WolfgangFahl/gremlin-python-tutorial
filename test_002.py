# start GremlinServer 
# bin/gremlin-server.sh -i org.apache.tinkerpop gremlin-python 3.2.2-SNAPSHOT
# bin/gremlin-server.sh conf/gremlin-server-modern-py.yaml

from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import Operator

from gremlin_python.structure.io.graphson import GraphSONReader
from gremlin_python.structure.io.graphson import serializers
from gremlin_python.process.traversal import Bytecode
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import P

from gremlin_python.structure.io.graphson import GraphSONWriter

# in practice, you really only need the 3 imports below

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


# this allows us to do g.V().repeat(out()) instead of g.V().repeat(__.out())-type traversals

statics.load_statics(globals())

# create a remote connection using RemoteStrategy

graph = Graph()
g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182','g'))

# the __repr__ (string) of traversal is its Python encoded bytecode (lowest level of compilation for that host)

g.V().repeat(out()).times(2).name

# you can see the GraphSON 2.0 bytecode for a traversal

GraphSONWriter.writeObject(g.V().repeat(out()).times(2).name)

# toList()/toSet()/next()/etc. are terminal/action methods that trigger evaluation

g.V().repeat(both()).times(2).name.toList()
g.V().repeat(both()).times(2).name.toSet()
g.V().repeat(out()).times(2).name.next()
g.V().repeat(out()).times(2).name.nextTraverser()

# bindings ensure that cached traversal compilations can be reused

g.V().out(("a","knows"),"created").name
g.V().out(("a","knows"),"created").name.bytecode
g.V().out(("a","knows"),"created").name.bytecode.bindings
g.V().out(("a","knows"),"created").name.toList()

# lambdas are solved via a lamda that returns a string lambda

g.V().out().map(lambda: "lambda x: (x.get().value('name'),len(x.get().value('name')))")
g.V().out().map(lambda: "lambda x: x.get()").toList()
g.V().out().map(lambda: "x: (x.get().value('name'),len(x.get().value('name')))").toList()

# all the source modulators work

g.withComputer().V().out('created').valueMap()
g.withComputer().V().out('created').valueMap().toList()
g.withSack(0).V().repeat(outE().sack(sum,'weight').inV()).times(2).project('a','b').by('name').by(sack()).toList()

# side-effects work too

g.V().repeat(groupCount('m').by('name').both()).times(10).cap('m').next()
t = g.V().repeat(groupCount('m').by('name').both()).times(10).iterate()
t.side_effects
t.side_effects.keys()
t.side_effects['m']

t = g.V().aggregate("m").iterate()
t.side_effects
t.side_effects.keys()
t.side_effects['m']

t = g.withSideEffect('m',0).V().hasLabel('person').sideEffect(lambda : "x : x.sideEffects('m',x.get().value('age'))").groupCount('n').by('name')
t.toList()
t.side_effects
t.side_effects.keys()
t.side_effects['m']
t.side_effects['n']

# with ssl authentification (be sure to add authentification to the gremlin-server-modern-py.yaml)

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

graph = Graph()
g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182','g', username='stephen', password='password'))
g.V().toList()