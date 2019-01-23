from pyclics.plugin import register_cluster_algorithm
import community


def louvain(graph, kw):
    partition = community.best_partition(graph)
    for com in set(partition.values()):
        yield [nodes for nodes in partition.keys() if partition[nodes] == com]


def includeme(registry):
    register_cluster_algorithm(registry, louvain)
