import docker, os, sys

from utilities.utilities import check_root, ask_confirm, check_rendered
from init.template import get_config

def get_database_container():
    client = docker.from_env()

    containers = client.containers.list()

    for container in containers:
        if container.attrs['Name'] == '/mariadb':
            return container


def exec_sql(container, sql):
    check_root()

    config_data = get_config()

    container.exec_run("mysql -u root -p" + config_data['database']['passwords']['root'])

def clean():
    if not ask_confirm("This will remove ALL e-mail users and domains from database. Proceed?"):
        return

    check_root()

    container = get_database_container()

    # Clear mailuser
    exec_sql(container, "DROP USER mailuser")

    # Remove mail donamins
    exec_sql(container, "DELETE FROM `mailserver`.`virtual_domains`")

def init_database():
    check_root()

    container = get_database_container()

    script_location = '../database/scripts/db-init.sql'

    check_rendered(script_location)

    sql = open(script_location).read()

    exec_sql(container, sql)
