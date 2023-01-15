from getinfo import get_info
from getsource import get_source
import subprocess
import os

def install(pkg,*args):
    link = get_info('link', pkg) if not '.org' in pkg else pkg
    if link is None:
        print(f"Couldn't find link for {pkg}")
        return
    src = get_source(link)
    name = pkg if not '.org' in pkg else get_info('name', link)
    depends = get_info('depends', name) or None
    on_pacman = get_info('pacman', name)
    installed = get_info('installed', name) if 'is_dependency' in args else False
    if installed:
        print(f"{name} already installed")
        return
    if depends is not None and len(depends) != 0:
        print(f"Found {len(depends)} dependencies")
        for dependency in depends:
            if get_info('installed', dependency):
                print(f'Dependency {dependency} is already installed')
                continue
            install(dependency,'is_dependency')
    if src is None:
        print(f"Could not find source for {pkg}")
        return
    if not on_pacman:
        print(f"{name} not found on pacman")
        command = f'cd {os.path.abspath(os.getcwd())};git clone {src};cd {name};makepkg -si --noconfirm;cd ..;rm -r -d -f {name}' if 'aur' in link else f'curl -JLO {src};sudo pacman -U --noconfirm download;rm download'
    else:
        print(f"found {name} on pacman")
        command = f'sudo pacman -S --needed --noconfirm {name}'
    print("Running command")
    subprocess.run(command,shell=True)

while True:
    go = input("Would you like to install a package? (Y/N)\n").lower()
    if "y" in go:
        install(input("Type package name or archlinux.org package link.\n"))
    else:
        print("Process cancelled")
        exit()
