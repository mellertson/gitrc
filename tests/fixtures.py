import os
import json


__all__ = [
	'GITHUB_REPOS_JSON',
]


GITHUB_REPOS_JSON = None
filename = os.path.join(os.path.dirname(__file__), 'fixture_1.json')
with open(filename, 'rt') as f:
	GITHUB_REPOS_JSON = f.read()

