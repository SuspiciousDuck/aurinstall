import requests
import json
import subprocess
import os
import argparse

def run_shell(args):
    result = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    sdata = result.communicate()[0]
    code = result.returncode
    return True if code == 0 else False

def get(url):
    return json.loads(requests.get(url).text)

class install():
    def __init__(self):
        self.api = ['https://www.archlinux.org/packages/search/json?name=','https://www.archlinux.org/packages/','https://aur.archlinux.org/rpc/?v=5&type=info&arg=','https://aur.archlinux.org/packages/','https://archlinux.org/packages/search/json/?name=','https://aur.archlinux.org/rpc/v5/info/']

    def get_name(self,link):
        return os.path.basename(os.path.dirname(link.rstrip("/")))

    def is_link(self,pkg):
        return True if 'archlinux.org' in pkg else False

    def get_link(self,name,repo):
        if repo == 2:
            data = get(self.api[0]+name)['results'][0]
            return f"{self.api[1]}{data['repo']}/{data['arch']}/{data['pkgname']}/"
        else:
            data = get(self.api[2]+name)['results'][0]['Name']
            return self.api[3]+data

    def get_depends(self,name):
        data = get(self.api[5]+name)['results'][0]
        deps,conflicts = None,None
        try:
            deps = data['Depends']
        except:
            pass
        try:
            conflicts = data['Conflicts']
        except:
            pass
        return deps,conflicts
    
    def is_installed(self,name):
        return run_shell(["pacman", "-Qi", name])

    def package_exists(self,pkgname):
        if run_shell(["pacman", "-Ss", f"^{pkgname}$"]) == True:
            return 1
        if get(self.api[0]+pkgname)['results'] != []:
            return 2
        if get(self.api[2]+pkgname)['results'] != []:
            return 3
        return None

    def remove(self, pkg):
        islink = self.is_link(pkg)
        pkg_name = pkg if not islink else self.get_name(pkg)
        if self.is_installed(pkg_name) == False:
            print(f'{pkg_name} is not installed.')
            return
        print(f'Removing {pkg_name}')
        output = subprocess.check_output(["pacman", "-Qi", pkg_name])
        if "Depends On" in output.decode():
            response = input(f"{pkg_name} is required by another package. Delete anyway? (Y/N)\n").lower()
            if 'y' in response:
                subprocess.run(f'sudo pacman -Rdd --noconfirm {pkg_name}',shell=True)
            else:
                return
        else:
            subprocess.run(f'sudo pacman -R --noconfirm {pkg_name}',shell=True)
    
    def install(self, pkg):
        islink = self.is_link(pkg)
        pkg_name = pkg if not islink else self.get_name(pkg)
        if self.is_installed(pkg_name):
            print(f'{pkg_name} is already installed.')
            return
        results = self.package_exists(pkg_name)
        if not results:
            print(f'{pkg_name} not found.')
            return
        if results == 1:
            print(f'Found {pkg_name} on pacman.')
            subprocess.run(f'sudo pacman -S --needed --noconfirm {pkg_name}',shell=True)
            return
        depends,conflicts = self.get_depends(pkg_name)
        if depends != None:
            print(f'Found {len(depends)} dependencies')
            for depend in depends:
                if '=' in depend:
                    self.install(depend.split('=')[0])
                else:
                    self.install(depend)
        if conflicts != None:
            for conflict in conflicts:
                if self.is_installed(conflict):
                    if input(f'{conflict} conflicts with package! Remove? (Y/N)\n').lower().startswith('y'):
                        subprocess.run(f'sudo pacman -Rdd {conflict}',shell=True)
                    else:
                        print('Conflicting package not removed. Cancelling build.')
                        return
        link = pkg if islink else self.get_link(pkg_name,results)
        src = (link+'download' if link.endswith('/') else link+'/download') if results == 2 else ('https://aur.archlinux.org/'+pkg_name+'.git')
        if results == 2:
            print('Found on normal repo.')
            subprocess.run(f'curl -JLO {src};sudo pacman -U --noconfirm download;rm download',shell=True)
        else:
            print('Found on AUR repo.')
            subprocess.run(f'cd {os.path.abspath(os.getcwd())};git clone {src};cd {pkg_name};makepkg -m --noconfirm;cd ..;rm -r -d -f {pkg_name}',shell=True)
            
    def main(self,text,which):
        args = text.split(' ')
        for arg in args:
            if which == 'install':
                self.install(arg)
            else:
                self.remove(arg)

parser = argparse.ArgumentParser(description='My Package Manager')
parser.add_argument('--install', nargs='+', help='Install package(s)')
parser.set_defaults(func=install().main)
parser.add_argument('--uninstall', nargs='+', help='Uninstall package(s)')
parser.set_defaults(func=install().main)
args = parser.parse_args()

if args.install:
    args.func(' '.join(args.install),'install')
if args.uninstall:
    args.func(' '.join(args.uninstall),'uninstall')