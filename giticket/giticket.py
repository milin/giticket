# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io
import re
import subprocess
import sys

import six

UNDERSCORE_SPLIT_MODE = 'underscore_split'
REGEX_MATCH_MODE = 'regex_match'


def update_commit_message(filename, regex, mode, format_string):
    # All escape sequences will be escaped with double backslash, so need to
    # replace escaped new-line character with normal one
    format_string = format_string.replace('\\n', '\n')

    with io.open(filename, 'r+') as fd:
        contents = fd.readlines()
        commit_msg = contents[0].rstrip('\r\n')
        # Check if we can grab ticket info from branch name.
        branch = get_branch_name()

        # Bail if commit message already contains tickets
        if any(re.search(regex, content) for content in contents):
            return

        tickets = re.findall(regex, branch)
        if tickets:
            if mode == UNDERSCORE_SPLIT_MODE:
                tickets = [branch.split(six.text_type('_'))[0]]
            tickets = [t.strip() for t in tickets]

            new_commit_msg = format_string.format(
                ticket=tickets[0], tickets=', '.join(tickets),
                commit_msg=commit_msg
            )

            contents[0] = six.text_type(new_commit_msg + "\n")
            fd.seek(0)
            fd.writelines(contents)
            fd.truncate()


def get_branch_name():
    # Only git support for right now.
    return subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ],
    ).decode('UTF-8')


def get_args(argv=None):
    """Parse and return all args passed to script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--regex')
    parser.add_argument('--format')
    parser.add_argument('--mode', nargs='?', const=UNDERSCORE_SPLIT_MODE,
                        default=UNDERSCORE_SPLIT_MODE,
                        choices=[UNDERSCORE_SPLIT_MODE, REGEX_MATCH_MODE])
    return parser.parse_args(argv)


def main(argv=None):
    """This hook saves developers time by prepending ticket numbers to commit-msgs.
    For this to work the following two conditions must be met:

        - The ticket format regex specified must match.
        - The branch name format must be <ticket number>_<rest of the branch name>
    """
    args = get_args(argv)
    regex = args.regex or r'[A-Z]+-\d+'  # noqa
    format_string = args.format or '{ticket} {commit_msg}' # noqa
    update_commit_message(args.filenames[0], regex, args.mode, format_string)


if __name__ == '__main__':
    sys.exit(main())
