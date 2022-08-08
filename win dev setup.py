import requests
import zipfile
import os

print("WARNING: This program is likely to require large scale use of windows admin,\nit is advised to run this as admin to avoid typing passwords dozens of times.")
print("Also, whilst this tool downloads all the dependancies for you, there is still\nsetup to do of each indivdual program as detailed in the instructions provided in this program.")
input("<press enter to begin installing>")

print("Downloading dev64 package...")  # Gets the latest dev64 files for mingw 11
url = "https://github.com/endless-sky/endless-sky.github.io/raw/9460071f6870d54dc19031f4a26f27a2fe7ef216/win64-dev.zip"

download = requests.get(url)
file = open("win64-dev.zip", "wb")
file.write(download.content)
file.close()
print("dev64 downloaded")

print("Downloading mingw version 11.3.0 (64 bit)...")  # Downloads mingw version 11
url = "https://github.com/brechtsanders/winlibs_mingw/releases/download/11.3.0-14.0.3-10.0.0-msvcrt-r3/winlibs-x86_64-posix-seh-gcc-11.3.0-mingw-w64msvcrt-10.0.0-r3.zip"

download = requests.get(url)
file = open("mingw-w64-11.3.0.zip", "wb")
file.write(download.content)
file.close()
print("Mingw version 11.3.0 downloaded")

while True:
    print("Would you like to use codeblocks (C), scons (S) or both (B) as your build environment?: ", end = "")
    which = input().upper()

    if which == "S" or which == "SCONS":
        scons = True
        code = False
        break
    elif which == "C" or which == "CODEBLOCKS":
        code = True
        scons = False
        break
    elif which == "B" or which == "BOTH":
        code = True
        scons = True
        break
    else:
        print("Please specify either \"codeblocks\" (\"C\"), \"scons\" (\"S\") or \"both\" (\"B\")!")

if code:  # Download code::blocks (non admin installer) without a built in compiler
    print("Downloading code::blocks version 20.03 (no compiler)")
    url = "https://nav.dl.sourceforge.net/project/codeblocks/Binaries/20.03/Windows/codeblocks-20.03-setup-nonadmin.exe"

    download = requests.get(url)
    file = open("codeblocks-setup.exe", "wb")
    file.write(download.content)
    file.close()

if scons:
    print("Do you have python version 3.8.0 or later installed? Y/N")
    inst_python = input().upper()[0]
    python_installed = False

    if inst_python == "Y":
        print("Skipping python interpriter download...")
        python_installed = True
    else:
        print("Downloading python installer...")
        url = "https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe"
        download = requests.get(url)
        file = open("python-3.10.6-setup.exe", "wb")
        file.write(download.content)
        file.close()

git = False
if os.system("git --version"):  # If git is not installed
    git = True
    print("downloading git version 2.37.1 (64 bit)")
    url = "https://github.com/git-for-windows/git/releases/download/v2.37.1.windows.1/Git-2.37.1-64-bit.exe"

    download = requests.get(url)
    file = open("git-install.exe", "wb")
    file.write(download.content)
    file.close()
    print("git version 2.37.1 downloaded")

print("All resources downloaded... unpacking resources")

print("Unpacking dev64...")
dev_zip = zipfile.ZipFile("win64-dev.zip")
dev_zip.extractall()
dev_zip.close()
print("dev64 unpacked!")

print("Unpacking mingw version 11.3.0...")
ming_zip = zipfile.ZipFile("mingw-w64-11.3.0.zip")
ming_zip.extractall(path = "mingw-w64-11.3.0")
ming_zip.close()
print("mingw version 11.3.0 unpacked!")
print"\nNote: you will need to add the compiler to your user path for it to be found.")
print("To add to your user path, open the start menu and search for \"environment\" and select \"Edit environment variables for your account\"")
print("Select \"Path\" in the top box and click \"edit\"")
print("Click \"new\" and enter the path to the bin folder of the compiler")
print("It should be: \"(this dir)/mingw-w64-11.3.0/mingw64/bin\"")
input("\n<press enter to continue>")

print("All resources unpacked!")
print("\nWhen installing packages, please ensure to add them to path where possible/applicible")
input("<press enter to launch installers>")
print("Launching installers...")

if git:
    print("Launching git installer")
    input("<press enter to continue>")
    result = os.system("git-install.exe")
    if result:
        print("git install aborted...")
        if input("Abort entire dev instilation? Y/N: ").upper()[0] == "Y":
            os.abort()

if code:
    print("Launching code::blocks installer")
    print("For code::blocks, the mingw compiler is found in the current directory, if code::blocks does not detect it, please add it manually if possible (also avalible through settings once installed)")
    input("<press enter to continue>")
    result = os.system("codeblocks-setup.exe")
    if result:
        print("code::blocks install aborted...")
        if input("Abort entire dev instilation? Y/N: ").upper()[0] == "Y":
            os.abort()

if scons:
    if not python_installed:
        print("Launching python installer")
        print("Please ensure to add python to path!")
        input("<press enter to continue>")
        result = os.system("python-3.10.6-setup.exe")
        if result:
            print("python install aborted...")
            if input("Abort entire dev instilation? Y/N: ").upper()[0] == "Y":
                os.abort()

print("All 3rd party installers have run, preparing to finish up instillation...")

print("Copying dev files to C:\dev64 (requires admin)")
input("<press enter to continue>")
try:
    if os.system("xcopy dev64 C:\dev64 /S /Q /Y /I"):
        print("ERROR: can't copy files!")
    if os.system("copy mingw-w64-11.3.0\mingw64\bin\libgcc_s_seh-1.dll C:\dev64\bin\libgcc_s_seh-1.dll /Y"):
        print("ERROR: can't copy files!")
    if os.system("copy mingw-w64-11.3.0\mingw64\bin\libstdc++-6.dll C:\dev64\bin\libstdc++-6.dll /Y"):
        print("ERROR: can't copy files!")
except:
    print("Error copying files!")
print("Dev files coppied!")

print("Cloning ES repo...")
os.system("git clone --quiet https://github.com/endless-sky/endless-sky.git")
os.system("xcopy C:\dev64\bin endless-sky /S /Q /Y /I")
print("Repo cloned and dev dlls coppied into repo!")
