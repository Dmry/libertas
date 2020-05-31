import argparse

from init import template
from services import services

services_list = ['database', 'dockermail', 'matrix', 'nextcloud', 'ouroboros', 'traefik']


parser = argparse.ArgumentParser(description='Administration tool for routine tasks for Libertas.')
sub = parser.add_subparsers()

'''
Configuration templating
'''

init_function_map = {'clean'  : template.clean,
                     'render' : template.render,
                     'dependencies' : template.dependencies}

parser_init = sub.add_parser('init', help='Initialize and manage configuration files.')
parser_init.add_argument('init_command', choices=init_function_map.keys())


'''
Services management
'''

services_function_map = {'install' : services.install,
                         'disable' : services.disable}

parser_services = sub.add_parser('services', help='Set up and manage systemd services.')
parser_services.add_argument('services_command', choices=services_function_map.keys())
parser_services.add_argument('target', choices=services_list)


'''
Parse
'''

args = parser.parse_args()

if (hasattr(args, 'init_command')):
    execute = init_function_map[args.init_command]()

if (hasattr(args, 'services_command')):
    services_function_map[args.services_command](args.target)