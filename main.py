#!/usr/bin/env python3
import sys, os
import requests

os.makedirs("packages", exist_ok=True)

if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} install <RequirementsFile/PackageId> [Server]")
    print(f"       {sys.argv[0]} update <RequirementsFile/PackageId> [Server]")
    sys.exit(0)

def download(packageId: str, update: bool):
    print(f"{packageId}: Downloading")
    if not update:
        if os.path.isfile(f"packages/{packageId}.junlib"):
            print(f"{packageId}: Downloaded / Do you need to upgrade?")
            return
    response = ""
    # Get version and package id
    versionId = packageId.split(':')[1]
    packageId = packageId.split(':')[0]
    if versionId is None:
        versionId = "latest"

    # Set Download server link
    if len(sys.argv) > 3:
        url = sys.argv[3]
    else:
        url = "https://pm.imjcj.eu.org/libs"

    # Get package information from server
    try:
        response = requests.get(f"{url}/{packageId[0]}/{packageId}.json")
    except Exception as e:
        print(f"{packageId}: Network Error: {e}")
        return
    if response.status_code == 404:
        print(f"{packageId}: Not Found in {url}")
        return
    elif response.status_code < 200 or response.status_code > 299:
        print(f"{packageId}: Server Error: {response.status_code}")
        return
    
    # Get package and download link
    url = response.json()["versions"][versionId]
    packageName = response.json()["name"]
    ext = response.json()["type"]
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"{packageName}: Network Error: {e}")
        return
    if response.status_code == 404:
        print(f"{packageName}: Not Found in {url}")
        return
    elif response.status_code < 200 or response.status_code > 299:
        print(f"{packageName}: Server Error: {response.status_code}")
        return
    with open(f"packages/{packageId}.jun{ext}", "wb") as f:
        f.write(response.content)
    print(f"{packageId}: Downloaded")

filePath = sys.argv[2]
install = sys.argv[1] == "install"
update = sys.argv[1] == "update"
if not (install or update):
    print(f"Usage: {sys.argv[0]} install <RequirementsFile/PackageId> [Server]")
    print(f"       {sys.argv[0]} update <RequirementsFile/PackageId> [Server]")
    sys.exit(0)
if os.path.isfile(filePath):
    with open(filePath, 'r') as f:
        for line in f:
            if update:
                download(line, True)
            else:
                download(line, False)
else:
    if update:
        download(sys.argv[2], True)
    else:
        download(sys.argv[2], False)