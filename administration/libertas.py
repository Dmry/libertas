import argparse

from init import template, dependencies
from services import services
from mail import database, setup

## TODO: Check current directory to see if we are indeed in libertas/administration

services_list = ['database', 'dockermail', 'matrix', 'nextcloud', 'ouroboros', 'traefik']


parser = argparse.ArgumentParser(description='Administration tool for routine tasks for Libertas.')
sub = parser.add_subparsers()

'''
Configuration templating
'''

init_function_map = {'clean'  : template.clean,
                     'render' : template.render,
                     'dependencies' : dependencies.dependencies}

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
Mail database management
'''

maildb_function_map = {'clean'  : database.clean,
                       'setup'  : database.init_database}

parser_maildb = sub.add_parser('maildb', help='Manage mail database.')
parser_maildb.add_argument('maildb_command', choices=maildb_function_map.keys())


'''
Mail setup
'''

mailsetup_function_map = {'opendkim'     : setup.opendkim,
                          'letsencrypt'  : setup.letsencrypt}

parser_mailsetup = sub.add_parser('mailsetup', help='Setting up dependencies for mail.')
parser_mailsetup.add_argument('mailsetup_command', choices=mailsetup_function_map.keys())


'''
Parse
'''

args = parser.parse_args()

if (hasattr(args, 'init_command')):
    execute = init_function_map[args.init_command]()

if (hasattr(args, 'services_command')):
    services_function_map[args.services_command](args.target)

if (hasattr(args, 'maildb_command')):
    execute = maildb_function_map[args.maildb_command]()

if (hasattr(args, 'mailsetup_command')):
    execute = mailsetup_function_map[args.mailsetup_command]()