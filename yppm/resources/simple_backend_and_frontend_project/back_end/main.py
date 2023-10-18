from typing import Any
import sys
import multiprocessing
from time import sleep
from datetime import datetime
import multiprocessing
import os
import re
import json

from auto_everything.terminal import Terminal, Terminal_User_Interface
from auto_everything.python import Python
from auto_everything.disk import Disk, Store
from auto_everything.io import IO
from auto_everything.time import Time
terminal = Terminal()
terminal_user_interface = Terminal_User_Interface()
disk = Disk()
python = Python()
io_ = IO()
time_ = Time()

import generated_yrpc.app_store_objects as app_store_objects
import generated_yrpc.app_store_pure_python_rpc as app_store_pure_python_rpc
from generated_yrpc.app_store_yingshaoxo_database_rpc import Yingshaoxo_Database_Excutor_app_store

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    #print('running in a PyInstaller bundle')
    def resource_path(relative_path: str) -> str:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path) #type: ignore
        return os.path.join(os.path.abspath("."), relative_path)
    resource_basic_folder_path = resource_path(".")
    the_database_path = disk.join_paths(disk.get_parent_directory_path(disk.get_parent_directory_path(resource_basic_folder_path)), './database_data')
else:
    #print('running in a normal Python process')
    resource_basic_folder_path = disk.get_directory_path(__file__)
    the_database_path = disk.join_paths(resource_basic_folder_path, './database_data')

print(f"resource_basic_folder_path: {resource_basic_folder_path}")
print(f"database_path: {the_database_path}")
print()
disk.create_a_folder(the_database_path)
database_excutor_for_remote_service = Yingshaoxo_Database_Excutor_app_store(database_base_folder=the_database_path)


class App_Store_Service(app_store_pure_python_rpc.Service_app_store):
    def add_app(self, headers: dict[str, str], item: app_store_objects.Add_App_Request) -> app_store_objects.Add_App_Response:
        default_response = app_store_objects.Add_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def search_app(self, headers: dict[str, str], item: app_store_objects.Search_App_Request) -> app_store_objects.Search_App_Response:
        default_response = app_store_objects.Search_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def get_app_detail(self, headers: dict[str, str], item: app_store_objects.Get_App_Detail_Request) -> app_store_objects.Get_App_Detail_Response:
        default_response = app_store_objects.Get_App_Detail_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def run_service(port: str):
    service_instance = App_Store_Service()
    app_store_pure_python_rpc.run(service_instance, port=port)


run_service("3333")
