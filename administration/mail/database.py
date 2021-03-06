import docker, os, sys, subprocess, getpass

from utilities.utilities import drop_privileges, ask_confirm, check_rendered
from base.template import get_config

def get_database_container():
    drop_privileges()
    
    client = docker.from_env()

    containers = client.containers.list()

    for container in containers:
        if container.attrs['Name'] == '/mariadb':
            return container


def exec_sql(container, sql):
    config_data = get_config()

    container.exec_run("mysql -u root -p" + config_data['database']['passwords']['root'])

def clean():
    if not ask_confirm("This will remove ALL e-mail users and domains from database. Proceed?"):
        return

    container = get_database_container()

    # Clear mailuser
    exec_sql(container, "DROP USER mailuser")

    # Remove mail donamins
    exec_sql(container, "DELETE FROM `mailserver`.`virtual_domains`")

def init_database():
    container = get_database_container()

    script_location = '../database/scripts/db-init.sql'

    check_rendered(script_location)

    sql = open(script_location).read()

    exec_sql(container, sql)

def add_user():
    from passlib.hash import bcrypt

    container = get_database_container()

    username = input("Please specify a username:\n")

    try: 
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")

        if password == confirm:
            hash = bcrypt.using(rounds=5).hash(password)
        else:
            sys.exit("Passwords did not match!")
    except Exception as error: 
        print('ERROR', error) 

    sql = f"INSERT INTO `mailserver`.`virtual_users` (domain_id, password , email) VALUES ('1', '{hash}', '{username}');"

    exec_sql(container, sql)

