import os

template_list = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".template"):
            template_list.append(os.path.join(root, file))

for template_file in template_list:
    os.remove(os.path.splitext(template_file)[0])