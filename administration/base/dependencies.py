from utilities.utilities import check_root, ask_confirm

import os

# For installing dependencies
import apt

def install_packages(list):
    if not ask_confirm("This will install software on your computer.\nIf you're sceptical, please check out the corresponding scripts.\nContinue?"):
        return

    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    for name in list:

        pkg = cache[name]
        if pkg.is_installed:
            print(f"{name} already installed")
        else:
            pkg.mark_install()

            cache.commit()

def dependencies():
    check_root()

    package_list = ["docker.io", "docker-compose", "python3-toml", "python3-jinja2"]

    install_packages(package_list)

    os.system("systemctl start docker")
    os.system("docker network create backend")
    os.system("docker network create frontend")