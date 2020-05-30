from jinja2 import Environment, FileSystemLoader

# Used for user configuration
import toml

# For finding template files
import os

# Load config for Jinja
config_data = toml.loads(open('./config.toml', 'r').read())

# Load all template file locations in current directory
template_list = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".template"):
            template_list.append(os.path.join(root, file))

# Set up Jinja environment
env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

for template_file in template_list:
    template = env.get_template(template_file)

    # Fill in the template
    result = template.render(config_data)

    # Write result to file without the .template extension
    outfile = open(os.path.splitext(template_file)[0], 'w')
    outfile.write(result)
    outfile.close()
