import sys, os
import requests

os.makedirs("packages", exist_ok=True)

if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} install <RequirementsFile/PackageName> [Server]")
    print(f"       {sys.argv[0]} update <RequirementsFile/PackageName> [Server]")
    sys.exit(0)

def download(packageName: str, update: bool):
    print(f"{packageName}: Downloading")
    if not update:
        if os.path.isfile(f"packages/{packageName}.junlib"):
            print(f"{packageName}: Downloaded / Do you need to upgrade?")
            return
    response = ""
    retry = 0
    if len(sys.argv) > 3:
        url = sys.argv[3]
    else:
        url = "https://pm.imjcj.eu.org/libs"
    try:
        response = requests.get(f"{url}/{packageName[0]}/{packageName}.json")
    except:
        print(f"{packageName}: Network Error")
        return
    if response.status_code == 404:
        print(f"{packageName}: Not Found")
        return
    elif response.status_code < 200 or response.status_code > 299:
        print(f"{packageName}: Server Error {response.status_code}")
        return
    url = response.json()["url"]
    try:
        response = requests.get(url)
    except:
        print(f"{packageName}: Network Error")
        return
    if response.status_code == 404:
        print(f"{packageName}: Not Found")
        return
    elif response.status_code < 200 or response.status_code > 299:
        print(f"{packageName}: Server Error")
        return
    with open(f"packages/{packageName}.junlib", "wb") as f:
        f.write(response.content)
    print(f"{packageName}: Downloaded")

filePath = sys.argv[2]
install = sys.argv[1] == "install"
update = sys.argv[1] == "update"
if not (install or update):
    print(f"Usage: {sys.argv[0]} install <RequirementsFile/PackageName> [Server]")
    print(f"       {sys.argv[0]} update <RequirementsFile/PackageName> [Server]")
    sys.exit(0)
if os.path.isfile(filePath):
    with open(filePath, 'r') as f:
        for line in f:
            if update:
                download(line, 1)
            else:
                download(line, 0)
else:
    if update:
        download(sys.argv[2], 1)
    else:
        download(sys.argv[2], 0)