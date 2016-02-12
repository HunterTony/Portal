import requests
import subprocess
import os


def main():
    print("    Downloading installer...")
    with open("C:\\Cilix\\PCSetup\\Chrome-Installer.msi", "wb") as fp:
        fp.write(requests.get("https://dl.google.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise.msi").content)

    print("    Executing installer...")
    subprocess.call(["msiexec.exe", "/i", "C:\\Cilix\\PCSetup\\Chrome-Installer.msi")

    print("    Cleaning up...")
    os.remove("C:\\Cilix\\PCSetup\\Chrome-Installer.msi")


if(__name__ == "__main__"):
    main()
