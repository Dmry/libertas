import os, sys, shutil

service_file_source = "systemd/libertas@.service"
service_file_target = "/etc/systemd/system/libertas@.service"
service_enabled_path = "/etc/systemd/system/multi-user.target.wants/"

def check_root():
    if (os.getuid() != 0):
        sys.exit("Please execute this command as root.")

def install(target):
    check_root()

    if not os.path.exists(service_file_target):
        if not os.path.exists(service_file_source):
            sys.exit("Rendered libertas@.service not found, please render template using the command 'init render'.")

        shutil.copyfile(service_file_source, service_file_target)

    command = 'systemctl enable --now libertas@' + target
    
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

    