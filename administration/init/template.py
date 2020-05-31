from jinja2 import Environment, FileSystemLoader

from utilities.utilities import check_root, ask_confirm

# Scoped import for toml below, as not to error upon dependency install

# For finding template files
import os

# For installing dependencies
import apt

# Load all template file locations in current directory
def get_template_list():
    template_list = []

    for root, dirs, files in os.walk("../"):
        for file in files:
            if file.endswith(".template"):
                template_list.append(os.path.abspath(os.path.join(root, file)))

    return template_list

def clean():
    for template_file in get_template_list():
        file = os.path.splitext(template_file)[0]

        if os.path.exists(file):
            os.remove(file)

def render():
    import toml

    # Load config for Jinja
    config_data = toml.loads(open('./config.toml', 'r').read())

    # Set up Jinja environment
    env = Environment(loader = FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True)

    for template_file in get_template_list():
        template = env.get_template(template_file)

        # Fill in the template
        result = template.render(config_data)
        # Write result to file without the .template extension
        outfile = open(os.path.splitext(template_file)[0], 'w')
        outfile.write(result)
        outfile.close()

def install_package(cache, name):
    pkg = cache[name]
    if pkg.is_installed:
        print(f"{name} already installed")
    else:
        pkg.mark_install()

        cache.commit()

def dependencies():
    check_root()

    if not ask_confirm("This will install software on your computer.\nIf you're sceptical, please check out administration/init/template.py.\nContinue?"):
        return
    
    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    package_list = ["docker.io", "docker-compose", "python3-toml", "python3-jinja2"]

    for package in package_list:
        install_package(cache, package)

    os.system("systemctl start docker")
    os.system("docker network create backend")
    os.system("docker network create frontend")