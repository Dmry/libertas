import os, sys, shutil

from utilities.utilities import check_root, check_rendered, drop_privileges

service_file_source = "services/libertas@.service"
service_file_target = "/etc/systemd/user/libertas@.service"
service_enabled_path = "/etc/systemd/user/multi-user.target.wants/"

def install(target):
    check_root()

    if not os.path.exists(service_file_target):
        check_rendered(service_file_source)

        shutil.copyfile(service_file_source, service_file_target)

    drop_privileges()

    command = 'systemctl --user enable libertas@' + target
    
    os.system(command)

def disable(target):
    drop_privileges()

    current_target_file = service_enabled_path + 'libertas@' + target + '.service'

    if os.path.exists(current_target_file):
        command = 'systemctl --user disable libertas@' + target
        os.system(command)

def clean():
    check_root()

    files = [i for i in os.listdir(service_enabled_path) if os.path.isfile(os.path.join(service_enabled_path,i)) and 'libertas@' in i]
    
    if not files:
        if os.path.exists(service_file_target):
            os.remove(service_file_target)
    else:
        print("There are still services enabled, please disable first.")

    