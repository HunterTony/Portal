import requests
import subprocess
import os


print("    Downloading installer...")
with open("C:\\Cilix\\Chrome-Installer.msi", "wb") as fp:
    fp.write(requests.get("https://dl.google.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise.msi").content)

print("    Executing installer...")
subprocess.call(["msiexec.exe", "/i", "C:\\Cilix\\Chrome-Installer.msi")

print("    Cleaning up...")
os.remove("C:\\Cilix\\Chrome-Installer.msi")
