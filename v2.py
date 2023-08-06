import os
import json
import shutil
import argparse

def create_links(source_path, destination_path):
    # Check if the source and destination are on the same filesystem
    if os.path.exists(destination_path) and os.path.samefile(source_path, destination_path):
        # If they are on the same filesystem, create a hard link
        try:
            shutil.link(source_path, destination_path)
            print(f"Hard link created for '{source_path}' at '{destination_path}'")
        except Exception as e:
            print(f"Failed to create hard link for '{source_path}': {e}")
    else:
        # If they are on different filesystems, create a symbolic (soft) link
        try:
            os.symlink(source_path, destination_path)
            print(f"Symbolic link created for '{source_path}' at '{destination_path}'")
        except Exception as e:
            print(f"Failed to create symbolic link for '{source_path}': {e}")

def create_links_in_destination(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, _, files in os.walk(source_folder):
        for filename in files:
            src_file_path = os.path.join(root, filename)
            dst_file_extension = os.path.splitext(filename)[1]
            dst_subfolder = os.path.join(destination_folder, dst_file_extension[1:])

            if not os.path.exists(dst_subfolder):
                os.makedirs(dst_subfolder)

            dst_file_path = os.path.join(dst_subfolder, filename)

            create_links(src_file_path, dst_file_path)

def main():
    parser = argparse.ArgumentParser(description="Create hardlinks or symbolic links for files in a specified folder.")
    parser.add_argument("source_folder", help="Specify the source folder.")
    args = parser.parse_args()

    source_folder = args.source_folder

    # Read the destination folder from the config file
    config_file = "v2.json"  # Replace with the path to your config file
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            destination_folder = config["destination_folder"]
            create_links_in_destination(source_folder, destination_folder)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
