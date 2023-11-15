#!/usr/bin/env /usr/bin/python
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
        rm -fr dist/

        python3 -m pip install pyinstaller==5.13.0  --break-system-packages
        #python3 -m pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev"

        #python3 -m PyInstaller yppm/main.py --noconfirm --onefile --add-data "./yppm/resources:resources" --hidden-import auto_everything --name yppm
        python3 -m PyInstaller yppm/main.py --noconfirm --add-data "./yppm/resources:resources" --add-data "./yppm/auto_everything:auto_everything" --hidden-import auto_everything --name yppm

        rm -fr dist/yppm/resources/backend_and_frontend_project

        tar -czvf dist/yppm.tar.gz -C dist/yppm .
                     """)

    def install(self):
        self.build()
        print("\nPlease input your root password: ")
        terminal.run(f"""
        sudo -S echo 'Working on...'

        sudo rm -fr /usr/bin/yppm
        sudo rm -fr /usr/bin/yppm_folder

        sudo rm -fr /root/yppm.tar.gz
        sudo mv dist/yppm.tar.gz /root/yppm.tar.gz
        sudo mkdir -p /usr/bin/yppm_folder
        sudo tar -xzvf /root/yppm.tar.gz -C /usr/bin/yppm_folder

        sudo chmod a+rx /usr/bin/yppm_folder/yppm
        sudo ln -s /usr/bin/yppm_folder/yppm /usr/bin/yppm
        sudo chmod a+rx /usr/bin/yppm

        echo 'Done'
                     """, wait=True)

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
