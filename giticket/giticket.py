# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io
import re
import subprocess
import sys

import six

underscore_split_mode = 'underscore_split'
regex_match_mode = 'regex_match'
conventionalcommit_regex = r'^(?P<type>build|chore|ci|docs|feat|fix|perf|refactor|style|test)(\((?P<scope>.+)\))?: (?P<subject>.+)'

def update_commit_message(filename, regex, mode, format_string, conventionalcommits=False):
    with io.open(filename, 'r+') as fd:
        contents = fd.readlines()
        commit_msg = contents[0].rstrip('\r\n')
        # Check if we can grab ticket info from branch name.
        branch = get_branch_name()

        # Bail if commit message starts with “fixup!” or commit message already contains tickets
        if commit_msg.startswith('fixup!') or any(re.search(regex, content) for content in contents):
            return

        tickets = re.findall(regex, branch)
        if tickets:
            if mode == underscore_split_mode:
                tickets = [branch.split(six.text_type('_'))[0]]
            tickets = [t.strip() for t in tickets]

            if conventionalcommits and (match := re.match(conventionalcommit_regex, commit_msg)):
                # If the commit message matches the Conventional Commits spec, we can use the captured groups.
                type = match.group('type')
                scope = match.group('scope')
                if scope:
                    scope = scope + ',' + ', '.join(tickets)
                else:
                    scope = ', '.join(tickets)
                subject = match.group('subject')
                format_string = '{type}({scope}): {subject}'
                new_commit_msg = format_string.format(
                    type=type, scope=scope, subject=subject
                )
            else:
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


def main(argv=None):
    """This hook saves developers time by prepending ticket numbers to commit-msgs.
    For this to work the following two conditions must be met:

        - The ticket format regex specified must match.
        - The branch name format must be <ticket number>_<rest of the branch name>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--conventionalcommits', action='store_true')
    parser.add_argument('--regex')
    parser.add_argument('--format', nargs='?')
    parser.add_argument('--mode', nargs='?', const=underscore_split_mode,
                        default=underscore_split_mode,
                        choices=[underscore_split_mode, regex_match_mode])
    args = parser.parse_args(argv)
    if not args.conventionalcommits and not args.format:
        parser.error('You must provide --format if not using --conventionalcommits')
        return 1
    regex = args.regex or r'[A-Z]+-\d+'  # noqa
    format_string = args.format or '{ticket} {commit_msg}' # noqa
    update_commit_message(args.filenames[0], regex, args.mode, format_string, args.conventionalcommits)


if __name__ == '__main__':
    sys.exit(main())
