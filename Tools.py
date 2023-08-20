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
    
    def build_package(self):
        terminal.run(f"""
        rm -fr dist/
        python3 -m pip install --upgrade build
        python3 -m build
                     """)

    def publish_package(self):
        terminal.run(f"""
        python3 -m pip install --upgrade twine
        python3 -m twine upload dist/* 
                     """)
    
    def build(self):
        virtual_env_folder = disk.join_paths(self.project_root_folder, ".venv")
        activate_file = disk.join_paths(virtual_env_folder, "bin/activate")
        # python_path = disk.join_paths(virtual_env_folder, "bin/python")

        terminal.run(f"""
        #python3 -m venv {virtual_env_folder}
        #source {activate_file}

        #python3 -m pip install pyinstaller==5.13.0
        #python3 -m pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev"

        python3 -m PyInstaller yppm/main.py --noconfirm --onefile --add-data "./yppm/resources:resources" --hidden-import auto_everything --name yppm 

        ./dist/yppm
                     """)
    

py.make_it_runnable()
py.fire2(Tools)
