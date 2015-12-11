(New-Object Net.WebClient).DownloadFile('https://bitbucket.org/pypy/pypy/downloads/pypy3-2.4.0-win32.zip', '$env:appveyor_build_folder\\pypy3-2.4.0-win32.zip')
(New-Object Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', '$env:appveyor_build_folder\\get-pip.py')
7z x pypy-4.0.1-win32.zip
$env:path = '$env:appveyor_build_folder\\pypy3-2.4.0-win32;$env:path'
pypy get-pip.py
