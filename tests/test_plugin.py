from pyclics_clustering import louvain, hlc, labelpropagation, connectedcomponents


def test_connected_components(graph):
    res = list(connectedcomponents(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_louvain(graph):
    res = list(louvain(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_label_propagation(graph):
    res = list(labelpropagation(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_hlc(graph):
    res = list(hlc(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1
    res = list(hlc(graph, {'weight': 'x'}))
    assert isinstance(res[0], list)
