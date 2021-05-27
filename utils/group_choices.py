from .groups import *
from collections import defaultdict

GROUP_CHOICES = [
    (GROUP_8A, '8А'),
    (GROUP_8V, '8В'),
    (GROUP_9A, '9А'),
    (GROUP_9B, '9Б'),
    (GROUP_9V, '9В'),
    (GROUP_9G, '9Г'),
    (GROUP_9E, '9Е'),
    (GROUP_10A, '10А'),
    (GROUP_10B, '10Б'),
    (GROUP_10V, '10В'),
    (GROUP_10G, '10Г'),
    (GROUP_10D, '10Д'),
    (GROUP_10E, '10Е'),
    (GROUP_10Z, '10З'),
    (GROUP_10K, '10К'),
    (GROUP_10L, '10Л'),
    (GROUP_10M, '10М'),
    (GROUP_10N, '10Н'),
    (GROUP_10S, '10С'),
    (GROUP_11A, '11А'),
    (GROUP_11B, '11Б'),
    (GROUP_11V, '11В'),
    (GROUP_11G, '11Г'),
    (GROUP_11D, '11Д'),
    (GROUP_11E, '11Е'),
    (GROUP_11Z, '11З'),
    (GROUP_11K, '11К'),
    (GROUP_11L, '11Л'),
    (GROUP_11M, '11М'),
    (GROUP_11N, '11Н'),
    (GROUP_11S, '11С')
]

groups_dict = dict(GROUP_CHOICES)

reversed_groups_dict = dict([(title.lower(), num) for num, title in GROUP_CHOICES])
reversed_groups_defaultdict = defaultdict(lambda: None, reversed_groups_dict)
