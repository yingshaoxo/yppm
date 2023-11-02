from .question_and_answer_objects import *


from typing import Any
import json
from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


class Service_question_and_answer:
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


def run(service_instance: Service_question_and_answer, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    def handle_get_url(sub_url: str, headers: dict[str, str]) -> str:
        return 'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> dict | str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("question_and_answer", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
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

    def general_handler(request: Yingshaoxo_Http_Request) -> dict | str:
        response = f"No handler for {request.url}"
        if request.method == "GET":
            response = handle_get_url(request.url, request.headers)
        elif request.method == "POST":
            response = handle_post_url(request.url, request.headers, json.loads(request.payload))
        return response

    router = {
        r"(.*)": general_handler,
    }

    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
    yingshaoxo_http_server.start(host="0.0.0.0", port=int(port), html_folder_path=html_folder_path, serve_html_under_which_url=serve_html_under_which_url)


if __name__ == "__main__":
    service_instance = Service_question_and_answer()
    run(service_instance, port="6060")