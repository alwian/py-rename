import argparse
import os
import re


def rename_file(file_path):
    """Rename a file using patterns provided via the command line."""

    # Extract file information
    filename = os.path.basename(file_path)
    file_extension = filename.split('.', maxsplit=1)[-1]
    directory = os.path.dirname(file_path)

    # Find groups specified by the user
    initial_groups = re.search(args.initial, filename)

    # If groups found, get dict of groups so values can be retrieved
    if initial_groups is not None:
        initial_groups = initial_groups.groupdict()
    else:
        return

    # Find all groups the users wishes to reuse
    desired_groups = re.findall(r'\[.+\]', args.desired)

    # Make a copy of the desired filename pattern
    result = args.desired

    # Replace group names in desired filename with the relevant values
    for group in desired_groups:
        result = result.replace(group, initial_groups[group.replace('[', '').replace(']', '')])

    # If file had an extension, add it back on
    if file_extension != filename:
        result = result + '.' + file_extension

    # Rename the file
    os.rename(file_path, os.path.join(directory, result))


if __name__ == "__main__":
    # Setup argument parsing
    parser = argparse.ArgumentParser(
        description='Bulk rename files using regex',
        epilog='Report any issues at - https://github.com/alwian/py-rename/issues'
    )
    parser.add_argument('-s', '--subdirectories', action='store_true', help='rename files inside of subdirectories')
    parser.add_argument('directory', help="the directory containing files to be renamed", )
    parser.add_argument("initial", help="the initial regex pattern of all files to be renamed")
    parser.add_argument("desired", help="the desired  pattern of all files to be renamed")
    args = parser.parse_args()

    # Check provided directory is valid
    if not os.path.isdir(args.directory):
        parser.error("'{0}' is not a valid directory.".format(args.directory))

    # If subdirectories flag specified
    if args.subdirectories:
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                rename_file(os.path.join(root, file))
    # If only renaming inside of specified directory
    else:
        for file in os.listdir(args.directory):
            rename_file(os.path.join(args.directory, file))
