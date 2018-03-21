from .. import convert


def test_abc_to_id():
    samples = {
        'A': 0,
        'B': 1,
        'Y': 24,
        'a': 26,
        'b': 27,
        'y': 50,
        'BA': 52,
        'BAB': 2705,
    }
    for abc, id in samples.items():
        assert convert.abc_to_id(abc) == id


def test_id_to_abc():
    samples = {
        1: 'B',
        24: 'Y',
        26: 'a',
        52: 'BA',
        78: 'Ba',
        104: 'CA',
        130: 'Ca',
    }
    for id, abc in samples.items():
        assert convert.id_to_abc(id) == abc
