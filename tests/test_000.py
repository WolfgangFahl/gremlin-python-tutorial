# see https://github.com/WolfgangFahl/gremlin-python-tutorial/blob/master/test_001.py
from gremlin.remote import RemoteTraversal
import unittest

class TestModern(unittest.TestCase):
    """
    test Remote Traversal
    """

    def test_LoadModern(self):
        """
        test loading the tinkerpop-modern graph
        """
        remoteTraversal=RemoteTraversal()
        g=remoteTraversal.g()
        remoteTraversal.load(g,"../data/tinkerpop-modern.xml")


