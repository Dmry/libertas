import argparse

from base import template, dependencies
from services import services
from mail import database, setup
from extras import security

## TODO: Check current directory to see if we are indeed in libertas/administration

services_list = ['database', 'dockermail', 'matrix', 'nextcloud', 'ouroboros', 'traefik']


parser = argparse.ArgumentParser(description='Administration tool for routine tasks for Libertas.')
sub = parser.add_subparsers()

'''
Base setup: config templating & core dependencies
'''

base_function_map = {'clean'  : template.clean,
                     'render' : template.render,
                     'dependencies' : dependencies.dependencies}

parser_init = sub.add_parser('base', help='Configuration templating & core dependencies.')
parser_init.add_argument('base_command', choices=base_function_map.keys())


'''
Services management
'''

services_function_map = {'install' : services.install,
                         'disable' : services.disable}

parser_services = sub.add_parser('services', help='Set up and manage systemd services.')
parser_services.add_argument('services_command', choices=services_function_map.keys())
parser_services.add_argument('target', choices=services_list)


'''
Mail configuration
'''

parser_mail = sub.add_parser('mail', help='Manage mail dependencies and database')
sub_parser_mail = parser_mail.add_subparsers()

maildb_function_map = {'clean'  : database.clean,
                       'setup'  : database.init_database}

parser_mail_database = sub_parser_mail.add_parser('database', help='Manage mail database.')
parser_mail_database.add_argument('maildb_command', choices=maildb_function_map.keys())

maildep_function_map = {'opendkim'     : setup.opendkim,
                        'letsencrypt'  : setup.letsencrypt,
                        'bcrypt'       : setup.bcrypt}

parser_mail_dependencies = sub_parser_mail.add_parser('dependencies', help='Setting up dependencies for mail.')
parser_mail_dependencies.add_argument('maildep_command', choices=maildep_function_map.keys())


'''
Extras
'''

security_function_map = {'fail2ban' : security.fail2ban}

parser_security = sub.add_parser('security', help='Set up security extras.')
parser_security.add_argument('security_command', choices=security_function_map.keys())

'''
Parse
'''

args = parser.parse_args()

if (hasattr(args, 'base_command')):
    execute = base_function_map[args.base_command]()

if (hasattr(args, 'services_command')):
    services_function_map[args.services_command](args.target)

if (hasattr(args, 'maildb_command')):
    execute = maildb_function_map[args.maildb_command]()

if (hasattr(args, 'maildep_command')):
    execute = maildep_function_map[args.maildep_command]()

if (hasattr(args, 'security_command')):
    execute = security_function_map[args.security_command]()