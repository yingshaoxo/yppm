#!/usr/bin/env /usr/bin/python3
import os
import re
import json

from auto_everything.base import Python, Terminal, IO   
from auto_everything.develop import YRPC
from auto_everything.disk import Disk

py = Python()
io_ = IO()
terminal = Terminal()
yrpc = YRPC()
disk = Disk()


class Tools():
    def __init__(self) -> None:
        self.project_root_folder = disk.get_directory_path(os.path.realpath(os.path.abspath(__file__))) 
        self.src_project_root_folder = disk.join_paths(self.project_root_folder, "src")
    
    def hi(self):
        print("Hi")


py.make_it_runnable()
py.fire2(Tools)
