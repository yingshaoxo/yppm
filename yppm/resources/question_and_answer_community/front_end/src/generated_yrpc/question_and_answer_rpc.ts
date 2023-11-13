import * as question_and_answer_objects from './question_and_answer_objects'

export class Client_question_and_answer {
  /**
   * @param {string} _service_url is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
   * @param {{ [key: string]: string }} _header  http headers, it's a dictionary, liek {'content-type', 'application/json'}
   * @param {Function} _error_handle_function will get called when http request got error, you need to give it a function like: (err: String) {print(err)}
   * @param {Function} _interceptor_function will get called for every response, you need to give it a function like: (data: dict[Any, Any]) {print(data)}
   * @param {Function} _function_before_request will get called before every request, you need to give it a function like: () {global_loading_animation = true}
   * @param {Function} _function_after_request will get called after every request, you need to give it a function like: () {global_loading_animation = false}
   */
    _service_url: string
    _header: { [key: string]: string } = {}
    _error_handle_function: (error: string) => void = (error: string) => {console.log(error)}
    _special_error_key: string = "__yingshaoxo's_error__"
    _interceptor_function: (data: any) => void = (data: any) => {console.log(data)}
    _function_before_request: () => void = () => {}
    _function_after_request: () => void = () => {}

    constructor(service_url: string, header?: { [key: string]: string }, error_handle_function?: (error: string) => void, interceptor_function?: (data: any) => void, function_before_request?: () => void, function_after_request?: () => void) {
        if (service_url.endsWith("/")) {
            service_url = service_url.slice(0, service_url.length-1);
        }
        try {
            if (location.protocol === 'https:') {
                if (service_url.startsWith("http:")) {
                    service_url = service_url.replace("http:", "https:")
                }
            } else if (location.protocol === 'http:') {
                if (service_url.startsWith("https:")) {
                    service_url = service_url.replace("https:", "http:")
                }
            }
        } catch (e) {
        }
        this._service_url = service_url
        
        if (header != null) {
            this._header = header
        }

        if (error_handle_function != null) {
            this._error_handle_function = error_handle_function
        }

        if (interceptor_function != null) {
            this._interceptor_function = interceptor_function
        }

        if (function_before_request != null) {
            this._function_before_request = function_before_request
        }

        if (function_after_request != null) {
            this._function_after_request = function_after_request
        }
    } 

    async _get_reponse_or_error_by_url_path_and_input(sub_url: string, input_dict: { [key: string]: any }): Promise<any> {
        let the_url = `${this._service_url}/question_and_answer/${sub_url}/`
        try {
            this._function_before_request()
            const response = await fetch(the_url, 
            {
                method: "POST",
                body: JSON.stringify(input_dict),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    ...this._header
                }
            });
            var json_response = await response.json()
            this._function_after_request()
            this._interceptor_function(json_response)
            return json_response
        } catch (e) {
            this._function_after_request()
            return {[this._special_error_key]: String(e)};
        }
    }

    async about(item: question_and_answer_objects.About_Request, ignore_error?: boolean): Promise<question_and_answer_objects.About_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("about", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.About_Response().from_dict(result)
        }
    }

    async ask_yingshaoxo_ai(item: question_and_answer_objects.Ask_Yingshaoxo_Ai_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Ask_Yingshaoxo_Ai_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("ask_yingshaoxo_ai", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Ask_Yingshaoxo_Ai_Response().from_dict(result)
        }
    }

    async visitor_search(item: question_and_answer_objects.Search_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Search_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("visitor_search", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Search_Response().from_dict(result)
        }
    }

    async visitor_get_a_post(item: question_and_answer_objects.Get_A_Post_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Get_A_Post_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("visitor_get_a_post", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Get_A_Post_Response().from_dict(result)
        }
    }

    async visitor_get_comment_list_by_id_list(item: question_and_answer_objects.Get_Comment_List_By_Id_List_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Get_Comment_List_By_Id_List_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("visitor_get_comment_list_by_id_list", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Get_Comment_List_By_Id_List_Response().from_dict(result)
        }
    }

    async user_add_post(item: question_and_answer_objects.Add_Post_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Add_Post_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("user_add_post", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Add_Post_Response().from_dict(result)
        }
    }

    async user_comment_post(item: question_and_answer_objects.Comment_Post_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Comment_Post_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("user_comment_post", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Comment_Post_Response().from_dict(result)
        }
    }

    async user_download_backup_data(item: question_and_answer_objects.Download_Backup_Data_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Download_Backup_Data_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("user_download_backup_data", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Download_Backup_Data_Response().from_dict(result)
        }
    }

    async admin_download_backup_data(item: question_and_answer_objects.Admin_Download_Backup_Data_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Admin_Download_Backup_Data_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("admin_download_backup_data", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Admin_Download_Backup_Data_Response().from_dict(result)
        }
    }

    async admin_upload_backup_data(item: question_and_answer_objects.Admin_Upload_Backup_Data_Request, ignore_error?: boolean): Promise<question_and_answer_objects.Admin_Upload_Backup_Data_Response | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("admin_upload_backup_data", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new question_and_answer_objects.Admin_Upload_Backup_Data_Response().from_dict(result)
        }
    }
}

export default Client_question_and_answer