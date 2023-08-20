#!/usr/bin/env /usr/bin/python3
import os
import re
import json
import sys

from auto_everything.base import Python, Terminal, IO   
from auto_everything.disk import Disk

py = Python()
io_ = IO()
terminal = Terminal()
disk = Disk()


class Tools():
    def __init__(self) -> None:
        self.project_root_folder = disk.get_directory_path(os.path.realpath(os.path.abspath(__file__))) 
        self.src_project_root_folder = disk.join_paths(self.project_root_folder, "src")

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            #print('running in a PyInstaller bundle')
            def resource_path(relative_path: str) -> str:
                if hasattr(sys, '_MEIPASS'):
                    return os.path.join(sys._MEIPASS, relative_path) #type: ignore
                return os.path.join(os.path.abspath("."), relative_path)
            resource_basic_folder_path = resource_path(".")
        else:
            #print('running in a normal Python process')
            resource_basic_folder_path = disk.get_directory_path(__file__)
        self.resource_basic_folder_path = disk.join_paths(resource_basic_folder_path, 'resources').replace("//.//", "//")
    
    def hi(self):
        print(self.resource_basic_folder_path)
        print(disk.get_files(self.resource_basic_folder_path))


try:
    py.fire2(Tools)
except Exception as e:
    pass