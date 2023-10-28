import { markRaw, reactive } from 'vue'

import * as app_store_rpc from './generated_yrpc/app_store_rpc'
import * as app_store_objects from './generated_yrpc/app_store_objects'

import home_page from "./pages/home_page.vue"
import app_page from "./pages/app_page.vue"

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

let get_host_url = () => {
    return `http://127.0.0.1:3333`
}

enum page_name_dict {
    home_page="home_page",
    app_page="app_page",
}

export var global_dict = reactive({
    show_dialog_window: false,
    show_global_loading: false,
    dialog_message: "Welcome to yingshaoxo's style shop!",
    current_page_name: "",
    current_page_data: {} as any,
    page_name_dict,
    page_name_to_component_dict: {
        [page_name_dict.home_page]:  markRaw(home_page),
        [page_name_dict.app_page]:  markRaw(app_page),
    } as any,
    app_store_objects: app_store_objects,
    client: new app_store_rpc.Client_app_store(
            get_host_url(),
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
    image_dict: new Map<string, string>(), // product_id -> base64 string
})

export var global_functions = {
    init: async () => {
        // await global_functions.redirect_to_user_home_page_if_jwt_is_valid()

        global_functions.go_to_page_based_on_current_url()
    },
    log: (message: any) => {
        console.log(message)
    },
    print: async (message: string) => {
        global_dict.dialog_message = message
        global_dict.show_dialog_window = true

        global_functions.log(message)

        while (global_dict.show_dialog_window == true) {
            await (new Promise(resolve => setTimeout(resolve, 1000)))
        }
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

        if ((<any>Object).values(page_name_dict).includes(the_current_route_name)) {
            global_dict.current_page_name = the_current_route_name
        } else {
            global_dict.current_page_name = global_dict.page_name_dict.home_page
        }
    },
    go_to_page: (page_name: page_name_dict, data: any = {}) => {
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
        //global_dict.current_page_data = data
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
}

export default {
    global_dict, 
    global_functions
}
