#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python3
#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python
import os
import re
import json

from auto_everything.base import Python, Terminal, IO   
from auto_everything.develop import YRPC
from auto_everything.disk import Disk
from auto_everything.database import Database_Of_Yingshaoxo
from auto_everything.cryptography import Encryption_And_Decryption

py = Python()
io_ = IO()
terminal = Terminal()
yrpc = YRPC()
disk = Disk()


class Tools():
    def __init__(self) -> None:
        self.project_root_folder = disk.get_directory_path(os.path.realpath(os.path.abspath(__file__))) 
        self.src_project_root_folder = disk.join_paths(self.project_root_folder, "src")
    
    def build(self):
        terminal.run(f"""
        rm -fr dist/
        python3 -m pip install --upgrade build
        python3 -m build
                     """)

    def publish(self):
        terminal.run(f"""
        python3 -m pip install --upgrade twine
        python3 -m twine upload dist/* 
                     """)


py.make_it_runnable()
py.fire2(Tools)
