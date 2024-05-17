#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, local, run
import os

# Define the IP addresses of the servers
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your actual IPs

def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number <= 1:
        number = 1

    # Local clean up
    archives = sorted(os.listdir("versions"))
    archives_to_delete = archives[:-number]
    for archive in archives_to_delete:
        local("rm -f versions/{}".format(archive))

    # Remote clean up
    releases = run("ls -tr /data/web_static/releases").split()
    releases_to_delete = [release for release in releases if "web_static_" in release]
    releases_to_delete = sorted(releases_to_delete)[:-number]

    for release in releases_to_delete:
        run("rm -rf /data/web_static/releases/{}".format(release))
