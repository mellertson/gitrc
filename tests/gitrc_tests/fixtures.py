import os
import json


__all__ = [
	'GITHUB_REPOS_JSON',
	'GitHubCloneUrlMock',
	'GitHub3Mock',
]


GITHUB_REPOS_JSON = None
filename = os.path.join(os.path.dirname(__file__), 'fixture_1.json')
with open(filename, 'rt') as f:
	GITHUB_REPOS_JSON = json.load(f)


class GitHubCloneUrlMock(object):
	def __init__(self, clone_url):
		self.clone_url = clone_url


class GitHub3Mock(object):

	def __iter__(self, *args, **kwargs):
		for data in GITHUB_REPOS_JSON:
			yield GitHubCloneUrlMock(data['clone_url'])










