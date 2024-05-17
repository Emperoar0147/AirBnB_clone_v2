#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import env, put, run
import os.path

# Define the IP addresses of the servers
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your actual IPs

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        path_tmp = "/tmp/{}".format(file_name)

        put(archive_path, path_tmp)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        path_release = "/data/web_static/releases/{}/".format(no_ext)
        run("mkdir -p {}".format(path_release))
        run("tar -xzf {} -C {}".format(path_tmp, path_release))

        # Delete the archive from the web server
        run("rm {}".format(path_tmp))

        # Move contents out of the web_static folder
        run("mv {}/web_static/* {}".format(path_release, path_release))
        run("rm -rf {}/web_static".format(path_release))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("ln -s {} /data/web_static/current".format(path_release))

        return True
    except Exception:
        return False
