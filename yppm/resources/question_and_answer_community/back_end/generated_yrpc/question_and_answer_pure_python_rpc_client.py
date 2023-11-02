from .question_and_answer_objects import *

from typing import Any, Callable
import json
from urllib import request


def _send_a_post(url: str, data: dict, headers: dict | None=None) -> str:
    a_request = request.Request(url, method="POST")
    a_request.add_header('Content-Type', 'application/json')
    if headers != None:
        for key, value in headers.items():
            a_request.add_header(key, value)
    data = json.dumps(data, indent=4)
    data = data.encode("utf-8", errors="ignore")
    r_ = request.urlopen(a_request, data=data)
    content = r_.read().decode("utf-8", errors="ignore")
    return content


class Client_question_and_answer:
    def __init__(self, service_url: str, headers: dict[str, Any] | None = None, error_handle_function: Callable[[str], None] | None = None, special_error_key: str = "__yingshaoxo's_error__", interceptor_function: Callable[[dict], None] | None = None):
        if (service_url.endswith("/")):
            service_url = service_url[:-1]
        self._service_url = service_url 

        if headers == None:
            headers = {}
        self._header = headers

        def _default_error_handle_function(error_message: str):
            print(f"errors: {error_message}")
        if error_handle_function == None:
            error_handle_function = _default_error_handle_function
        self._error_handle_function = error_handle_function

        self._special_error_key = special_error_key

        def _default_interceptor_function(data: dict):
            pass
        if interceptor_function == None:
            interceptor_function = _default_interceptor_function
        self._interceptor_function = interceptor_function

    def _get_reponse_or_error_by_url_path_and_input(self, sub_url: str, input_dict: dict[str, Any]):
        the_url = f"{self._service_url}/question_and_answer/{sub_url}/"
        try:
            response = _send_a_post(url=the_url, data=input_dict, headers=self._header)
            json_response = json.loads(response)
            self._interceptor_function(json_response)
            return json_response
        except Exception as e: 
            return {self._special_error_key: str(e)}

    def visitor_get_json_web_token(self, item: Get_JSON_Web_Token_Request, ignore_error: bool | None=None) -> Get_JSON_Web_Token_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("visitor_get_json_web_token", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_JSON_Web_Token_Response().from_dict(result)

    def visitor_is_json_web_token_ok(self, item: Is_JSON_Web_Token_Ok_Request, ignore_error: bool | None=None) -> Is_JSON_Web_Token_Ok_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("visitor_is_json_web_token_ok", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Is_JSON_Web_Token_Ok_Response().from_dict(result)

    def visitor_search(self, item: Search_Request, ignore_error: bool | None=None) -> Search_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("visitor_search", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Search_Response().from_dict(result)

    def visitor_get_a_post(self, item: Get_A_Post_Request, ignore_error: bool | None=None) -> Get_A_Post_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("visitor_get_a_post", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_A_Post_Response().from_dict(result)

    def visitor_get_comment_list_by_id_list(self, item: Get_Comment_List_By_Id_List_Request, ignore_error: bool | None=None) -> Get_Comment_List_By_Id_List_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("visitor_get_comment_list_by_id_list", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Get_Comment_List_By_Id_List_Response().from_dict(result)

    def user_add_post(self, item: Add_Post_Request, ignore_error: bool | None=None) -> Add_Post_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_add_post", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Add_Post_Response().from_dict(result)

    def user_update_post(self, item: Update_Post_Request, ignore_error: bool | None=None) -> Update_Post_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_update_post", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Update_Post_Response().from_dict(result)

    def user_delete_post(self, item: Delete_Post_Request, ignore_error: bool | None=None) -> Delete_Post_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_delete_post", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Delete_Post_Response().from_dict(result)

    def user_comment_post(self, item: Comment_Post_Request, ignore_error: bool | None=None) -> Comment_Post_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_comment_post", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Comment_Post_Response().from_dict(result)

    def user_modify_comment(self, item: Modify_Comment_Request, ignore_error: bool | None=None) -> Modify_Comment_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_modify_comment", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Modify_Comment_Response().from_dict(result)

    def user_delete_comment(self, item: Delete_Comment_Request, ignore_error: bool | None=None) -> Delete_Comment_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_delete_comment", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Delete_Comment_Response().from_dict(result)

    def user_like_or_dislike_a_post_or_comment(self, item: Like_Or_Dislike_Request, ignore_error: bool | None=None) -> Like_Or_Dislike_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_like_or_dislike_a_post_or_comment", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Like_Or_Dislike_Response().from_dict(result)

    def user_download_backup_data(self, item: Download_Backup_Data_Request, ignore_error: bool | None=None) -> Download_Backup_Data_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_download_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Download_Backup_Data_Response().from_dict(result)

    def user_upload_backup_data(self, item: Upload_Backup_Data_Request, ignore_error: bool | None=None) -> Upload_Backup_Data_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("user_upload_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Upload_Backup_Data_Response().from_dict(result)

    def admin_download_backup_data(self, item: Download_Backup_Data_Request, ignore_error: bool | None=None) -> Download_Backup_Data_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("admin_download_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Download_Backup_Data_Response().from_dict(result)

    def admin_upload_backup_data(self, item: Upload_Backup_Data_Request, ignore_error: bool | None=None) -> Upload_Backup_Data_Response | None:
        result = self._get_reponse_or_error_by_url_path_and_input("admin_upload_backup_data", item.to_dict())
        if self._special_error_key in result.keys():
            if ((ignore_error == None) or ((ignore_error != None) and (not ignore_error))):
                self._error_handle_function(result[self._special_error_key])
            return None
        else:
            return Upload_Backup_Data_Response().from_dict(result)