from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest
import six

from giticket.giticket import get_branch_name
from giticket.giticket import main
from giticket.giticket import update_commit_message

TESTING_MODULE = 'giticket.giticket'

COMMIT_MESSAGE = 'Test commit message\n\nFoo bar\nBaz qux'


@pytest.mark.parametrize('msg', (
    'Test ABC-1 message',
    'ABC-2 Test message',
    'Test message ABC-3',
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_no_modification(mock_branch_name, msg, tmpdir):
    mock_branch_name.return_value = 'JIRA-1234_new_feature'
    path = tmpdir.join('file.txt')
    path.write(msg)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'underscore_split', '{ticket} {commit_msg}')
    # Message should remain intact as it contains some ticket
    assert path.read() == msg


@pytest.mark.parametrize('test_data', (
    ('JIRA-1234', 'JIRA-1234'),
    ('JIRA-1234_bar', 'JIRA-1234'),
    ('foo-JIRA-1234_bar', 'foo-JIRA-1234'),
    ('foo/JIRA-1234-bar', 'foo/JIRA-1234-bar'),
    ('foo_JIRA-1234_bar', 'foo'),
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_underscore_split_mode(mock_branch_name,
                                                     test_data, tmpdir):
    mock_branch_name.return_value = test_data[0]
    path = tmpdir.join('file.txt')
    path.write(COMMIT_MESSAGE)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'underscore_split', '{ticket}: {commit_msg}')
    assert path.read() == '{expected_ticket}: {message}'.format(
        expected_ticket=test_data[1], message=COMMIT_MESSAGE
    )


@pytest.mark.parametrize('branch_name', (
    'JIRA-1234',
    'JIRA-1234_bar',
    'foo_JIRA-1234_bar',
    'foo-JIRA-1234-bar',
    'foo/JIRA-1234-bar',
    'fooJIRA-1234bar',
    'foo/bar/JIRA-1234',
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_regex_match_mode(mock_branch_name,
                                                branch_name, tmpdir):
    mock_branch_name.return_value = branch_name
    path = tmpdir.join('file.txt')
    path.write(COMMIT_MESSAGE)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}')
    assert path.read() == 'JIRA-1234: {message}'.format(message=COMMIT_MESSAGE)


@pytest.mark.parametrize('test_data', (
    ('JIRA-1234', 'JIRA-1234'),
    ('JIRA-1234-JIRA-239', 'JIRA-1234'),
    ('JIRA-239-JIRA-1234', 'JIRA-239'),
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_multiple_ticket_first_selected(mock_branch_name,
                                                              test_data,
                                                              tmpdir):
    mock_branch_name.return_value = test_data[0]
    path = tmpdir.join('file.txt')
    path.write(COMMIT_MESSAGE)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}')
    assert path.read() == '{expected_ticket}: {message}'.format(
        expected_ticket=test_data[1], message=COMMIT_MESSAGE
    )


@pytest.mark.parametrize('test_data', (
    ('JIRA-1234', 'JIRA-1234'),
    ('JIRA-1234-JIRA-239', 'JIRA-1234, JIRA-239'),
    ('JIRA-239-JIRA-1234', 'JIRA-239, JIRA-1234'),
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_multiple_ticket_all_selected(mock_branch_name,
                                                            test_data, tmpdir):
    mock_branch_name.return_value = test_data[0]
    path = tmpdir.join('file.txt')
    path.write(COMMIT_MESSAGE)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{tickets}: {commit_msg}')
    assert path.read() == '{expected_tickets}: {message}'.format(
        expected_tickets=test_data[1], message=COMMIT_MESSAGE
    )


@pytest.mark.parametrize('msg', (
    "\n",
    "a bogus message\n"
    """A message

With a description\n""",
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_ci_message_with_nl_regex_match_mode(mock_branch_name, msg, tmpdir):
    first_line = msg.split('\n')[0].strip()
    mock_branch_name.return_value = "JIRA-239_mock_branch"
    path = tmpdir.join('file.txt')
    path.write(msg)
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{commit_msg} - {ticket}')
    assert path.read().split('\n')[0] == "{first_line} - {ticket}".format(first_line=first_line, ticket="JIRA-239")


# create a unit test to verify that if the --conventionalcommits flag is set,
# the commit message is updated according to the conventional commit format
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_conventionalcommits(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-5678_new_feature"
    path = tmpdir.join('file.txt')
    path.write("feat: add new feature")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{commit_msg}', conventionalcommits=True)
    assert path.read() == "feat(JIRA-5678): add new feature\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_capitalize(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "jira-1234_new_feature"
    path = tmpdir.join('file.txt')
    path.write("Test commit message")
    update_commit_message(six.text_type(path), r'[a-zA-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          capitalize_spaces=1)
    assert path.read() == "Jira-1234: Test commit message\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_capitalize_multiple_chars(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "jira-1234"
    path = tmpdir.join('file.txt')
    path.write("Test commit message")
    update_commit_message(six.text_type(path), r'[a-zA-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          capitalize_spaces=4)
    assert path.read() == "JIRA-1234: Test commit message\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_capitalize_already_uppercase(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-1234_new_feature"
    path = tmpdir.join('file.txt')
    path.write("Test commit message")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          capitalize_spaces=1)
    assert path.read() == "JIRA-1234: Test commit message\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_capitalize_conventionalcommits(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-5678_new_feature"
    path = tmpdir.join('file.txt')
    path.write("feat: add new feature")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{commit_msg}',
                          conventionalcommits=True, capitalize_spaces=1)
    assert path.read() == "feat(JIRA-5678): add new feature\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_to_trailer(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-1234_new_feature"
    path = tmpdir.join('file.txt')
    path.write("Subject line\n\nBody text.")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          to_trailer=True)
    assert path.read() == "Subject line\n\nBody text.\n\nRefs: JIRA-1234\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_to_trailer_subject_only(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-1234_new_feature"
    path = tmpdir.join('file.txt')
    path.write("Subject line")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          to_trailer=True)
    assert path.read() == "Subject line\n\nRefs: JIRA-1234\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_to_trailer_multiple_tickets(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-1234-JIRA-5678"
    path = tmpdir.join('file.txt')
    path.write("Subject line")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}',
                          to_trailer=True)
    assert path.read() == "Subject line\n\nRefs: JIRA-1234, JIRA-5678\n"


@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_capitalize_disabled_by_default(mock_branch_name, tmpdir):
    mock_branch_name.return_value = "JIRA-1234_new_feature"
    path = tmpdir.join('file.txt')
    path.write("test commit message")
    update_commit_message(six.text_type(path), r'[A-Z]+-\d+',
                          'regex_match', '{ticket}: {commit_msg}')
    assert path.read() == "JIRA-1234: test commit message\n"


@pytest.mark.parametrize('msg', (
    """A descriptive header

A descriptive body.

Issue: 2397""",
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_no_modification_if_ticket_in_body(mock_branch_name, msg, tmpdir):
    mock_branch_name.return_value = "team_name/2397/a_nice_feature"
    path = tmpdir.join('file.txt')
    path.write(msg)
    update_commit_message(six.text_type(path), r'\d{4,}',
                          'regex_match', '{commit_msg}\n\nIssue: {ticket}')
    assert path.read() == msg


@pytest.mark.parametrize('msg', (
    """fixup! A descriptive header

A descriptive body.""",
))
@mock.patch(TESTING_MODULE + '.get_branch_name')
def test_update_commit_message_no_modification_if_commit_is_a_fixup(mock_branch_name, msg, tmpdir):
    mock_branch_name.return_value = "team_name/2397/a_nice_feature"
    path = tmpdir.join('file.txt')
    path.write(msg)
    update_commit_message(six.text_type(path), r'\d{4,}',
                          'regex_match', '{commit_msg}\n\nIssue: {ticket}')
    assert path.read() == msg


@mock.patch(TESTING_MODULE + '.subprocess')
def test_get_branch_name(mock_subprocess):
    get_branch_name()
    mock_subprocess.check_output.assert_called_once_with(
        [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ],
    )


@mock.patch(TESTING_MODULE + '.argparse')
@mock.patch(TESTING_MODULE + '.update_commit_message')
def test_main(mock_update_commit_message, mock_argparse):
    mock_args = mock.Mock()
    mock_args.filenames = ['foo.txt']
    mock_args.regex = None
    mock_args.format = None
    mock_args.mode = 'underscore_split'
    mock_args.conventionalcommits = True
    mock_args.capitalize = 0
    mock_args.to_trailer = False
    mock_argparse.ArgumentParser.return_value.parse_args.return_value = mock_args
    main()
    mock_update_commit_message.assert_called_once_with('foo.txt', r'[A-Z]+-\d+',
                                                       'underscore_split',
                                                       '{ticket} {commit_msg}',
                                                       True,
                                                       0,
                                                       False)


@mock.patch(TESTING_MODULE + '.update_commit_message')
def test_main_to_trailer_only_is_allowed(mock_update_commit_message):
    main(['foo.txt', '--to_trailer'])
    mock_update_commit_message.assert_called_once_with('foo.txt', r'[A-Z]+-\d+',
                                                       'underscore_split',
                                                       '{ticket} {commit_msg}',
                                                       False,
                                                       0,
                                                       True)


def test_main_errors_without_format_or_conventionalcommits_or_to_trailer():
    with pytest.raises(SystemExit):
        main(['foo.txt'])
