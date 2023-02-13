import os

import inotify.adapters


def main():
    i = inotify.adapters.Inotify()
    base_target = '/sys/class/backlight'
    dynamic_amd_folder_current_name = ''
    nvidia_target = '/sys/class/backlight/nvidia_wmi_ec_backlight/brightness'
    directory_list = list()
    for root, dirs, files in os.walk(base_target, topdown=False):
        for name in dirs:
            if 'amdgpu_bl' in name.strip():
                dynamic_amd_folder_current_name = name
                print(name)

    amd_target = f'/sys/class/backlight/{dynamic_amd_folder_current_name}/brightness'
    i.add_watch(nvidia_target)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if type_names == ['IN_MODIFY']:
            with open(nvidia_target, "r") as f:
                nvidia_brightness = f.read().strip()
                percent = int(nvidia_brightness) / 255 * 100
                with open(amd_target, 'w+') as amd:
                    amd.write(str(int(percent)))


if __name__ == '__main__':
    main()
