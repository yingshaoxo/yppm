from .question_and_answer_objects import *


from typing import Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import os
from time import sleep


class Service_question_and_answer:
    def ask_yingshaoxo_ai(self, headers: dict[str, str], item: Ask_Yingshaoxo_Ai_Request) -> Ask_Yingshaoxo_Ai_Response:
        default_response = Ask_Yingshaoxo_Ai_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_json_web_token(self, headers: dict[str, str], item: Get_JSON_Web_Token_Request) -> Get_JSON_Web_Token_Response:
        default_response = Get_JSON_Web_Token_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_is_json_web_token_ok(self, headers: dict[str, str], item: Is_JSON_Web_Token_Ok_Request) -> Is_JSON_Web_Token_Ok_Response:
        default_response = Is_JSON_Web_Token_Ok_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_search(self, headers: dict[str, str], item: Search_Request) -> Search_Response:
        default_response = Search_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_a_post(self, headers: dict[str, str], item: Get_A_Post_Request) -> Get_A_Post_Response:
        default_response = Get_A_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def visitor_get_comment_list_by_id_list(self, headers: dict[str, str], item: Get_Comment_List_By_Id_List_Request) -> Get_Comment_List_By_Id_List_Response:
        default_response = Get_Comment_List_By_Id_List_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_add_post(self, headers: dict[str, str], item: Add_Post_Request) -> Add_Post_Response:
        default_response = Add_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_update_post(self, headers: dict[str, str], item: Update_Post_Request) -> Update_Post_Response:
        default_response = Update_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_delete_post(self, headers: dict[str, str], item: Delete_Post_Request) -> Delete_Post_Response:
        default_response = Delete_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_comment_post(self, headers: dict[str, str], item: Comment_Post_Request) -> Comment_Post_Response:
        default_response = Comment_Post_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_modify_comment(self, headers: dict[str, str], item: Modify_Comment_Request) -> Modify_Comment_Response:
        default_response = Modify_Comment_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_delete_comment(self, headers: dict[str, str], item: Delete_Comment_Request) -> Delete_Comment_Response:
        default_response = Delete_Comment_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_like_or_dislike_a_post_or_comment(self, headers: dict[str, str], item: Like_Or_Dislike_Request) -> Like_Or_Dislike_Response:
        default_response = Like_Or_Dislike_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_download_backup_data(self, headers: dict[str, str], item: Download_Backup_Data_Request) -> Download_Backup_Data_Response:
        default_response = Download_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def user_upload_backup_data(self, headers: dict[str, str], item: Upload_Backup_Data_Request) -> Upload_Backup_Data_Response:
        default_response = Upload_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def admin_download_backup_data(self, headers: dict[str, str], item: Download_Backup_Data_Request) -> Download_Backup_Data_Response:
        default_response = Download_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def admin_upload_backup_data(self, headers: dict[str, str], item: Upload_Backup_Data_Request) -> Upload_Backup_Data_Response:
        default_response = Upload_Backup_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def _get_headers_dict_from_string(headers: str) -> dict:
    dic = {}
    for line in headers.split("\n"):
        if line.startswith(("GET", "POST")):
            continue
        point_index = line.find(":")
        dic[line[:point_index].strip()] = line[point_index+1:].strip()
    return dic


def run(service_instance: Service_question_and_answer, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    # allow_origins=['*'],
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],

    def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
        return b'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            def handle_get_url(sub_url: str, headers: dict[str, str]) -> bytes:
                sub_url = sub_url.strip("/")
                sub_url = sub_url.lstrip(serve_html_under_which_url)
                if sub_url == '':
                    sub_url = 'index.html'
                real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                if os.path.exists(real_file_path) and os.path.isfile(real_file_path):
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                else:
                    #return b"Resource not found\n\n(This web service is using YRPC (Yingshaoxo Remote Procedure Call))"
                    sub_url = 'index.html'
                    real_file_path = f"{os.path.join(html_folder_path, sub_url)}"
                    with open(real_file_path, mode="rb") as f:
                        the_data = f.read()
                return the_data

            print(f"The website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("question_and_answer", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
        elif (request_url == "ask_yingshaoxo_ai"):
            correct_item = Ask_Yingshaoxo_Ai_Request().from_dict(item)
            return json.dumps((service_instance.ask_yingshaoxo_ai(headers, correct_item)).to_dict())

        elif (request_url == "visitor_get_json_web_token"):
            correct_item = Get_JSON_Web_Token_Request().from_dict(item)
            return json.dumps((service_instance.visitor_get_json_web_token(headers, correct_item)).to_dict())

        elif (request_url == "visitor_is_json_web_token_ok"):
            correct_item = Is_JSON_Web_Token_Ok_Request().from_dict(item)
            return json.dumps((service_instance.visitor_is_json_web_token_ok(headers, correct_item)).to_dict())

        elif (request_url == "visitor_search"):
            correct_item = Search_Request().from_dict(item)
            return json.dumps((service_instance.visitor_search(headers, correct_item)).to_dict())

        elif (request_url == "visitor_get_a_post"):
            correct_item = Get_A_Post_Request().from_dict(item)
            return json.dumps((service_instance.visitor_get_a_post(headers, correct_item)).to_dict())

        elif (request_url == "visitor_get_comment_list_by_id_list"):
            correct_item = Get_Comment_List_By_Id_List_Request().from_dict(item)
            return json.dumps((service_instance.visitor_get_comment_list_by_id_list(headers, correct_item)).to_dict())

        elif (request_url == "user_add_post"):
            correct_item = Add_Post_Request().from_dict(item)
            return json.dumps((service_instance.user_add_post(headers, correct_item)).to_dict())

        elif (request_url == "user_update_post"):
            correct_item = Update_Post_Request().from_dict(item)
            return json.dumps((service_instance.user_update_post(headers, correct_item)).to_dict())

        elif (request_url == "user_delete_post"):
            correct_item = Delete_Post_Request().from_dict(item)
            return json.dumps((service_instance.user_delete_post(headers, correct_item)).to_dict())

        elif (request_url == "user_comment_post"):
            correct_item = Comment_Post_Request().from_dict(item)
            return json.dumps((service_instance.user_comment_post(headers, correct_item)).to_dict())

        elif (request_url == "user_modify_comment"):
            correct_item = Modify_Comment_Request().from_dict(item)
            return json.dumps((service_instance.user_modify_comment(headers, correct_item)).to_dict())

        elif (request_url == "user_delete_comment"):
            correct_item = Delete_Comment_Request().from_dict(item)
            return json.dumps((service_instance.user_delete_comment(headers, correct_item)).to_dict())

        elif (request_url == "user_like_or_dislike_a_post_or_comment"):
            correct_item = Like_Or_Dislike_Request().from_dict(item)
            return json.dumps((service_instance.user_like_or_dislike_a_post_or_comment(headers, correct_item)).to_dict())

        elif (request_url == "user_download_backup_data"):
            correct_item = Download_Backup_Data_Request().from_dict(item)
            return json.dumps((service_instance.user_download_backup_data(headers, correct_item)).to_dict())

        elif (request_url == "user_upload_backup_data"):
            correct_item = Upload_Backup_Data_Request().from_dict(item)
            return json.dumps((service_instance.user_upload_backup_data(headers, correct_item)).to_dict())

        elif (request_url == "admin_download_backup_data"):
            correct_item = Download_Backup_Data_Request().from_dict(item)
            return json.dumps((service_instance.admin_download_backup_data(headers, correct_item)).to_dict())

        elif (request_url == "admin_upload_backup_data"):
            correct_item = Upload_Backup_Data_Request().from_dict(item)
            return json.dumps((service_instance.admin_upload_backup_data(headers, correct_item)).to_dict())

        return f"No API url matchs '{request_url}'"

    class WebRequestHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            self.send_response(200)

            self.send_header("Access-Control-Allow-Origin", "*")

            if sub_url.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif sub_url.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif sub_url.endswith(".js"):
                self.send_header("Content-Type", "text/javascript")

            response = handle_get_url(sub_url, headers)

            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            sub_url = self.path
            headers = _get_headers_dict_from_string(self.headers.as_string())

            content_length = headers.get('Content-Length')
            if content_length is None:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return
            else:
                content_length = int(content_length)
            
            if content_length == 0:
                self.wfile.write("What you send is not json".encode("utf-8"))
                return

            request_json_dict = json.loads(self.rfile.read(content_length))

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = handle_post_url(sub_url, headers, request_json_dict)

            self.wfile.write(response.encode("utf-8"))

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass
    
    # Setting TCP Address
    server_address = ('0.0.0.0', int(port))
    
    # invoking server
    http = ThreadedHTTPServer(server_address, WebRequestHandler)
    
    http.serve_forever()


def run_with_hot_load(watch_path: str, service_instance: Service_question_and_answer, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    import multiprocessing
    from auto_everything.develop import Develop
    develop = Develop()

    the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
    the_running_process.start()

    while True:
        changed = develop.whether_a_folder_has_changed(folder_path=watch_path, type_limiter=[".py", ".html", ".css", ".js"])
        if (changed):
            print("Source code get changed, doing a reloading now...")
            the_running_process.kill()
            while the_running_process.is_alive():
                sleep(1)
            the_running_process = multiprocessing.Process(target=run, args=(service_instance, port, html_folder_path, serve_html_under_which_url))
            the_running_process.start()
        sleep(1)


if __name__ == "__main__":
    service_instance = Service_question_and_answer()
    run(service_instance, port="6060")