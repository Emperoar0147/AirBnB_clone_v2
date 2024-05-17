#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Define the IP addresses of the servers
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your actual IPs

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None

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

def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
