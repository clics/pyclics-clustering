from pyclics_clustering import louvain, hlc, label_propagation, connected_components


def test_connected_components(graph):
    res = list(connected_components(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_louvain(graph):
    res = list(louvain(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_label_propagation(graph):
    res = list(label_propagation(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1


def test_hlc(graph):
    res = list(hlc(graph, {}))
    assert isinstance(res[0], list)
    assert max(map(len, res)) > 1
    res = list(hlc(graph, {'weight': 'x'}))
    assert isinstance(res[0], list)
