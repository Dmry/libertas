from utilities.utilities import check_root, chown_recursive
from base.template import get_config
from base.dependencies import install_packages
from pathlib import Path
from termcolor import colored

import shutil, os, grp, pwd

def opendkim():
    check_root()

    domain = get_config()['general']['domain']

    package_list = ['opendkim', 'opendkim-tools']

    install_packages(package_list)

    Path("/etc/opendkim/").mkdir(parents=True, exist_ok=True)

    os.system(f"opendkim-genkey -b 2048 -r -h rsa-sha256 -d {domain} -s /etc/opendkim/mail")

    shutil.move("/etc/opendkim/mail.private", "/etc/opendkim/mail")

    uid = pwd.getpwnam("opendkim").pw_uid
    gid = grp.getgrnam("opendkim").gr_gid

    chown_recursive("/etc/opendkim", uid, gid)

    os.system("chmod -R go-rwx /etc/opendkim")

    print(colored("Please add the DNS entry listed in /etc/opendkim/mail.txt to your DNS", 'red'))

def letsencrypt():
    check_root()

    package_list = ['certbot']

    domain = get_config()['general']['domain']

    install_packages(package_list)

    os.system(f"certbot certonly -d {domain}")

    with open("/var/spool/cron/crontabs/root", 'a') as file:
        file.write("0 4 1 * * letsencrypt renew")

def bcrypt():
    check_root()

    package_list = ['python3-passlib', 'python3-bcrypt']

    install_packages(package_list)

