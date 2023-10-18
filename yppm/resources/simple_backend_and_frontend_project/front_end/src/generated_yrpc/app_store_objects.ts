const _ygrpc_official_types = ["string", "number", "boolean"];

export const clone_object_ = (obj: any) =>  JSON.parse(JSON.stringify(obj));

export const get_secret_alphabet_dict_ = (a_secret_string: string) =>  {
    const ascii_lowercase = "abcdefghijklmnopqrstuvwxyz".split("")
    const number_0_to_9 = "0123456789".split("")

    var new_key = a_secret_string.replace(" ", "").toLowerCase().split("")
    var character_list: string[] = []
    for (var char of new_key) {
        if ((/[a-zA-Z]/).test(char)) {
            if (!character_list.includes(char)) {
                character_list.push(char)
            }
        }
    }

    if (character_list.length >= 26) {
        character_list = character_list.slice(0, 26)
    } else {
        var characters_that_the_key_didnt_cover: string[] = []
        for (var char of ascii_lowercase) {
            if (!character_list.includes(char)) {
                characters_that_the_key_didnt_cover.push(char)
            }
        }
        character_list = character_list.concat(characters_that_the_key_didnt_cover) 
    }

    var final_dict = {} as Record<string, string>

    // for alphabet
    for (let [index, char] of ascii_lowercase.entries()) {
        final_dict[char] = character_list[index]
    }

    // for numbers
    var original_numbers_in_alphabet_format = ascii_lowercase.slice(0, 10) // 0-9 representations in alphabet format
    var secret_numbers_in_alphabet_format = Object.values(final_dict).slice(0, 10)
    var final_number_list = [] as string[]
    for (var index in number_0_to_9) {
        var secret_char = secret_numbers_in_alphabet_format[index]
        if (original_numbers_in_alphabet_format.includes(secret_char)) {
            final_number_list.push(String(original_numbers_in_alphabet_format.findIndex((x) => x===secret_char)))
        }
    }
    if (final_number_list.length >= 10) {
        final_number_list = final_number_list.slice(0, 10)
    } else {
        var numbers_that_didnt_get_cover = [] as string[]
        for (var char of number_0_to_9) {
            if (!final_number_list.includes(char)) {
                numbers_that_didnt_get_cover.push(char)
            }
        }
        final_number_list = final_number_list.concat(numbers_that_didnt_get_cover)
    }
    for (let [index, char] of final_number_list.entries()) {
        final_dict[String(index)] = char
    }

    return final_dict
};

export const encode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

export const decode_message_ = (a_secret_dict: Record<string, string>, message: string):string => {
    var new_secret_dict = {} as Record<string, string>
    for (var key of Object.keys(a_secret_dict)) {
        new_secret_dict[a_secret_dict[key]] = key
    }
    a_secret_dict = new_secret_dict

    var new_message = ""
    for (const char of message) {
        if ((!(/[a-zA-Z]/).test(char)) && (!(/^\d$/).test(char))) {
            new_message += char
            continue
        }
        var new_char = a_secret_dict[char.toLowerCase()]
        if ((/[A-Z]/).test(char)) {
            new_char = new_char.toUpperCase()
        }
        new_message += new_char
    }
    return new_message
}

const _general_to_dict_function = (object: any): any => {
    let the_type = typeof object
    if (the_type == "object") {
        if (object == null) {
            return null
        } else if (Array.isArray(object)) {
            let new_list: any[] = []
            for (const one of object) {
                new_list.push(_general_to_dict_function(one))
            }
            return new_list
        } else {
            let keys = Object.keys(object);
            if (keys.includes("_key_string_dict")) {
                // custom message type
                let new_dict: any = {}
                keys = keys.filter((e) => !["_property_name_to_its_type_dict", "_key_string_dict"].includes(e));
                for (const key of keys) {
                    new_dict[key] = _general_to_dict_function(object[key])
                    // the enum will become a string in the end, so ignore it
                }
                return new_dict
            }
        }
    } else {
        if (_ygrpc_official_types.includes(typeof object)) {
            return object
        } else {
            return null
        }
    }
    return null
};

const _general_from_dict_function = (old_object: any, new_object: any): any => {
    let the_type = typeof new_object
    if (the_type == "object") {
        if (Array.isArray(new_object)) {
            //list
            let new_list: any[] = []
            for (const one of new_object) {
                new_list.push(structuredClone(_general_from_dict_function(old_object, one)))
            }
            return new_list
        } else {
            // dict or null
            if (new_object == null) {
                return null
            } else {
                let keys = Object.keys(old_object);
                if (keys.includes("_key_string_dict")) {
                    keys = Object.keys(old_object._property_name_to_its_type_dict)
                    for (const key of keys) {
                        if (Object.keys(new_object).includes(key)) {
                            if ((typeof old_object._property_name_to_its_type_dict[key]) == "string") {
                                // default value type
                                old_object[key] = new_object[key]
                            } else {
                                // custom message type || enum
                                if (
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("class") || 
                                    (typeof old_object._property_name_to_its_type_dict[key]).includes("function")
                                ) {
                                    // custom message type || a list of custom type
                                    var reference_object = new (old_object._property_name_to_its_type_dict[key])()
                                    old_object[key] = structuredClone(_general_from_dict_function(reference_object, new_object[key]))
                                } else {
                                    // enum
                                    if (Object.keys(new_object).includes(key)) {
                                        old_object[key] = new_object[key]
                                    } else {
                                        old_object[key] = null
                                    }
                                }
                            }
                        } 
                    }
                } else {
                    return null
                }
            }
        }
    } 
    return old_object
}



export interface _An_App {
    create_time_in_10_numbers_timestamp_format: number | null;
    name: string | null;
    description: string | null;
    url: string | null;
    app_icon_in_base64: string | null;
    author_contact_method: string | null;
    click_number: number | null;
}

export class An_App {
    create_time_in_10_numbers_timestamp_format: number | null = null;
    name: string | null = null;
    description: string | null = null;
    url: string | null = null;
    app_icon_in_base64: string | null = null;
    author_contact_method: string | null = null;
    click_number: number | null = null;

    _property_name_to_its_type_dict = {
            create_time_in_10_numbers_timestamp_format: "number",
            name: "string",
            description: "string",
            url: "string",
            app_icon_in_base64: "string",
            author_contact_method: "string",
            click_number: "number",
    };

    _key_string_dict = {
        create_time_in_10_numbers_timestamp_format: "create_time_in_10_numbers_timestamp_format",
        name: "name",
        description: "description",
        url: "url",
        app_icon_in_base64: "app_icon_in_base64",
        author_contact_method: "author_contact_method",
        click_number: "click_number",
    };

    /*
    constructor(create_time_in_10_numbers_timestamp_format: number | null = null, name: string | null = null, description: string | null = null, url: string | null = null, app_icon_in_base64: string | null = null, author_contact_method: string | null = null, click_number: number | null = null) {
            this.create_time_in_10_numbers_timestamp_format = create_time_in_10_numbers_timestamp_format
            this.name = name
            this.description = description
            this.url = url
            this.app_icon_in_base64 = app_icon_in_base64
            this.author_contact_method = author_contact_method
            this.click_number = click_number
    }
    */

    to_dict(): _An_App {
        return _general_to_dict_function(this);
    }

    _clone(): An_App {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _An_App): An_App {
        let an_item = new An_App()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Add_App_Request {
    question: string | null;
    answer: string | null;
    an_app: An_App | null;
}

export class Add_App_Request {
    question: string | null = null;
    answer: string | null = null;
    an_app: An_App | null = null;

    _property_name_to_its_type_dict = {
            question: "string",
            answer: "string",
            an_app: An_App,
    };

    _key_string_dict = {
        question: "question",
        answer: "answer",
        an_app: "an_app",
    };

    /*
    constructor(question: string | null = null, answer: string | null = null, an_app: An_App | null = null) {
            this.question = question
            this.answer = answer
            this.an_app = an_app
    }
    */

    to_dict(): _Add_App_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Add_App_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_App_Request): Add_App_Request {
        let an_item = new Add_App_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Add_App_Response {
    error: string | null;
    app_name: string | null;
}

export class Add_App_Response {
    error: string | null = null;
    app_name: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            app_name: "string",
    };

    _key_string_dict = {
        error: "error",
        app_name: "app_name",
    };

    /*
    constructor(error: string | null = null, app_name: string | null = null) {
            this.error = error
            this.app_name = app_name
    }
    */

    to_dict(): _Add_App_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Add_App_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_App_Response): Add_App_Response {
        let an_item = new Add_App_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Search_App_Request {
    search_input: string | null;
    page_size: number | null;
    page_number: number | null;
}

export class Search_App_Request {
    search_input: string | null = null;
    page_size: number | null = null;
    page_number: number | null = null;

    _property_name_to_its_type_dict = {
            search_input: "string",
            page_size: "number",
            page_number: "number",
    };

    _key_string_dict = {
        search_input: "search_input",
        page_size: "page_size",
        page_number: "page_number",
    };

    /*
    constructor(search_input: string | null = null, page_size: number | null = null, page_number: number | null = null) {
            this.search_input = search_input
            this.page_size = page_size
            this.page_number = page_number
    }
    */

    to_dict(): _Search_App_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Search_App_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_App_Request): Search_App_Request {
        let an_item = new Search_App_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Search_App_Response {
    error: string | null;
    app_list: An_App[] | null;
}

export class Search_App_Response {
    error: string | null = null;
    app_list: An_App[] | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            app_list: An_App,
    };

    _key_string_dict = {
        error: "error",
        app_list: "app_list",
    };

    /*
    constructor(error: string | null = null, app_list: An_App[] | null = null) {
            this.error = error
            this.app_list = app_list
    }
    */

    to_dict(): _Search_App_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Search_App_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_App_Response): Search_App_Response {
        let an_item = new Search_App_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Get_App_Detail_Request {
    name: string | null;
}

export class Get_App_Detail_Request {
    name: string | null = null;

    _property_name_to_its_type_dict = {
            name: "string",
    };

    _key_string_dict = {
        name: "name",
    };

    /*
    constructor(name: string | null = null) {
            this.name = name
    }
    */

    to_dict(): _Get_App_Detail_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_App_Detail_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_App_Detail_Request): Get_App_Detail_Request {
        let an_item = new Get_App_Detail_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Get_App_Detail_Response {
    error: string | null;
    an_app: An_App | null;
}

export class Get_App_Detail_Response {
    error: string | null = null;
    an_app: An_App | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            an_app: An_App,
    };

    _key_string_dict = {
        error: "error",
        an_app: "an_app",
    };

    /*
    constructor(error: string | null = null, an_app: An_App | null = null) {
            this.error = error
            this.an_app = an_app
    }
    */

    to_dict(): _Get_App_Detail_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_App_Detail_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_App_Detail_Response): Get_App_Detail_Response {
        let an_item = new Get_App_Detail_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Export_Data_Request {

}

export class Export_Data_Request {


    _property_name_to_its_type_dict = {

    };

    _key_string_dict = {

    };

    /*
    constructor() {

    }
    */

    to_dict(): _Export_Data_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Export_Data_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Export_Data_Request): Export_Data_Request {
        let an_item = new Export_Data_Request()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}


export interface _Export_Data_Response {
    error: string | null;
    file_name: string | null;
    file_bytes_in_base64_format: string | null;
}

export class Export_Data_Response {
    error: string | null = null;
    file_name: string | null = null;
    file_bytes_in_base64_format: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            file_name: "string",
            file_bytes_in_base64_format: "string",
    };

    _key_string_dict = {
        error: "error",
        file_name: "file_name",
        file_bytes_in_base64_format: "file_bytes_in_base64_format",
    };

    /*
    constructor(error: string | null = null, file_name: string | null = null, file_bytes_in_base64_format: string | null = null) {
            this.error = error
            this.file_name = file_name
            this.file_bytes_in_base64_format = file_bytes_in_base64_format
    }
    */

    to_dict(): _Export_Data_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Export_Data_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Export_Data_Response): Export_Data_Response {
        let an_item = new Export_Data_Response()
        let new_dict = _general_from_dict_function(an_item, item)

        for (const key of Object.keys(new_dict)) {
            let value = new_dict[key]
            //@ts-ignore
            this[key] = value
            //@ts-ignore
            an_item[key] = value
        }

        return an_item
    }
}