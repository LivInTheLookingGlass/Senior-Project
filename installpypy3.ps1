\Python27\python -c "import urllib; urllib.urlretrieve ('http://bitbucket.org/pypy/pypy/downloads/pypy3-2.4.0-win32.zip', r'pypy3-2.4.0-win32.zip')"
\Python27\python -c "import urllib; urllib.urlretrieve ('https://bootstrap.pypa.io/get-pip.py', r'get-pip.py')"
7z x pypy3-2.4.0-win32.zip > Out-Null
pypy3-2.4.0-win32\\pypy get-pip.py
