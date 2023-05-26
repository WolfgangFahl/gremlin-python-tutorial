#!/usr/bin/env python
# see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/tests/driver/test_client.py
from gremlin_python.driver.request import RequestMessage
from gremlin.remote import RemoteTraversal
from tests.basetest import Basetest

class TestConnection(Basetest):
    """
    test connection handling
    """
    # test a connection
    def test_connection(self):
        # see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/gremlin_python/driver/driver_remote_connection.py
        remoteTraversal=RemoteTraversal()
        g = remoteTraversal.g()
        t=g.V()
        remoteConnection=remoteTraversal.remoteConnection
        # see https://github.com/apache/tinkerpop/blob/master/gremlin-python/src/main/jython/gremlin_python/driver/client.py
        client=remoteConnection._client
    
        connection=client._get_connection()
        message = RequestMessage('traversal', 'bytecode', {'gremlin': t.bytecode, 'aliases': {'g': client._traversal_source}})
        results_set = connection.write(message).result()
        future = results_set.all()
        results = future.result()
        print ("%d results" % (len(results)))
        #assert len(results) == 6
        assert isinstance(results, list)
        assert results_set.done.done()
        #assert 'host' in results_set.status_attributes
        print (results_set.status_attributes)


