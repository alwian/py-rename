import argparse
import os
import re


def rename_item(path):
    """Rename a file or directory using patterns provided via the command line."""

    # Extract file information
    item_name = os.path.basename(path)
    item_extension = item_name.split('.', maxsplit=1)[-1]
    item_root = os.path.dirname(path)

    # Find groups specified by the user
    initial_groups = re.search(args.initial, item_name)

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
    if item_extension != item_name:
        result = result + '.' + item_extension

    # Rename the file
    os.rename(path, os.path.join(item_root, result))


if __name__ == "__main__":
    # Setup argument parsing
    parser = argparse.ArgumentParser(
        description='Bulk rename files using regex',
        epilog='Report any issues at - https://github.com/alwian/py-rename/issues'
    )
    rename_type = parser.add_mutually_exclusive_group(required=True)
    rename_type.add_argument('-f', '--files', action='store_true', help='rename files')
    rename_type.add_argument('-d', '--directories', action='store_true', help='rename directories')
    parser.add_argument('-s', '--subdirectories', action='store_true', help='rename items inside of subdirectories')
    parser.add_argument('directory', help="the directory containing items to be renamed", )
    parser.add_argument("initial", help="the initial regex pattern of all items to be renamed")
    parser.add_argument("desired", help="the desired  pattern of all items to be renamed")
    args = parser.parse_args()

    # Check provided directory is valid
    if not os.path.isdir(args.directory):
        parser.error("'{0}' is not a valid directory.".format(args.directory))

    # If subdirectories flag specified
    if args.subdirectories:
        for root, dirs, files in os.walk(args.directory):
            # Rename files
            if args.files:
                for file in files:
                    rename_item(os.path.join(root, file))
            # Rename directories
            elif args.directories:
                for directory in dirs:
                    rename_item(os.path.join(root, directory))
    # If only renaming inside of specified directory
    else:
        for item in os.listdir(args.directory):
            # Rename files
            if args.files and os.path.isfile(os.path.join(args.directory, item)):
                rename_item(os.path.join(args.directory, item))
            # Rename directories
            elif args.directories and os.path.isdir(os.path.join(args.directory, item)):
                rename_item(os.path.join(args.directory, item))
