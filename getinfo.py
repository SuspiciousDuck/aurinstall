import requests
import json
import subprocess

def get_info(info,package_name):
    if 'link' in info:
        response = requests.get(f"https://www.archlinux.org/packages/search/json?name={package_name}")
        data = json.loads(response.text)
        if data['results']:
            url = f"https://www.archlinux.org/packages/{data['results'][0]['repo']}/{data['results'][0]['arch']}/{data['results'][0]['pkgname']}/"
            return url
        else:
            response = requests.get(f"https://aur.archlinux.org/rpc/?v=5&type=info&arg={package_name}")
            data = json.loads(response.text)
            if data['results']:
                url = f"https://aur.archlinux.org/packages/{data['results'][0]['Name']}"
                return url
            else:
                print(f"{package_name} not found in both normal repository and AUR")
                return None
    elif 'name' in info:
        url = f'https://archlinux.org/packages/search/json/?name={package_name}'
        response = requests.get(url)
        data = response.json()

        if data['results']:
            package_name = data['results'][0]['pkgname']
            return package_name
    elif 'depends' in info:
        response = requests.get(f"https://aur.archlinux.org/rpc/v5/info/{package_name}")
        data = json.loads(response.text)
        depends_list = None
        if data['results']:
            depends_list = data['results'][0]['Depends']
            return depends_list
    elif 'pacman' in info:
        result = subprocess.Popen(["pacman", "-Qq", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        sdata = result.communicate()[0]
        code = result.returncode
        return True if code == 0 else False
    elif 'installed' in info:
        result = subprocess.Popen(["pacman", "-Qi", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        sdata = result.communicate()[0]
        code = result.returncode
        return True if code == 0 else False