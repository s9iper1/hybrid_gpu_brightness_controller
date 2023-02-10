import inotify.adapters


def main():
    i = inotify.adapters.Inotify()
    nvidia_target = '/sys/class/backlight/nvidia_wmi_ec_backlight/brightness'
    amd_target = '/sys/class/backlight/amdgpu_bl1/brightness'
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
