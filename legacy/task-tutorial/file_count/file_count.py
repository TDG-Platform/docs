"""
Usage:
    count_files.py <directory> [--recursive]

Counts files in a directory.

Options:
    -r --recursive  Execute recursively
"""


import os
import json
from docopt import docopt


def count_files_in_directory(src, is_recursive):
    file_count = 0

    if not os.path.isdir(src):
        raise NotADirectoryError('{_src} is not a directory.'.format(_src=src))

    list_dir = os.listdir(src)

    for item in list_dir:
        full_path = os.path.join(src, item)

        if os.path.isfile(full_path):
            file_count += 1
        elif os.path.isdir(full_path) and is_recursive:
            file_count += count_files_in_directory(full_path, recursive)

    return file_count


if __name__ == "__main__":
    arguments = docopt(__doc__)

    src_dir = arguments['<directory>']
    recursive = arguments['--recursive']

    result = {
        'directory': src_dir,
        'is_recursive': recursive,
        'file_count': count_files_in_directory(src_dir, recursive)
    }

    print('Directory {_dir} contains {_file_count} files{_rec}.'
          .format(_dir=src_dir, _file_count=result['file_count'], _rec='' if not recursive else ' including subdirectories'))

    with open('file_count.json', 'w') as outfile:
        json.dump(result, outfile)
