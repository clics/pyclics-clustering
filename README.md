# pyclics-clustering

Various clustering algoriths packaged as plugins for CLICS.

[![Build Status](https://travis-ci.org/clics/pyclics-clustering.svg?branch=master)](https://travis-ci.org/clics/pyclics-clustering)
[![codecov](https://codecov.io/gh/clics/pyclics-clustering/branch/master/graph/badge.svg)](https://codecov.io/gh/clics/pyclics-clustering)
[![PyPI](https://img.shields.io/pypi/v/pyclics-clustering.svg)](https://pypi.org/project/pyclics-clustering)


## Connected Components

As implemented in the [`networkx` package](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.components.connected.connected_components.html).


## Hierarchical Link Clustering (HLC)

The algorithm is described in

> Ahn YY, Bagrow JP and Lehmann S: Link communities reveal multiscale complexity in networks. *Nature* **466**, 761 (2010).

The implementation is copied from [Tamás Nepusz](https://github.com/ntamas/hlc) with
slight modifications to work with CLICS networks.


## Louvain Community Detection

The algorithm is described in

> Vincent D Blondel, Jean-Loup Guillaume, Renaud Lambiotte, Renaud Lefebvre: Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment* **10** (2008), P10008 (12pp).

We use the implementation by [Thomas Aynaud](https://github.com/taynaud/python-louvain).


## Label Propagation

The algorithm is described in

> Cordasco, G., & Gargano, L.: Community detection via semi-synchronous label propagation algorithms. 
> In Business Applications of Social Network Analysis (BASNA), 
> 2010 IEEE International Workshop on (pp. 1-8). IEEE.

As implemented in the [`networkx` package](https://networkx.github.io/documentation/latest/reference/algorithms/generated/networkx.algorithms.community.label_propagation.label_propagation_communities.html).

