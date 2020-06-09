from utilities.utilities import check_root, ask_confirm, drop_privileges

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

    package_list = ["docker-compose", "python3-toml", "python3-jinja2", "uidmap"]

    os.system("modprobe bridge")
    os.system("modprobe overlay permit_mounts_in_userns=1")

    with open('/etc/sysctl.conf', 'a') as file:
        file.write('net.ipv4.ip_unprivileged_port_start=0\n')

    os.system("sysctl --system")

    install_packages(package_list)

    drop_privileges()

    install_docker_rootless()

def install_docker_rootless():
    os.system("curl -fsSL https://get.docker.com/rootless | sh")

    os.system("export PATH=/home/$(whoami)/bin:$PATH")
    os.system("export XDG_RUNTIME_DIR=/run/user/$UID")
    os.system("export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock")
    os.system("systemctl --user start docker")
    os.system("docker network create backend")
    os.system("docker network create frontend")