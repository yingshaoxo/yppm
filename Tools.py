#!/usr/bin/env /usr/bin/python3
import os
import re
import json
from time import sleep

from auto_everything.base import Python, Terminal, IO
from auto_everything.develop import YRPC
from auto_everything.disk import Disk
from auto_everything.develop import Develop
from auto_everything.time import Time

py = Python()
io_ = IO()
terminal = Terminal()
yrpc = YRPC()
disk = Disk()
develop = Develop()
time_ = Time()


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

        terminal.run(f"""
        #python3 -m venv {virtual_env_folder}
        #source {activate_file}

        python3 -m pip install pyinstaller==5.13.0
        #python3 -m pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev"

        python3 -m PyInstaller yppm/main.py --noconfirm --onefile --add-data "./yppm/resources:resources" --hidden-import auto_everything --name yppm 
                     """)
    
    def install(self):
        self.build()
        disk.copy_a_file("./dist/yppm", "/usr/bin/yppm")
        terminal.run(f"""
        chmod a+rx /usr/bin/yppm 
                     """)
    
    def dev(self):
        print("\n\n\nIn watching, when you change code, I'll do the compile and installation for you.")

        watch_folder = disk.join_paths(self.project_root_folder, "yppm")
        while True:
            changed = develop.whether_a_folder_has_changed(watch_folder)
            if changed == True:
                sleep(60)
                develop.whether_a_folder_has_changed(watch_folder)

                try:
                    self.install()
                except Exception as e:
                    print(e)

                print("\n\n\nIn watching, when you change code, I'll do the compile and installation for you.")

            sleep(5)
    

py.make_it_runnable()
py.fire2(Tools)