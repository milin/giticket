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
    update_commit_message(six.text_type(path), '[A-Z]+-\d+',
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
    update_commit_message(six.text_type(path), '[A-Z]+-\d+',
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
    update_commit_message(six.text_type(path), '[A-Z]+-\d+',
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
    update_commit_message(six.text_type(path), '[A-Z]+-\d+',
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
    update_commit_message(six.text_type(path), '[A-Z]+-\d+',
                          'regex_match', '{tickets}: {commit_msg}')
    assert path.read() == '{expected_tickets}: {message}'.format(
        expected_tickets=test_data[1], message=COMMIT_MESSAGE
    )


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
    mock_argparse.ArgumentParser.return_value.parse_args.return_value = mock_args
    main()
    mock_update_commit_message.assert_called_once_with('foo.txt', '[A-Z]+-\d+',
                                                       'underscore_split',
                                                       '{ticket} {commit_msg}')
