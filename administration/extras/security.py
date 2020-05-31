from utilities.utilities import check_root, check_rendered
from base.dependencies import install_packages

import fileinput
from shutil import copy

# For installing dependencies
import apt

def fail2ban():
    check_root()

    package_list = ['fail2ban']

    install_packages(package_list)

    containers = ['dovecot', 'postfix']

    for item in containers:
        copy(f"fail2ban-{item}-action.conf", "/etc/fail2ban/action.d/")
        copy(f"fail2ban-{item}-filter.conf", "/etc/fail2ban/filter.d/")

    copy("jail.local", "/etc/fail2ban/")

    ssh_port = input("ssh port?")

    with fileinput.FileInput("/etc/fail2ban/jail.local", inplace=True, backup='.bak') as file:
        for line in file:
            line.replace("port = ssh", "port = " + ssh_port)

