# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io
import sys
import six


def update_commit_message(filename, format_string):
    with io.open(filename, 'r+') as fd:
        contents = fd.readlines()
        commit_msg = contents[0].rstrip('\r\n')
        new_commit_msg = format_string.format(commit_msg=commit_msg)
        contents[0] = six.text_type(new_commit_msg + "\n")
        fd.seek(0)
        fd.writelines(contents)
        fd.truncate()

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--format_string')
    args = parser.parse_args(argv)
    update_commit_message(args.filenames[0], args.format_string)

if __name__ == '__main__':
    sys.exit(main())
