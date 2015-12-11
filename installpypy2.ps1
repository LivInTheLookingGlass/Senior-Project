\Python27\python -c "import urllib; urllib.urlretrieve ('http://bitbucket.org/pypy/pypy/downloads/pypy-4.0.1-win32.zip', r'pypy-4.0.1-win32.zip')"
\Python27\python -c "import urllib; urllib.urlretrieve ('https://bootstrap.pypa.io/get-pip.py', r'get-pip.py')"
7z x pypy-4.0.1-win32.zip
$env:path = '$env:appveyor_build_folder\\pypy-4.0.1-win32;$env:path'
pypy get-pip.py
