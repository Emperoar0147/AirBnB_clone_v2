#!/usr/bin/python3
"""
Fabric script that generates .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create the archive name with the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_name))

        # Return the archive path if successfully created
        return archive_name
    except Exception as e:
        # Return None if there was any exception
        return None
