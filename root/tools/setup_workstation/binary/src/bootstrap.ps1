$EXIT_SUCCESS = 0
$EXIT_FAILURE = -1
$CURRENT_VERSION = 5


function download_file($remote_location, $local_location) {
    $web_client = new-object System.Net.WebClient

    for($attempt = 5; $attempt -ge 0; $attempt -= 1) {
        $web_client.DownloadFile($remote_location, $local_location)

        if((test-path $local_location) -eq $False) {
            write-host "    Download from $remote_location failed - Retrying"
        } else {
            break
        }
    }

    if((test-path $local_location) -eq $False) {
        write-host "    Download from $remote_location failed"
        exit $EXIT_FAILURE
    }
}


function install_visual_studio() {
    write-host "  Visual Studio"

    write-host "    Downloading"
    download_file "http://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe" "C:\Cilix\Python\vcredist_x86.exe"

    write-host "    Installing"
    start-process "C:\Cilix\Python\vcredist_x86.exe" -Wait -ArgumentList "/q /norestart"

    remove-item "C:\Cilix\Python\vcredist_x86.exe"
}


function install_python() {
    write-host "  Python"

    write-host "    Downloading"
    download_file "https://www.python.org/ftp/python/3.4.2/python-3.4.2.msi" "C:\Cilix\Python\python-setup.msi"

    write-host "    Installing"
    start-process msiexec -Wait -ArgumentList "/i C:\Cilix\Python\python-setup.msi /qn TARGETDIR=C:\Cilix\Python ALLUSERS=1 ADDLOCAL=DefaultFeature,TclTk"

    remove-item "C:\Cilix\Python\python-setup.msi"

    if($env:Path.contains(";C:\Cilix\Python") -eq $False) {
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Cilix\Python", [System.EnvironmentVariableTarget]::Machine)

        restart-service "Advanced Monitoring Agent" 2>&1 | out-null
    }
}


function install_requests() {
    write-host "  Requests"

    write-host "    Downloading"
    download_file "https://github.com/kennethreitz/requests/archive/v2.8.1.zip" "C:\Cilix\Python\requests.zip"

    write-host "    Extracting"
    $shell       = new-object -com Shell.Application
    $zip_file    = $shell.NameSpace("C:\Cilix\Python\requests.zip")
    $destination = $shell.NameSpace("C:\Cilix\Python")

    foreach($item in $zip_file.items()) {
        $destination.copyhere($item)
    }

    sleep 2

    remove-item "C:\Cilix\Python\requests.zip"

    write-host "    Installing"
    $location = get-location
    set-location -Path "C:\Cilix\Python\requests-2.8.1"
    start-process "C:\Cilix\Python\python.exe" -Wait -ArgumentList "C:\Cilix\Python\requests-2.8.1\setup.py install"
    set-location $location

    sleep 2

    remove-item -recurse -force "C:\Cilix\Python\requests-2.8.1"
}


function remove_start_menu_folders() {
    write-host "  Removing start menu folders"

    remove-item "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.4\*"
    remove-item "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.4\"
}


function update_version_file() {
    $CURRENT_VERSION | out-file C:\Cilix\Python\version
}


function run_install() {
    install_visual_studio
    install_python
    install_requests
    remove_start_menu_folders
    update_version_file
}


function main() {
    if((test-path "C:\Cilix\") -eq $False) {
        new-item -itemtype directory -path "C:\Cilix" 2>&1 | out-null
    }

    if((test-path "C:\Cilix\Python\") -eq $True) {
        if((test-path "C:\Cilix\Python\version") -eq $True) {
            $version = get-content "C:\Cilix\Python\version"
        } else {
            $version = -1
        }

        if($version -eq $CURRENT_VERSION) {
            write-host "  At latest version $version"
            exit $EXIT_SUCCESS
        }

        write-host "  Updating from $version to $CURRENT_VERSION"
    } else {
        new-item -itemtype directory -path "C:\Cilix\Python" 2>&1 | out-null
    }

    run_install
}

main
