import os
import unittest
import mock
import timeout_decorator
from io import StringIO
from gitrc import GitRC
from gitrc_tests.fixtures import *
from unittest.mock import patch


@mock.patch('github3.github.GitHub.repositories_by')
class TestDownloadCommand_NoPasswordPrompt(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.maxDiff = None
		self.gitrc = GitRC()
		self.args = self.gitrc.parse_cmdl_args(['download', 'Neo'])
		self.expected = ''
		for x in [x['clone_url'] for x in GITHUB_REPOS_JSON]:
			self.expected += x + '\n'
		self.cases = [
			self.gitrc.parse_cmdl_args(['download', 'Neo']),
			self.gitrc.parse_cmdl_args(['download', 'Neo', '--username', 'Johhny5', '--password', 'super_secret']),
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
class TestDownloadCommand_WithPasswordPrompt(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.maxDiff = None
		self.gitrc = GitRC()
		self.expected = {
			'password_prompt': 'Enter your password: ',
			'entered_password': 'SuperSecret12345'
		}
		self.args = self.gitrc.parse_cmdl_args([
			'download', 'Neo',
			'--username', 'Johny5',
			'-p', '--password_prompt', self.expected['password_prompt'],
		])

	@timeout_decorator.timeout(1.0)
	def test_should_output_custom_password_prompt(self, repositories_by):
		# setup
		repositories_by.return_value = []
		with patch('sys.stdout', new=StringIO()) as actual_output:
			with patch('sys.stdin', new=StringIO(self.expected['password_prompt'])) as m_input:

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


@mock.patch('github3.github.GitHub.repositories_by')
class TestDownloadCommand_WithNoCredentials(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.maxDiff = None
		self.gitrc = GitRC()
		self.expected = {
			'password_prompt': 'Password: ',
		}
		self.args = self.gitrc.parse_cmdl_args([
			'download', 'Neo',
		])

	@timeout_decorator.timeout(1.0)
	def test_should_call_GitHub_with_zero_args(self, repositories_by):
		# setup
		repositories_by.return_value = []
		with patch('sys.stdout', new=StringIO()) as actual_output:
			with patch('sys.stdin', new=StringIO(self.expected['password_prompt'])) as m_input:

				# test
				result = self.gitrc.download_cmd(self.args)

				# verify
				self.assertIsNone(result)
				self.assertEquals('', actual_output.getvalue())
				self.assertEquals(
					self.expected['password_prompt'],
					self.gitrc.args.password_prompt,
				)
				self.assertFalse(self.gitrc.args.output_prompt)


@mock.patch('gitrc.GitRC.parse_cmdl_args', autospec=True)
class TestDownloadCommand_run__method(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.gitrc = GitRC()

	def test_should_call_methods_correctly(self, parse_cmdl_args):
		# setup
		expected_args = mock.MagicMock('args')
		expected_args.func = mock.MagicMock('args.func')
		parse_cmdl_args.return_value = expected_args

		# test
		self.gitrc.run()

		# verify
		expected_args.func.assert_called_with(expected_args)


@mock.patch('gitrc.GitRC.run')
class Test_gitrc__main__(unittest.TestCase):

	def setUp(self) -> None:
		super().setUp()
		self.project_root = os.path.dirname(
			os.path.dirname(os.path.dirname(__file__))
		)
		self.main_py = os.path.join(
			self.project_root,
			'src/gitrc/__main__.py'
		)

	@timeout_decorator.timeout(1.0)
	def test_should_instantiate_and_call_run_method(self, m_run):
		# setup
		import imp
		run_main = imp.load_source('__main__', self.main_py)
		with mock.patch('gitrc.__name__', '__main__'):

			# test
			import gitrc

			# verify
			m_run.assert_called_once_with()



