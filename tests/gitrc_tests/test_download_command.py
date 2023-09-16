import os
import unittest
import json
import mock
import gitrc
import timeout_decorator
from io import StringIO
from gitrc import GitRC
from argparse import _AttributeHolder
from gitrc_tests.fixtures import *
from unittest.mock import patch


@mock.patch('github3.github.GitHub.repositories_by')
class DownloadCommand_NoPasswordPrompt_Tests(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.maxDiff = None
		self.gitrc = GitRC()
		self.args = self.gitrc.parse_cmdl_args(['download', 'jasperfirecai2'])
		self.expected = ''
		for x in [x['clone_url'] for x in GITHUB_REPOS_JSON]:
			self.expected += x + '\n'
		self.cases = [
			self.gitrc.parse_cmdl_args(['download', 'jasperfirecai2']),
			self.gitrc.parse_cmdl_args(['download', 'jasperfirecai2', '--username', 'johhny5', '--password', 'super_secret']),
		]

	@timeout_decorator.timeout(2.0)
	def test_should_return_list_of_all_Github_user_account(self, repositories_by):
		# setup
		for args in self.cases:
			repositories_by.return_value = GitHub3Mock()
			with patch('sys.stdout', new=StringIO()) as actual_output:

				# test
				with self.subTest():
					self.gitrc.download_cmd(args)

					# verify
					self.assertEquals(
						self.expected,
						actual_output.getvalue(),
						# 'foo',
					)


@mock.patch('github3.github.GitHub.repositories_by')
class DownloadCommand_WithPasswordPrompt_Tests(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.maxDiff = None
		self.gitrc = GitRC()
		self.expected = {
			'password_prompt': 'Enter your password: ',
			'entered_password': 'SuperSecret12345'
		}
		self.args = self.gitrc.parse_cmdl_args([
			'download', 'jasperfirecai2',
			'--username', 'Johny5',
			'-p', '--password_prompt', self.expected['password_prompt'],
		])

	@timeout_decorator.timeout(1.0)
	def test_should_output_custom_password_prompt(self, repositories_by):
		# setup
		repositories_by.return_value = []
		with patch('sys.stdout', new=StringIO()) as actual_output:
			with patch('sys.stdin', new=StringIO(self.expected['password_prompt'])) as m_input:
				# m_input.return_value = self.expected['password_prompt']

				# test
				result = self.gitrc.download_cmd(self.args)

				# verify
				self.assertIsNone(result)
				self.assertEquals(
					self.expected['password_prompt'],
					actual_output.getvalue(),
				)
				self.assertEquals(
					self.expected['password_prompt'],
					self.gitrc.args.password_prompt,
				)
				self.assertTrue(self.gitrc.args.output_prompt)













