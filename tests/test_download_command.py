import unittest
import json
import mock
from gitrc import GitRC
from argparse import _AttributeHolder
from .fixtures import GITHUB_REPOS_JSONrequests
michael.el

class _MockedArgs(_AttributeHolder):
	def __init__(self, username=None, passowrd=None, github_username=None):
		self.username = username
		self.password = passowrd
		self.github_username = github_username


@mock.patch('github3.github.GitHub.repositories_by')
class DownloadCommand_Tests(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.gitrc = GitRC()
		self.args = self.gitrc.parse_cmdl_args(
			['download', 'jasperfirecai2'],
		)

	def test_should_return_list_of_all_Github_user_account(self, repositories_by):

		# test
		actual = self.gitrc.download_cmd(self.args)

		# verify
		self.assertGreaterEqual(len(actual), 10)


if __name__ == '__main__':
	unittest.main()





