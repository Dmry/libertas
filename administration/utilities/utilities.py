# For root check
import sys, os, ntpath, pwd, grp

def get_filename_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def check_root():
    if (os.getuid() != 0):
        sys.exit("Please execute this command as root.")

def drop_privileges():
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    user_name = os.getenv("SUDO_USER")
    pwnam = pwd.getpwnam(user_name)

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def check_rendered(path):
    if not os.path.exists(path):
        filename = get_filename_from_path(path)
        sys.exit(f"Rendered {filename} not found, please render template using the command 'init render'.")

def ask_confirm(message):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(message + " [Y/N]").lower()
    return answer == "y"

def chown_recursive(path, uid, gid):
    os.chown(path, uid, gid)
    
    for root, dirs, files in os.walk(path):  
        for dir in dirs:  
            os.chown(os.path.join(root, dir), uid, gid)
        for file in files:
            os.chown(os.path.join(root, file), uid, gid)