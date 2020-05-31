from jinja2 import Environment, FileSystemLoader

from utilities.utilities import check_root, ask_confirm

# Scoped import for toml below, as not to error upon dependency install

# For finding template files
import os

def get_config():
    import toml

    # Load config for Jinja
    return toml.loads(open('./config.toml', 'r').read())

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
    config_data = get_config()

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