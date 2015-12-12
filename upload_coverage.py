import platform, sys

if platform.python_implementation() != "PyPy" or sys.version_info[0] != 3:
  import subprocess
  subprocess.call("\\Python" + str(sys.version_info[0]) + str(sys.version_info[1]) + "\\Scripts\\coverage xml")
  a = "\\Python" + str(sys.version_info[0]) + str(sys.version_info[1])
  if platform.architecture()[0] != '32bit':
    a += "-X64"
  subprocess.call(a + "\\Scripts\\codecov --token=0482d032-e24c-461b-a116-f0e3dbc88734")
