#!/usr/bin/env python
# coding: utf-8

import semantic_version
import datetime
import re
import os
import sys
import getopt
import json


def usage():
    print(f"Usage: \n"
          f"-h | --help      [ See usage for script ]\n"
          f"-e | --env       [ Export version metadata to environment file ]\n"
          f"-j | --json      [ Export version metadata to JSON file ]\n"
          f"-d | --directory [ Directory to save .env and JSON files ]\n"
          f"\n"
          f"autoversioner -v 'v2024.1.4'\n"
          f"autoversioner -v '2024.1.4'\n"
          f"autoversioner -v '1.10.4' --json --directory '~/Downloads' --env\n")


def version(current_version):
    date_pattern = re.compile(r'20[1-2][0-9]')

    if date_pattern.search(current_version):
        today = datetime.date.today()
        year = today.strftime("%Y")
        month = int(today.strftime("%m"))
        date = f"{year}.{month}"
        if current_version == "":
            new_version = f'{date}.0'
        else:
            current_version = semantic_version.Version(current_version)
            s = semantic_version.SimpleSpec(f'<{date}.0')
            new_version = f'{date}.0'
            if s.match(current_version):
                new_version = f'{date}.0'

            s = semantic_version.SimpleSpec(f'=={date}.{current_version.patch}')
            if s.match(current_version):
                new_version = current_version.next_patch()
                new_version = f'{str(new_version)}'
        return new_version
    else:
        current_version = semantic_version.Version(current_version)
        new_version = current_version.next_patch()
        return new_version


def output(metadata=None, json_output=False, env_output=False, print_output=False, directory=""):
    if not metadata:
        print("No metadata supplied to output")
        return
    if json_output:
        json_file_path = os.path.join(directory, 'version.json')
        # Write the dictionary to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(metadata, json_file, indent=2)
    if env_output:
        env_content = "\n".join([f"{key}={value}" for key, value in metadata.items()])
        env_file_path = os.path.join(directory, '.env')
        # Save the content to the .env file
        with open(env_file_path, 'w') as env_file:
            env_file.write(env_content)
    if print_output:
        print(f"{metadata['new_version']}")


def autoversioner(argv):
    current_version = '0.0.0'
    directory = ""
    environment_output = False
    json_output = False
    try:
        opts, args = getopt.getopt(argv, "hejd:v:", ["help", "env", "json", "directory=", "version="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--env"):
            environment_output = True
        elif opt in ("-d", "--directory"):
            directory = os.path.normpath(arg)
        elif opt in ("-j", "--json"):
            json_output = True
        elif opt in ("-v", "--version"):
            current_version = arg

    current_version = re.sub("v", "", current_version)

    new_version = version(current_version=current_version)

    version_metadata = {
        "current_version": current_version,
        "new_version": new_version,
        "current_version_tag": f"v{current_version}",
        "new_version_tag": f"v{new_version}",
    }

    output(metadata=version_metadata,
           json_output=json_output,
           env_output=environment_output,
           print_output=True,
           directory=directory)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    autoversioner(sys.argv[1:])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    autoversioner(sys.argv[1:])
