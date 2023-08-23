#!/usr/bin/env /usr/bin/python3
from typing import Any

import os
import sys
import platform
import re
import json
from subprocess import call

from auto_everything.io import IO   
from auto_everything.disk import Disk
from auto_everything.python import Python
from auto_everything.terminal import Terminal, Terminal_User_Interface
from auto_everything.string import String


py = Python()
io_ = IO()
terminal = Terminal()
disk = Disk()
python_ = Python()
terminal_user_interface = Terminal_User_Interface()
string_tool = String()


class Tools():
    def __init__(self) -> None:
        # get static resource folder
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
        self.resource_basic_folder_path = disk.join_paths(resource_basic_folder_path, 'resources').replace("/./", "/")

        # get python executable path
        self.python_executable_path = "python"
        if " 3." in terminal.run_command("python --version"):
            self.python_executable_path = "python"
        elif " 3." in terminal.run_command("python3 --version"):
            self.python_executable_path = "python3"

        # get git user email and username
        self.git_user_email = terminal.run_command("git config user.email").strip().split('\n')[0]
        self.git_user_name = terminal.run_command("git config user.name").strip().split('\n')[0].lower()
        if self.git_user_name == "":
            self.git_user_name = string_tool.remove_all_special_characters_from_a_string(os.getlogin(), white_list_characters='_').strip().lower()
            if self.git_user_name == "":
                self.git_user_name = platform.system().lower().strip()

        # get project base folder
        self.project_root_folder = os.getcwd()

        # get virtual env folder
        self.virtual_env_folder = disk.join_paths(self.project_root_folder, ".venv")
        self.env_activate_file_path = disk.join_paths(self.virtual_env_folder, "bin/activate")

        # get package json file
        self.package_json_file_path = disk.join_paths(self.project_root_folder, "package.json")
    
    def _add_to_gitignore(self, name: str):
        gitignore_path = disk.join_paths(self.project_root_folder, ".gitignore")
        if disk.exists(gitignore_path):
            text = io_.read(gitignore_path)
            if name not in text:
                text = f"{name}\n" + text 
                io_.write(gitignore_path, text)
        else:
            text = name
            io_.write(gitignore_path, text)

    def _create_virtual_env(self):
        if disk.exists(self.virtual_env_folder):
            return
        
        print(f"Creating virtual envirnoment by using '{self.python_executable_path}'...")

        terminal.run(f"""
        {self.python_executable_path} -m venv {self.virtual_env_folder}
                     """)

        # change permission of activate file
        terminal.run(f"""chmod 777 {self.env_activate_file_path}""")
        
        # ignore .venv folder
        self._add_to_gitignore(".venv/")
    
    def _get_package_json_object(self) -> Any:
        try:
            text = io_.read(self.package_json_file_path)
            json_object = json.loads(text)
            return json_object
        except Exception as e:
            print(e)
            return None
    
    def create_a_new_project(self):
        pass

    def init(self):
        # create package.json file in current folder if there does not have one
        if disk.exists(self.package_json_file_path):
            print("There already has a 'package.json' file.")
        else:
            json_content = """
            {
                "name": "",
                "version": "",
                "author": "",
                "main": "main.py",
                "scripts": {},
                "dependencies": [
                    "git+https://github.com/yingshaoxo/auto_everything.git@dev"
                ]
            }
            """
            package_object = json.loads(json_content)
            print("\n")

            # handle project name
            default_project_name = disk.get_directory_name(self.project_root_folder)
            print(default_project_name)
            def assign_name(text: str):
                package_object["name"] = text
            terminal_user_interface.input_box(
                f"Please give me a project name (default '{default_project_name}'): ", 
                default_value=default_project_name,
                handle_function=assign_name
            )

            # handle project version
            default_project_version = "0.0.0"
            def assign_version(text: str):
                package_object["version"] = text
            terminal_user_interface.input_box(
                f"Please give me a project version (default '{default_project_version}'): ", 
                default_value=default_project_version,
                handle_function=assign_version
            )

            # handle author name
            default_author = self.git_user_email
            if "@" not in default_author:
                default_author = "" 
            def assign_author(text: str):
                package_object["author"] = text
            terminal_user_interface.input_box(
                f"Please give me your name (default '{default_author}'): ", 
                default_value=default_author,
                handle_function=assign_author
            )

            io_.write(self.package_json_file_path, json.dumps(package_object, indent=4))
            self._create_virtual_env()

    def run(self, script_name: str = ""):
        if not disk.exists(self.package_json_file_path):
            print("You have to run `yppm init` first.")
            return
        self._create_virtual_env()

        package_object = self._get_package_json_object()

        scripts = package_object.get("scripts")
        if scripts == None:
            print('package.json should have a key called {"scripts": {}}')
            return

        entry_point_python_script = package_object.get("main")
        if entry_point_python_script == None:
            print('package.json should have a key called {"main": "main.py"}')
            return

        script_name = script_name.strip()
        if script_name == "":
            terminal.run(f"""
            {self.env_activate_file_path}

            {self.python_executable_path} {entry_point_python_script}
                         """)
        else:
            if script_name in scripts.keys():
                terminal.run(f"""
                {self.env_activate_file_path}

                {scripts[script_name]}
                            """)
            else:
                print(f"Sorry, script '{script_name}' not exists in the package.json")

    def _install_package(self, package_name: str, upgrade: bool = False):
        pip_path = disk.join_paths(self.virtual_env_folder, "bin", "pip3")
        if not disk.exists(pip_path):
            pip_path = disk.join_paths(self.virtual_env_folder, "bin", "pip")

        yes_exists = terminal.run_command("yes --version")
        if ("copyright" in yes_exists.strip().lower()):
            yes_exists = True
        else:
            yes_exists = False

        if upgrade == False:
            terminal.run(f"""
            {self.env_activate_file_path}

            yes | {pip_path} install {package_name}
                        """)
        else:
            terminal.run(f"""
            {self.env_activate_file_path}

            yes | {pip_path} install {package_name} --upgrade
                        """)

    def _uninstall_package(self, package_name: str):
        pip_path = disk.join_paths(self.virtual_env_folder, "bin", "pip3")
        if not disk.exists(pip_path):
            pip_path = disk.join_paths(self.virtual_env_folder, "bin", "pip")

        yes_exists = terminal.run_command("yes --version")
        if ("copyright" in yes_exists.strip().lower()):
            yes_exists = True
        else:
            yes_exists = False

        terminal.run(f"""
        {self.env_activate_file_path}

        yes | {pip_path} uninstall {package_name}
                        """)

    def install(self, package_name: str = ""):
        if not disk.exists(self.package_json_file_path):
            print("You have to run `yppm init` first.")
            return
        self._create_virtual_env()

        package_object = self._get_package_json_object()

        dependencies = package_object.get("dependencies")
        if dependencies == None:
            print('package.json should have a key called {"dependencies": []}')
            return

        package_name = package_name.strip()
        if package_name == "":
            # install all package
            for package_name in dependencies:
                self._install_package(package_name=package_name)
        else:
            # install one package
            if package_name not in dependencies:
                # install once
                self._install_package(package_name=package_name)
            else:
                # install again
                self._install_package(package_name=package_name, upgrade=True)
            
            if package_name not in dependencies:
                package_object["dependencies"].append(package_name)
                io_.write(self.package_json_file_path, json.dumps(package_object, indent=4))

    def uninstall(self, package_name: str = ""):
        if not disk.exists(self.package_json_file_path):
            print("You have to run `yppm init` first.")
            return
        self._create_virtual_env()

        package_object = self._get_package_json_object()

        dependencies = package_object.get("dependencies")
        if dependencies == None:
            print('package.json should have a key called {"dependencies": []}')
            return

        package_name = package_name.strip()
        if package_name == "":
            pass
        else:
            if package_name not in dependencies:
                pass
            else:
                self._uninstall_package(package_name=package_name)
            
            if package_name in dependencies:
                del package_object["dependencies"][package_name]
                io_.write(self.package_json_file_path, json.dumps(package_object, indent=4))

    def build(self, pyinstaller_arguments: str = "", use_virtual_env: bool = False):
        package_object = self._get_package_json_object()

        name = package_object.get("name")
        if name == None:
            print('package.json should have a key called {"name": "your_app_name"}')
            return

        entry_point_python_script = package_object.get("main")
        if entry_point_python_script == None:
            print('package.json should have a key called {"main": "main.py"}')
            return

        self._add_to_gitignore(".build/")
        self._add_to_gitignore(".dist/")

        terminal.run(f"""
        {'#' if use_virtual_env == False else ''}{self.env_activate_file_path}

        export PIP_BREAK_SYSTEM_PACKAGES=1
        {self.python_executable_path} -m pip install pyinstaller

        {self.python_executable_path} -m PyInstaller {entry_point_python_script} --noconfirm --onefile {pyinstaller_arguments} --hidden-import auto_everything --name {name}
                     """)

    def clean(self):
        disk.delete_a_folder(self.virtual_env_folder)

    def env(self):
        print(f""" Please run:\n\n{self.env_activate_file_path} """.strip())

    def about(self):
        terminal.run("clear")
        print("""
YPPM: Yingshaoxo Python Package Manager. 
              
(yingshaoxo is my name)
        """.strip())


try:
    py.fire2(Tools)
except Exception as e:
    pass