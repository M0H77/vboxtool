
import virtualbox

def create_vm(vbox, name, memory_size, cpu_count, storage_size):
    """
    create a new vm
    :param vbox:
    :param name:
    :param memory_size:
    :param cpu_count:
    :param storage_size:
    :return:
    """
    primary_group = ""
    create_flags = ""
    basefolder = ""
    settings_file = vbox.compose_machine_filename(
        name, primary_group, create_flags, basefolder
    )
    new_vm = vbox.create_machine(settings_file, name, [], "", create_flags)
    new_vm.cpu_count = int(cpu_count)
    new_vm.memory_size = int(memory_size)
    # new_vm.storage_controllers = int(storage_size)
    vbox.register_machine(new_vm)


def list_setting(vbox, vm):
    """
    list vm sittings
    :param vbox:
    :param vm:
    :return:
    """
    machine = vbox.find_machine(vm)
    print()
    print("Name: ", machine.name)
    print("cpu count: ", machine.cpu_count)
    print("memory size: ", machine.memory_size)
    print("os type: ", machine.os_type_id)
    print("snapshot count: ", machine.snapshot_count)
    print("state: ", machine.state)
    print("settings file path: ", machine.settings_file_path)
    print("hardware version: ", machine.hardware_version)
    print("hardware uuid: ", machine.hardware_uuid)


def list_vm(vbox, running_only=False):
    """
    list vms on host
    :param vbox:
    :param running_only:
    :return:
    """
    if running_only:
        print("VM(s):\n + %s" % "\n + ".join([vm.name for vm in vbox.machines if vm.state.__str__() == "FirstOnline"]))
    else:
        print("VM(s):\n + %s" % "\n + ".join([vm.name for vm in vbox.machines]))


def start_vm(vbox, session, vm):
    """
    start vm
    :param vbox:
    :param session:
    :param vm:
    :return:
    """
    machine = vbox.find_machine(vm)
    if machine.state.__str__() == "PoweredOff":
        proc = machine.launch_vm_process(session, "gui", [])
        proc.wait_for_completion(timeout=-1)
    else:
        print("vm is already on")


def stop_vm(vbox, vm):
    """
    stop vm
    :param vbox:
    :param vm:
    :return:
    """
    machine = vbox.find_machine(vm)
    session = machine.create_session()
    session.console.power_down()


def delete_vm(vbox, vm):
    """
    delete vm
    :param vbox:
    :param vm:
    :return:
    """
    machine = vbox.find_machine(vm)
    machine.remove(delete=True)


def main():
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()

    print("1. Create VM\n2. List available VMs\n3. Start VM\n4. Stop VM\n5. List VM settings\n6. Delete VM\n7. End")
    while True:
        print()
        task = input("Enter task number: ")
        # create VM
        if task == "1":
            try:
                name = input("choose vm name: ")
                memory_size = input("Enter memory size in bytes: ")
                cpu_count = input("Enter cpu count: ")
                storage_size = input("Enter storage size in GB: ")
                print("creating", name + "...")
                create_vm(vbox, name, memory_size, cpu_count, storage_size)
            except:
                print("Invalid input")
        # list VMs
        elif task == "2":
            list_vm(vbox)
        # start VM
        elif task == "3":
            try:
                list_vm(vbox)
                vm = input("Enter the name of the vm want to start : ")
                print("starting", vm + "...")
                start_vm(vbox, session, vm)
            except:
                print("Invalid vm name")
        # stop VM
        elif task == "4":
            try:
                list_vm(vbox, True)
                vm = input("Enter the name of the vm you want to stop : ")
                print("stopping", vm + "...")
                stop_vm(vbox, vm)
            except:
                print("Invalid vm name")
        # list settings
        elif task == "5":
            try:
                list_vm(vbox)
                vm = input("Enter the name of the vm to see settings: ")
                list_setting(vbox, vm)
            except:
                print("Invalid vm name")
        # delete VM
        elif task == "6":
            try:
                list_vm(vbox)
                vm = input("Enter the name of the vm you want to delete: ")
                if not input("Are you sure? (y/n): ").lower().strip()[:1] == "y": break
                delete_vm(vbox, vm)
                print(vm, "deleted")
            except:
                print("Invalid vm name")
        # end
        elif task == "7" or task == "exit":
            break
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()
