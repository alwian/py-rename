import argparse
import os
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help="The directory containing files to be renamed.", )
    parser.add_argument("initial", help="The initial regex pattern of all files to be renamed.")
    parser.add_argument("desired", help="The desired  pattern of all files to be renamed.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        parser.error("'{0}' is not a valid directory.".format(args.directory))

    for file in os.listdir(args.directory):
        if os.path.isfile(os.path.join(args.directory, file)):
            initial_groups = re.search(args.initial, file)

            if initial_groups is not None:
                initial_groups = initial_groups.groupdict()
            else:
                continue

            desired_groups = re.findall(r'\[.+\]', args.desired)

            result = args.desired

            for group in desired_groups:
                result = result.replace(group, initial_groups[group.replace('[', '').replace(']', '')])

            os.rename(os.path.join(args.directory, file), os.path.join(args.directory, result))
