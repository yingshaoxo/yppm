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
from auto_everything.ml import ML
ml = ML()
terminal = Terminal()
terminal_user_interface = Terminal_User_Interface()
disk = Disk()
python = Python()
io_ = IO()
time_ = Time()

import generated_yrpc.question_and_answer_objects as question_and_answer_objects
import generated_yrpc.question_and_answer_pure_python_rpc as question_and_answer_pure_python_rpc
from generated_yrpc.question_and_answer_yingshaoxo_database_rpc import Yingshaoxo_Database_Excutor_question_and_answer

offline_question_and_answer_bot_dataset_path = "/home/yingshaoxo/CS/ML/18.fake_ai_asistant/input_txt_files"
if disk.exists(offline_question_and_answer_bot_dataset_path):
    text_generator = ml.Yingshaoxo_Text_Generator(
        input_txt_folder_path=offline_question_and_answer_bot_dataset_path,
        use_machine_learning=False
    )
else:
    text_generator = None

def decode_response(text: str, chat_context: str):
    #print("`"+text+"`")
    splits = text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n")
    if (len(splits) > 1):
        response = splits[1].strip()
    elif (len(splits) == 1):
        response = splits[0].strip()
    else:
        response = ""
    new_code = f"""
chat_context = '''{chat_context}'''

{response}
"""
    final_response = terminal.run_python_code(code=new_code)
    if final_response.strip() == "":
        final_response = response
    final_response = "\n".join([one for one in final_response.split("\n") if not one.strip().startswith("__**")])
    return final_response

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
#multiprocess_manager_socket_service = multiprocessing.Manager()
#global_shared_dict = multiprocess_manager_socket_service.dict()
database_excutor_for_remote_service = Yingshaoxo_Database_Excutor_question_and_answer(database_base_folder=the_database_path, use_sqlite=False, global_multiprocessing_shared_dict=None)


class Question_And_Answer_Service(question_and_answer_pure_python_rpc.Service_question_and_answer):
    def ask_yingshaoxo_ai(self, headers: dict[str, str], item: question_and_answer_objects.Ask_Yingshaoxo_Ai_Request) -> question_and_answer_objects.Ask_Yingshaoxo_Ai_Response:
        default_response = question_and_answer_objects.Ask_Yingshaoxo_Ai_Response()

        try:
            if item.input == None:
                default_response.error == "You should give me input"
                return default_response
            item.input = item.input.strip()

            if text_generator == None:
                default_response.answers = "No txt database path set."
                return default_response

            response = text_generator.search_and_get_following_text_in_a_exact_way(input_text=item.input, quick_mode=True)
            response = decode_response(text=response, chat_context=item.input)
            default_response.answers = response
        except Exception as e:
            print(f"Error: {e}")
            default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_json_web_token(self, headers: dict[str, str], item: question_and_answer_objects.Get_JSON_Web_Token_Request) -> question_and_answer_objects.Get_JSON_Web_Token_Response:
        default_response = question_and_answer_objects.Get_JSON_Web_Token_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_is_json_web_token_ok(self, headers: dict[str, str], item: question_and_answer_objects.Is_JSON_Web_Token_Ok_Request) -> question_and_answer_objects.Is_JSON_Web_Token_Ok_Response:
        default_response = question_and_answer_objects.Is_JSON_Web_Token_Ok_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_search(self, headers: dict[str, str], item: question_and_answer_objects.Search_Request) -> question_and_answer_objects.Search_Response:
        default_response = question_and_answer_objects.Search_Response()

        try:
            if item.search_input == None:
                default_response.error == "You should give me input"
                return default_response
            item.search_input = item.search_input.strip()

            def a_handler(raw_json_text: str) -> dict[str, Any] | None:
                search_text = item.search_input
                json_object = json.loads(raw_json_text)
                if search_text.lower() in str(json_object).lower():
                    return json_object
                return None
            search_list = database_excutor_for_remote_service.A_Post.raw_search(one_row_json_string_handler=a_handler, page_number=item.page_number, page_size=item.page_size)
            # need to do a comment search in the future for more accurate result

            if len(search_list) == 0:
                default_response.post_list = []
                return default_response
            else:
                default_response.post_list = search_list
                return default_response
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_a_post(self, headers: dict[str, str], item: question_and_answer_objects.Get_A_Post_Request) -> question_and_answer_objects.Get_A_Post_Response:
        default_response = question_and_answer_objects.Get_A_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_comment_list_by_id_list(self, headers: dict[str, str], item: question_and_answer_objects.Get_Comment_List_By_Id_List_Request) -> question_and_answer_objects.Get_Comment_List_By_Id_List_Response:
        default_response = question_and_answer_objects.Get_Comment_List_By_Id_List_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_add_post(self, headers: dict[str, str], item: question_and_answer_objects.Add_Post_Request) -> question_and_answer_objects.Add_Post_Response:
        default_response = question_and_answer_objects.Add_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_update_post(self, headers: dict[str, str], item: question_and_answer_objects.Update_Post_Request) -> question_and_answer_objects.Update_Post_Response:
        default_response = question_and_answer_objects.Update_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_delete_post(self, headers: dict[str, str], item: question_and_answer_objects.Delete_Post_Request) -> question_and_answer_objects.Delete_Post_Response:
        default_response = question_and_answer_objects.Delete_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_comment_post(self, headers: dict[str, str], item: question_and_answer_objects.Comment_Post_Request) -> question_and_answer_objects.Comment_Post_Response:
        default_response = question_and_answer_objects.Comment_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_modify_comment(self, headers: dict[str, str], item: question_and_answer_objects.Modify_Comment_Request) -> question_and_answer_objects.Modify_Comment_Response:
        default_response = question_and_answer_objects.Modify_Comment_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_delete_comment(self, headers: dict[str, str], item: question_and_answer_objects.Delete_Comment_Request) -> question_and_answer_objects.Delete_Comment_Response:
        default_response = question_and_answer_objects.Delete_Comment_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_like_or_dislike_a_post_or_comment(self, headers: dict[str, str], item: question_and_answer_objects.Like_Or_Dislike_Request) -> question_and_answer_objects.Like_Or_Dislike_Response:
        default_response = question_and_answer_objects.Like_Or_Dislike_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_download_backup_data(self, headers: dict[str, str], item: question_and_answer_objects.Download_Backup_Data_Request) -> question_and_answer_objects.Download_Backup_Data_Response:
        default_response = question_and_answer_objects.Download_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_upload_backup_data(self, headers: dict[str, str], item: question_and_answer_objects.Upload_Backup_Data_Request) -> question_and_answer_objects.Upload_Backup_Data_Response:
        default_response = question_and_answer_objects.Upload_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def admin_download_backup_data(self, headers: dict[str, str], item: question_and_answer_objects.Download_Backup_Data_Request) -> question_and_answer_objects.Download_Backup_Data_Response:
        default_response = question_and_answer_objects.Download_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def admin_upload_backup_data(self, headers: dict[str, str], item: question_and_answer_objects.Upload_Backup_Data_Request) -> question_and_answer_objects.Upload_Backup_Data_Response:
        default_response = question_and_answer_objects.Upload_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def generate_robots_txt_and_sitemap_xml(domain: str, output_folder: str):
    if not disk.exists(output_folder):
        print(f"Can't generate robots.txt and sitemap.xml to {output_folder}")
        return

    import urllib.parse
    robots = f"""
User-agent: *
Sitemap: {domain}/sitemaps.xml
""".strip()

    sitemap_part = """
"""
    sitemap_part_list = []
    search_list = database_excutor_for_remote_service.An_App.search(item_filter=app_store_objects.An_App())
    for one in search_list:
        last_modify_time = time_.get_datetime_object_from_timestamp(one.create_time_in_10_numbers_timestamp_format).strftime("%y-%m-%d")
        safe_name = urllib.parse.quote_plus(one.name)
        sitemap_part_list.append(f"""
   <url>
      <loc>{domain}/app_page?name={safe_name}</loc>
      <lastmod>{last_modify_time}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
   </url>
""")
    sitemap_part_list_text = "\n".join(sitemap_part_list)

    sitemap = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_part_list_text}
</urlset>
""".strip()

    robot_txt_path = disk.join_paths(output_folder, "robots.txt")
    io_.write(robot_txt_path, robots)

    sitemap_xml_path = disk.join_paths(output_folder, "sitemap.xml")
    io_.write(sitemap_xml_path, sitemap)


def run_service(port: str):
    database_excutor_for_remote_service.A_Post.database_of_yingshaoxo.refactor_database()
    database_excutor_for_remote_service.A_Comment.database_of_yingshaoxo.refactor_database()
    service_instance = Question_And_Answer_Service()

    html_folder_path = "../front_end/dist"
    #generate_robots_txt_and_sitemap_xml(domain="http://127.0.0.1:3333", output_folder=html_folder_path)
    question_and_answer_pure_python_rpc.run(service_instance, port=port, html_folder_path=html_folder_path)


run_service("54321")
