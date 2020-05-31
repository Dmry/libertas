# For root check
import sys, os, ntpath

def get_filename_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def check_root():
    if (os.getuid() != 0):
        sys.exit("Please execute this command as root.")

def check_rendered(path):
    if not os.path.exists(path):
        filename = get_filename_from_path(path)
        sys.exit(f"Rendered {filename} not found, please render template using the command 'init render'.")

def ask_confirm(message):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(message + " [Y/N]").lower()
    return answer == "y"