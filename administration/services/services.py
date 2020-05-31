import os, sys, shutil

from utilities.utilities import check_root, check_rendered

service_file_source = "services/libertas@.service"
service_file_target = "/etc/systemd/system/libertas@.service"
service_enabled_path = "/etc/systemd/system/multi-user.target.wants/"

def install(target):
    check_root()

    if not os.path.exists(service_file_target):
        check_rendered(service_file_source)

        shutil.copyfile(service_file_source, service_file_target)

    command = 'systemctl enable libertas@' + target
    
    os.system(command)

def disable(target):
    check_root()

    current_target_file = service_enabled_path + 'libertas@' + target + '.service'

    if os.path.exists(current_target_file):
        command = 'systemctl disable libertas@' + target
        os.system(command)

    files = [i for i in os.listdir(service_enabled_path) if os.path.isfile(os.path.join(service_enabled_path,i)) and 'libertas@' in i]
    
    if not files:
        if os.path.exists(service_file_target):
            os.remove(service_file_target)

    