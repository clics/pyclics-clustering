import community
import networkx.algorithms.community.label_propagation
import networkx.algorithms.components.connected
from pyclics_clustering.hlc import HLC

from pyclics.util import networkx2igraph


def louvain(graph, kw):
    partition = community.best_partition(graph, resolution=float(kw.pop('resolution', 1)))
    for com in set(partition.values()):
        yield [nodes for nodes in partition.keys() if partition[nodes] == com]


def connectedcomponents(graph, kw):
    for com in networkx.algorithms.components.connected.connected_components(graph):
        yield list(com)


def labelpropagation(graph, kw):
    for com in networkx.algorithms.community.label_propagation.label_propagation_communities(graph):
        yield list(com)


def hlc(graph, kw):
    _graph = networkx2igraph(graph)
    algo = HLC(_graph, min_size=3, weight=kw.pop('weight', 'FamilyWeight'))
    algo.run()
    for _community in algo.run():
        yield [i for i in _graph.vs[_community]["Name"]]


def includeme(registry):
    registry.register_clusterer(louvain)
    registry.register_clusterer(hlc)
    registry.register_clusterer(labelpropagation)
    registry.register_clusterer(connectedcomponents)
