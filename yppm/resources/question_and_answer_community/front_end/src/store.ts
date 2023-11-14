import { reactive } from 'vue';

import * as question_and_answer_objects from './generated_yrpc/question_and_answer_objects'
import * as question_and_answer_rpc from './generated_yrpc/question_and_answer_rpc'

const interceptor_function = (data: any) => {
    if (Object.keys(data).includes('error')) {
        if (data?.error) {
            global_functions.print(data?.error)
        }
    } else {
        if (data) {
            if (typeof data === 'string') {
                if (data.trim() != "") {
                    global_functions.print(data)
                }
            }
        }
    }
}

const before_request_function = () => {
    global_dict.show_global_loading = true
}

const after_request_function = () => {
    global_dict.show_global_loading = false
}

let get_host_url = (sub_domain: string) => {
    return `http://127.0.0.1:54321/${sub_domain}`
}

if ((!window.location.host.startsWith("127.")) && (!window.location.host.startsWith("localhost"))) {
    get_host_url = (sub_domain: string) => {
        return `${window.location.protocol}//${window.location.host}/${sub_domain}`
    }
}

let url_list = [
    "https://ask.ai-tools-online.xyz/",
    `${window.location.protocol}//${window.location.host}/`,
    "http://127.0.0.1:54321/"
]

export var global_dict = reactive({
    show_admin_page: false,
    show_global_loading: false,
    show_global_message: false,
    global_message: "Welcome to yingshaoxo's question and answer community!",
    test_done: true,
    current_page_name: "",
    current_page_data: {} as any,
    page_name_dict: {
        search_page: "search_page",
        chat_page: "chat_page",
        detail_page: "detail_page",
    },
    client: new question_and_answer_rpc.Client_question_and_answer(
            get_host_url(""),
            {
            }, 
            (error_string: string)=>{
                global_functions.print(error_string)
            },
            (data: any)=>{
                interceptor_function(data)
            },
            before_request_function,
            after_request_function,
    ),
})

export var global_functions = {
    init: async () => {
        global_functions.go_to_page_based_on_current_url()
    },
    set_reachable_client: async() => {
        global_dict.test_done = false
        for (let i = 0; i < url_list.length; i++) {
            let url = url_list[i]
            let a_client = new question_and_answer_rpc.Client_question_and_answer(
                url,
                {
                }, 
                (error_string: string)=>{
                    if (global_dict.test_done) {
                        global_functions.print(error_string)
                    }
                },
                (data: any)=>{
                    if (global_dict.test_done) {
                        interceptor_function(data)
                    }
                },
                before_request_function,
                after_request_function,
            )
            let response = await a_client.about(new question_and_answer_objects.About_Request())
            if (response?.about != null && response?.about?.includes("yingshaoxo")) {
                global_dict.test_done = true
                global_dict.client = a_client
                return
            }
        }
        global_dict.test_done = true
    },
    log: (message: any) => {
        console.log(message)
    },
    print: async (message: string) => {
        global_dict.global_message = message
        global_dict.show_global_message = true

        global_functions.log(message)

        setTimeout(()=>{
            global_dict.show_global_message = false
        }, 5000)
    },
    go_to_page_based_on_current_url: () => {
        let splits = document.location.href.split("//")
        let splits2 = splits[splits.length-1].split("/")
        let splits3 = splits2[splits2.length-1].split("?")
        let the_current_route_name = splits3[0]

        if (splits3.length > 1) {
            let data_string = splits3[1]
            let an_object = {} as any
            splits = data_string.split("&")
            for (var one_part of splits) {
                splits2 = one_part.split("=")
                if (splits2.length > 1) {
                    an_object[splits2[0]] = decodeURI(splits2[1])
                }
            }
            global_dict.current_page_data = an_object
        }

        if ((<any>Object).values(global_dict.page_name_dict).includes(the_current_route_name)) {
            global_dict.current_page_name = the_current_route_name
        } else {
            global_dict.current_page_name = global_dict.page_name_dict.search_page
        }
    },
    go_to_page: (page_name: string, data: any = {}) => {
        let keys = Object.keys(data)
        let new_url = `./${page_name}`
        if (keys.length > 0) {
            new_url += "?"
            let index = 0
            for (var key of keys) {
                if (index != 0) {
                    new_url += "&"
                }

                let value = data[key]
                new_url += `${key}=${String(value)}`
                
                index += 1
            }
        }
        document.location.href = new_url;     
    },
    execute_a_function_after_x_milliseconds: (a_function: any, milliseconds: number) => {
        setTimeout(a_function, milliseconds)
    },
    make_first_character_upper_case: (text: any) => {
        return text.charAt(0).toUpperCase() + text.slice(1);
    },
    copy_text_to_clipboard: async (text: string) => {
        try {
            var input = document.createElement('textarea');
            input.innerHTML = text;
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
        } catch (e) {
            await navigator.clipboard.writeText(text);
        }
    },
    compress_image: async (blobImg: any, percent: number) => {
        let compress_ratio = percent / 100

        let bitmap = await createImageBitmap(blobImg);
        let canvas = document.createElement("canvas");
        let ctx = canvas.getContext("2d") as any;
        canvas.width = bitmap.width;
        canvas.height = bitmap.height;

        ctx.drawImage(bitmap, 0, 0);
        let dataUrl = canvas.toDataURL("image/jpeg", compress_ratio);

        return dataUrl;
    },
    datestamp_to_string: (datestamp: string | number | null) => {
        if (datestamp == null) {
            return ""
        }
        datestamp = Number(datestamp)
        return new Date(datestamp * 1000).toISOString().replace("T", " ").split(".")[0]
    },
    refresh: () => {
        window.location.reload();
        window.scrollTo(0, 0);
    },
    get_current_url: (): string => {
        return window.location.href
    },
    is_en_broswer: ():boolean => {
        let language = window.navigator.language;
        if (language.startsWith("en-")) {
            return true;
        }
        return false;
    },
    set_value: (key: string, value: string) => {
        localStorage.setItem(key, value)
    },
    get_value: (key: string) => {
        return localStorage.getItem(key)
    },
    get_base64_product_image_by_using_product_id: async (product_id: string | null): Promise<string> => {
      return product_id ?? ""
      /*
      if(product_id == null) {
        return ""
      }

      var get_an_image_file_request = new global_dict.app_store_objects.Get_An_Image_File_Request()
      get_an_image_file_request.product_id = product_id

      let response = await global_dict.visitor_client.get_an_image_file(get_an_image_file_request)
      if (response?.base64_image_data != null) {
        return "data:image/jpeg;base64," + response?.base64_image_data
      }

      return ""
      */
    },
    get_username: (): string => {
        let username = global_functions.get_value("username")
        if (username == null) {
            username = ""
        }
        return username
    },
    download_base64_file: (base64Data: string, fileName: string) => {
        const linkSource = `data:application/octet-stream;base64,${base64Data}`;
        const downloadLink = document.createElement("a");
        downloadLink.href = linkSource;
        downloadLink.download = fileName;
        downloadLink.click();
    },
    download_user_data: async () => {
        let export_data_request = new question_and_answer_objects.Download_Backup_Data_Request()
        export_data_request.username = global_functions.get_username()

        let response = await global_dict.client.user_download_backup_data(export_data_request)
        if (response?.file_bytes_in_base64_format != null) {
            if (response?.file_name != null) {
                global_functions.download_base64_file(response?.file_bytes_in_base64_format, response?.file_name)
            }
        }
    }, 
    download_whole_site_data: async (token: any) => {
        let export_data_request = new question_and_answer_objects.Admin_Download_Backup_Data_Request()
        export_data_request.token = token

        let response = await global_dict.client.admin_download_backup_data(export_data_request)
        if (response?.file_bytes_in_base64_format != null) {
            if (response?.file_name != null) {
                global_functions.download_base64_file(response?.file_bytes_in_base64_format, response?.file_name)
            }
        }
    }, 
    file_to_base64: async (a_file: File) => {
        let a_function = 
          (file: File) => new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.readAsDataURL(file);
              reader.onload = () => {
                  let base64_string = String(reader.result).split(",")[1]
                  resolve(base64_string)
              };
              reader.onerror = error => reject(error);
          })
          return (await a_function(a_file) as string)
    },
    upload_whole_site_data: async (token: any, base64_data_string: any) => {
        let request = new question_and_answer_objects.Admin_Upload_Backup_Data_Request()
        request.token = token
        request.file_bytes_in_base64_format = base64_data_string

        let response = await global_dict.client.admin_upload_backup_data(request)
        if (response?.success != null) {
            global_functions.print("Website data upload successfully.")
        }
    }, 

}

declare global {
  interface Window {
    admin: () => void;
  }
}
window.admin = () => {
    console.log("yingshaoxo is the best.")
    console.log("Welcome, admin.")
    global_dict.show_admin_page = true
}

export default {
    global_dict, 
    global_functions
}
