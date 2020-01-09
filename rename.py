import argparse
import os
import re


def rename_file(file_path):
    filename = os.path.basename(file_path)
    file_extension = filename.split('.', maxsplit=1)[-1]
    directory = os.path.dirname(file_path)

    initial_groups = re.search(args.initial, filename)

    if initial_groups is not None:
        initial_groups = initial_groups.groupdict()
    else:
        return

    desired_groups = re.findall(r'\[.+\]', args.desired)

    result = args.desired

    for group in desired_groups:
        result = result.replace(group, initial_groups[group.replace('[', '').replace(']', '')])

    if file_extension != filename:
        result = result + '.' + file_extension

    os.rename(file_path, os.path.join(directory, result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subdirectories', action='store_true', help='Rename files inside of subdirectories.')
    parser.add_argument('directory', help="The directory containing files to be renamed.", )
    parser.add_argument("initial", help="The initial regex pattern of all files to be renamed.")
    parser.add_argument("desired", help="The desired  pattern of all files to be renamed.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        parser.error("'{0}' is not a valid directory.".format(args.directory))

    if args.subdirectories:
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                rename_file(os.path.join(root, file))
    else:
        for file in os.listdir(args.directory):
            rename_file(os.path.join(args.directory, file))
