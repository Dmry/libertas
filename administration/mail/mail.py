import docker, os, sys

from utilities.utilities import check_root, ask_confirm, check_rendered

def get_database_container():
    client = docker.from_env()

    containers = client.containers.list()

    for container in containers:
        if container.attrs['Name'] == '/mariadb':
            return container


def exec_sql(container, sql):
    check_root()

    import toml

    config_data = toml.loads(open('./config.toml', 'r').read())

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

def setup():
    check_root()

    container = get_database_container

    script_location = '../database/scripts/db-init.sql'

    check_rendered(script_location)

    sql = open('../database/scripts/').read()

    exec_sql(container, sql)
