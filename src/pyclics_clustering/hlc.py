"""
Hierarchical link clustering
============================

:Author: Tamás Nepusz (adapted to the CLICS use case by Robert Forkel)

This is an implementation of the hierarchical link clustering algorithm of Ahn
et al. The results provided by this implementation match those of the original
Python implementation of the authors, but it is somewhat faster.  At least I
hope so. Also, it handles all the input graph formats that igraph_ handles.

.. _igraph: http://igraph.sourceforge.net
"""

from array import array
from collections import defaultdict
from operator import itemgetter


__author__ = "Tamas Nepusz"
__license__ = "MIT"
__docformat__ = "restructuredtext en"
__version__ = "0.1"


class OptimizedJaccardSimilarityCalculator(object):
    """Calculates pairwise Jaccard similarities on a given unweighted
    graph, using igraph's optimized C function. When calculating the
    similarities, it is assumed that every vertex is linked to itself.
    """

    def __init__(self, graph):
        self._graph = graph

    def get_similarity_many(self, pairs):
        """Returns the Jaccard similarity between many pairs of vertices,
        assuming that all vertices are linked to themselves."""
        return self._graph.similarity_jaccard(pairs=pairs)


class TanimotoSimilarityCalculator(object):
    """Calculates pairwise Tanimoto coefficients on a given weighted
    graph. When calculating the similarities, it is assumed that every
    vertex is linked to itself with an edge whose weight is equal to the
    average weight of edges adjacent to the vertex."""

    def __init__(self, graph, attr="FamilyWeight"):
        degrees = graph.degree()
        strengths = graph.strength(weights=attr)
        weights = graph.es[attr]

        self._adjedgelist = []
        get_eid = graph.get_eid     # prelookup
        for i in range(graph.vcount()):
            weis = {j: weights[get_eid(i, j)] for j in graph.neighbors(i)}
            if degrees[i]:
                weis[i] = strengths[i] / degrees[i]
            self._adjedgelist.append(weis)

        self._sqsums = [sum(value * value for value in vec.values())
                        for vec in self._adjedgelist]

    def get_similarity(self, v1, v2):
        """Returns the Tanimoto coefficient of the two given vertices,
        assuming that both of them are linked to themselves."""
        vec1, vec2 = self._adjedgelist[v1], self._adjedgelist[v2]

        if len(vec1) > len(vec2):
            # vec1 must always be the smaller
            vec1, vec2 = vec2, vec1

        numerator = sum(value * vec2.get(key, 0)
                        for key, value in vec1.items())
        return numerator / (self._sqsums[v1] + self._sqsums[v2] - numerator)

    def get_similarity_many(self, pairs):
        """Returns the Jaccard similarity between many pairs of vertices,
        assuming that all vertices are linked to themselves."""
        return [self.get_similarity(*pair) for pair in pairs]


class EdgeCluster(object):
    """Class representing a group of edges (i.e. a group of vertices
    in the line graph)

    This class also keeps track of the original vertices the edges
    refer to."""

    __slots__ = ("vertices", "edges")

    def __init__(self, vertices, edges):
        self.vertices = set(vertices)
        self.edges = set(edges)

    def is_smaller_than(self, other):
        """Compares this group of edges with another one based on
        size."""
        return len(self.edges) < len(other.edges)

    def partition_density(self):
        """Returns the number of edges times the relative density
        of this group. This value is used in the calculation of
        the overall partition density, used to select the best
        threshold."""
        m, n = len(self.edges), len(self.vertices)
        if n <= 2:
            return 0.
        return m * (m - n + 1) / (n - 2) / (n - 1)

    def merge_from(self, other):
        """Merges another group of edges into this one, updating
        self.vertices and self.edges"""
        self.vertices |= other.vertices
        self.edges |= other.edges


class EdgeClustering(object):
    """Class representing an edge clustering of a graph as a whole.

    This class is essentially a list of `EdgeCluster` instances
    plus some additional bookkeeping to facilitate the easy lookup
    of the cluster of a given edge.
    """

    def __init__(self, edgelist):
        """Constructs an initial edge clustering of the given graph
        where each edge belongs to its own cluster.

        The graph is given by its edge list in the `edgelist`
        parameter."""
        self.clusters = [EdgeCluster(edge, (i, ))
                         for i, edge in enumerate(edgelist)]
        self.membership = list(range(len(edgelist)))
        self.d = 0.0

    def merge_edges(self, edge1, edge2):
        """Merges the clusters corresponding to the given edges."""
        cid1, cid2 = self.membership[edge1], self.membership[edge2]

        # Are they the same cluster?
        if cid1 == cid2:
            return

        cl1, cl2 = self.clusters[cid1], self.clusters[cid2]

        # We will always merge the smaller into the larger cluster
        if cl1.is_smaller_than(cl2):
            cl1, cl2 = cl2, cl1
            cid1, cid2 = cid2, cid1

        # Save the partition densities
        dc1, dc2 = cl1.partition_density(), cl2.partition_density()

        # Merge the smaller cluster into the larger one
        for edge in cl2.edges:
            self.membership[edge] = cid1
        cl1.merge_from(cl2)
        self.clusters[cid2] = cl1

        # Update D
        self.d += cl1.partition_density() - dc1 - dc2


class HLC(object):
    """Hierarchical link clustering algorithm on a given graph.

    This class implements the algorithm outlined in Ahn et al: Link communities
    reveal multiscale complexity in networks, Nature, 2010. 10.1038/nature09182

    The implementation supports undirected and unweighted networks only at the
    moment, and it is assumed that the graph does not contain multiple or loop
    edges. This is not ensured within the class for sake of efficiency.

    The class provides the following attributes:

    - `graph` contains the graph being analysed
    - `min_size` contains the minimum size of the clusters one is interested
      in. It is advised to set this to at least 3 (which is the default value)
      to ensure that pseudo-clusters containing only two nodes do not turn up
      in the results.

    The algorithm may be run with or without a similarity threshold. When no
    similarity threshold is passed to the `run()` method, the algorithm will
    scan over the possible range of similarities and return a partition that
    corresponds to the similarity with the highest partition density. In this
    case, the similarity threshold and the partition density is recorded in
    the `last_threshold` and `last_partition_density` attributes. The former
    is also set properly when a single similarity threshold is used.
    """

    def __init__(self, graph, min_size=3, weight='FamilyWeight'):
        """Constructs an instance of the algorithm. The algorithm
        will be run on the given `graph` with the given minimum
        community size `min_size`."""
        self._graph = None
        self._edgelist = None
        self.last_threshold = None
        self.last_partition_density = None
        self.graph = graph
        self.min_size = int(min_size)
        self._weight_attr = weight

    @property
    def graph(self):
        """Returns the graph being clustered."""
        return self._graph

    @graph.setter
    def graph(self, graph):
        """Sets the graph being clustered."""
        self._graph = graph
        self._edgelist = graph.get_edgelist()

    def run(self):
        """Runs the hierarchical link clustering algorithm on the
        graph associated to this `HLC` instance, cutting the dendrogram
        at the given `threshold`.
        The optimal threshold will be selected using the partition density
        method described in Ahn et al, 2010. Returns a generator that
        will generate the clusters one by one.
        """

        # Construct the line graph
        linegraph = self.get_edge_similarity_graph()

        # Sort the scores
        sorted_edges = sorted(linegraph.es, key=itemgetter("score"),
                              reverse=True)

        # From now on, we only need the edge list of the original graph
        del linegraph

        # Set up initial configuration: every edge is a separate cluster
        clusters = EdgeClustering(self._edgelist)

        # Merge clusters, keep track of D, find maximal D
        max_d, best_threshold, best_membership = -1, None, None
        prev_score = None
        merge_edges = clusters.merge_edges       # prelookup
        for edge in sorted_edges:
            score = edge["score"]

            if prev_score != score:
                # Check whether the current D score is better than the best
                # so far
                if clusters.d >= max_d:
                    max_d, best_threshold = clusters.d, score
                    best_membership = list(clusters.membership)
                prev_score = score

            # Merge the clusters
            merge_edges(edge.source, edge.target)

        del clusters
        max_d *= 2 / self.graph.ecount()

        # Record the best threshold and partition density
        self.last_threshold = best_threshold
        self.last_partition_density = max_d

        # Build the result
        result = defaultdict(set)
        for edge, cluster_index in zip(self._edgelist, best_membership):
            result[cluster_index].update(edge)
        return (list(cluster) for cluster in result.values()
                if len(cluster) >= self.min_size)

    def get_edge_similarity_graph(self):
        """Calculates the edge similarity graph of the graph assigned
        to this `HLC` instance."""

        # Construct the line graph
        linegraph = self.graph.linegraph()

        # Select the appropriate similarity function
        if self._weight_attr in self.graph.edge_attributes():
            sc = TanimotoSimilarityCalculator(self.graph, attr=self._weight_attr)
        else:
            sc = OptimizedJaccardSimilarityCalculator(self.graph)
        similarity = sc.get_similarity_many

        # For each edge in the line graph, compute a similarity score
        edgelist = self._edgelist    # prelookup
        sources, targets = array('l'), array('l')
        sources.extend(0 for _ in range(linegraph.ecount()))
        targets.extend(0 for _ in range(linegraph.ecount()))
        for edge in linegraph.es:
            (a, b), (c, d) = edgelist[edge.source], edgelist[edge.target]
            i = edge.index
            if a == c:
                sources[i] = b
                targets[i] = d
            elif a == d:
                sources[i] = b
                targets[i] = c
            elif b == c:
                sources[i] = a
                targets[i] = d
            else:   # b == d
                sources[i] = a
                targets[i] = c
        linegraph.es["score"] = similarity(zip(sources, targets))
        return linegraph
