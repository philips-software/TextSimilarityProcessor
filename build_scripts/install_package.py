""" file used for installing the package"""
import os
import sys
import subprocess


def get_version_sub_string():
    """ function returns the current package version substring"""
    cwd = os.getcwd()
    proj_root = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    os.chdir(proj_root)
    proc = subprocess.Popen("python3 setup.py --version", stdout=subprocess.PIPE)
    os.chdir(cwd)
    return proc.communicate()[0].rstrip().decode("utf-8")


def find_installer():
    """ Function finds the installer full name based on the substring"""
    proj_dist = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))), "dist")
    installer_list = os.listdir(proj_dist)
    return [item for item in installer_list if "%s" % get_version_sub_string() in item]


def install(package):
    """ Function used for installing the package using the pip installer"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def cmd_package():
    """ Function validates only one installer is present then issues install command"""
    whl_list = [whl for whl in find_installer() if "whl" in whl]
    if len(whl_list) != 1:
        print("unable to find the installer")
        sys.exit(1)
    whl_matching = ''.join(whl_list)
    proj_dist = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))), "dist", whl_matching)
    install(proj_dist)


if __name__ == '__main__':
    cmd_package()
