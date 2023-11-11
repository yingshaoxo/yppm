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



export interface _A_Post {
    owner_id: string | null;
    id: string | null;
    title: string | null;
    description: string | null;
    comment_id_list: string[] | null;
    create_time_in_10_numbers_timestamp_format: number | null;
    tag: string | null;
}

export class A_Post {
    owner_id: string | null = null;
    id: string | null = null;
    title: string | null = null;
    description: string | null = null;
    comment_id_list: string[] | null = null;
    create_time_in_10_numbers_timestamp_format: number | null = null;
    tag: string | null = null;

    _property_name_to_its_type_dict = {
            owner_id: "string",
            id: "string",
            title: "string",
            description: "string",
            comment_id_list: "string",
            create_time_in_10_numbers_timestamp_format: "number",
            tag: "string",
    };

    _key_string_dict = {
        owner_id: "owner_id",
        id: "id",
        title: "title",
        description: "description",
        comment_id_list: "comment_id_list",
        create_time_in_10_numbers_timestamp_format: "create_time_in_10_numbers_timestamp_format",
        tag: "tag",
    };

    /*
    constructor(owner_id: string | null = null, id: string | null = null, title: string | null = null, description: string | null = null, comment_id_list: string[] | null = null, create_time_in_10_numbers_timestamp_format: number | null = null, tag: string | null = null) {
            this.owner_id = owner_id
            this.id = id
            this.title = title
            this.description = description
            this.comment_id_list = comment_id_list
            this.create_time_in_10_numbers_timestamp_format = create_time_in_10_numbers_timestamp_format
            this.tag = tag
    }
    */

    to_dict(): _A_Post {
        return _general_to_dict_function(this);
    }

    _clone(): A_Post {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _A_Post): A_Post {
        let an_item = new A_Post()
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


export interface _A_Comment {
    owner_id: string | null;
    id: string | null;
    parent_post_id: string | null;
    parent_post_owner_id: string | null;
    description: string | null;
    create_time_in_10_numbers_timestamp_format: number | null;
    tag: string | null;
}

export class A_Comment {
    owner_id: string | null = null;
    id: string | null = null;
    parent_post_id: string | null = null;
    parent_post_owner_id: string | null = null;
    description: string | null = null;
    create_time_in_10_numbers_timestamp_format: number | null = null;
    tag: string | null = null;

    _property_name_to_its_type_dict = {
            owner_id: "string",
            id: "string",
            parent_post_id: "string",
            parent_post_owner_id: "string",
            description: "string",
            create_time_in_10_numbers_timestamp_format: "number",
            tag: "string",
    };

    _key_string_dict = {
        owner_id: "owner_id",
        id: "id",
        parent_post_id: "parent_post_id",
        parent_post_owner_id: "parent_post_owner_id",
        description: "description",
        create_time_in_10_numbers_timestamp_format: "create_time_in_10_numbers_timestamp_format",
        tag: "tag",
    };

    /*
    constructor(owner_id: string | null = null, id: string | null = null, parent_post_id: string | null = null, parent_post_owner_id: string | null = null, description: string | null = null, create_time_in_10_numbers_timestamp_format: number | null = null, tag: string | null = null) {
            this.owner_id = owner_id
            this.id = id
            this.parent_post_id = parent_post_id
            this.parent_post_owner_id = parent_post_owner_id
            this.description = description
            this.create_time_in_10_numbers_timestamp_format = create_time_in_10_numbers_timestamp_format
            this.tag = tag
    }
    */

    to_dict(): _A_Comment {
        return _general_to_dict_function(this);
    }

    _clone(): A_Comment {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _A_Comment): A_Comment {
        let an_item = new A_Comment()
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


export interface _Ask_Yingshaoxo_Ai_Request {
    input: string | null;
}

export class Ask_Yingshaoxo_Ai_Request {
    input: string | null = null;

    _property_name_to_its_type_dict = {
            input: "string",
    };

    _key_string_dict = {
        input: "input",
    };

    /*
    constructor(input: string | null = null) {
            this.input = input
    }
    */

    to_dict(): _Ask_Yingshaoxo_Ai_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Ask_Yingshaoxo_Ai_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Ask_Yingshaoxo_Ai_Request): Ask_Yingshaoxo_Ai_Request {
        let an_item = new Ask_Yingshaoxo_Ai_Request()
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


export interface _Ask_Yingshaoxo_Ai_Response {
    error: string | null;
    answers: string | null;
}

export class Ask_Yingshaoxo_Ai_Response {
    error: string | null = null;
    answers: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            answers: "string",
    };

    _key_string_dict = {
        error: "error",
        answers: "answers",
    };

    /*
    constructor(error: string | null = null, answers: string | null = null) {
            this.error = error
            this.answers = answers
    }
    */

    to_dict(): _Ask_Yingshaoxo_Ai_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Ask_Yingshaoxo_Ai_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Ask_Yingshaoxo_Ai_Response): Ask_Yingshaoxo_Ai_Response {
        let an_item = new Ask_Yingshaoxo_Ai_Response()
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


export interface _Search_Request {
    search_input: string | null;
    page_size: number | null;
    page_number: number | null;
    owner_id: string | null;
}

export class Search_Request {
    search_input: string | null = null;
    page_size: number | null = null;
    page_number: number | null = null;
    owner_id: string | null = null;

    _property_name_to_its_type_dict = {
            search_input: "string",
            page_size: "number",
            page_number: "number",
            owner_id: "string",
    };

    _key_string_dict = {
        search_input: "search_input",
        page_size: "page_size",
        page_number: "page_number",
        owner_id: "owner_id",
    };

    /*
    constructor(search_input: string | null = null, page_size: number | null = null, page_number: number | null = null, owner_id: string | null = null) {
            this.search_input = search_input
            this.page_size = page_size
            this.page_number = page_number
            this.owner_id = owner_id
    }
    */

    to_dict(): _Search_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Search_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_Request): Search_Request {
        let an_item = new Search_Request()
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


export interface _Search_Response {
    error: string | null;
    post_list: A_Post[] | null;
    comment_list: A_Comment[] | null;
}

export class Search_Response {
    error: string | null = null;
    post_list: A_Post[] | null = null;
    comment_list: A_Comment[] | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            post_list: A_Post,
            comment_list: A_Comment,
    };

    _key_string_dict = {
        error: "error",
        post_list: "post_list",
        comment_list: "comment_list",
    };

    /*
    constructor(error: string | null = null, post_list: A_Post[] | null = null, comment_list: A_Comment[] | null = null) {
            this.error = error
            this.post_list = post_list
            this.comment_list = comment_list
    }
    */

    to_dict(): _Search_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Search_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Search_Response): Search_Response {
        let an_item = new Search_Response()
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


export interface _Get_A_Post_Request {
    id: string | null;
}

export class Get_A_Post_Request {
    id: string | null = null;

    _property_name_to_its_type_dict = {
            id: "string",
    };

    _key_string_dict = {
        id: "id",
    };

    /*
    constructor(id: string | null = null) {
            this.id = id
    }
    */

    to_dict(): _Get_A_Post_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_A_Post_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_A_Post_Request): Get_A_Post_Request {
        let an_item = new Get_A_Post_Request()
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


export interface _Get_A_Post_Response {
    error: string | null;
    post: A_Post | null;
}

export class Get_A_Post_Response {
    error: string | null = null;
    post: A_Post | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            post: A_Post,
    };

    _key_string_dict = {
        error: "error",
        post: "post",
    };

    /*
    constructor(error: string | null = null, post: A_Post | null = null) {
            this.error = error
            this.post = post
    }
    */

    to_dict(): _Get_A_Post_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_A_Post_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_A_Post_Response): Get_A_Post_Response {
        let an_item = new Get_A_Post_Response()
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


export interface _Get_Comment_List_By_Id_List_Request {
    comment_id_list: string[] | null;
}

export class Get_Comment_List_By_Id_List_Request {
    comment_id_list: string[] | null = null;

    _property_name_to_its_type_dict = {
            comment_id_list: "string",
    };

    _key_string_dict = {
        comment_id_list: "comment_id_list",
    };

    /*
    constructor(comment_id_list: string[] | null = null) {
            this.comment_id_list = comment_id_list
    }
    */

    to_dict(): _Get_Comment_List_By_Id_List_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Get_Comment_List_By_Id_List_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_Comment_List_By_Id_List_Request): Get_Comment_List_By_Id_List_Request {
        let an_item = new Get_Comment_List_By_Id_List_Request()
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


export interface _Get_Comment_List_By_Id_List_Response {
    error: string | null;
    comment_list: A_Comment[] | null;
}

export class Get_Comment_List_By_Id_List_Response {
    error: string | null = null;
    comment_list: A_Comment[] | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            comment_list: A_Comment,
    };

    _key_string_dict = {
        error: "error",
        comment_list: "comment_list",
    };

    /*
    constructor(error: string | null = null, comment_list: A_Comment[] | null = null) {
            this.error = error
            this.comment_list = comment_list
    }
    */

    to_dict(): _Get_Comment_List_By_Id_List_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Get_Comment_List_By_Id_List_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Get_Comment_List_By_Id_List_Response): Get_Comment_List_By_Id_List_Response {
        let an_item = new Get_Comment_List_By_Id_List_Response()
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


export interface _Add_Post_Request {
    username: string | null;
    a_post: A_Post | null;
}

export class Add_Post_Request {
    username: string | null = null;
    a_post: A_Post | null = null;

    _property_name_to_its_type_dict = {
            username: "string",
            a_post: A_Post,
    };

    _key_string_dict = {
        username: "username",
        a_post: "a_post",
    };

    /*
    constructor(username: string | null = null, a_post: A_Post | null = null) {
            this.username = username
            this.a_post = a_post
    }
    */

    to_dict(): _Add_Post_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Add_Post_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_Post_Request): Add_Post_Request {
        let an_item = new Add_Post_Request()
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


export interface _Add_Post_Response {
    error: string | null;
    success: boolean | null;
    post_id: string | null;
}

export class Add_Post_Response {
    error: string | null = null;
    success: boolean | null = null;
    post_id: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
            post_id: "string",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
        post_id: "post_id",
    };

    /*
    constructor(error: string | null = null, success: boolean | null = null, post_id: string | null = null) {
            this.error = error
            this.success = success
            this.post_id = post_id
    }
    */

    to_dict(): _Add_Post_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Add_Post_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Add_Post_Response): Add_Post_Response {
        let an_item = new Add_Post_Response()
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


export interface _Comment_Post_Request {
    username: string | null;
    a_comment: A_Comment | null;
}

export class Comment_Post_Request {
    username: string | null = null;
    a_comment: A_Comment | null = null;

    _property_name_to_its_type_dict = {
            username: "string",
            a_comment: A_Comment,
    };

    _key_string_dict = {
        username: "username",
        a_comment: "a_comment",
    };

    /*
    constructor(username: string | null = null, a_comment: A_Comment | null = null) {
            this.username = username
            this.a_comment = a_comment
    }
    */

    to_dict(): _Comment_Post_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Comment_Post_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Comment_Post_Request): Comment_Post_Request {
        let an_item = new Comment_Post_Request()
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


export interface _Comment_Post_Response {
    error: string | null;
    success: boolean | null;
    comment_id: string | null;
}

export class Comment_Post_Response {
    error: string | null = null;
    success: boolean | null = null;
    comment_id: string | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
            comment_id: "string",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
        comment_id: "comment_id",
    };

    /*
    constructor(error: string | null = null, success: boolean | null = null, comment_id: string | null = null) {
            this.error = error
            this.success = success
            this.comment_id = comment_id
    }
    */

    to_dict(): _Comment_Post_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Comment_Post_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Comment_Post_Response): Comment_Post_Response {
        let an_item = new Comment_Post_Response()
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


export interface _Download_Backup_Data_Request {
    username: string | null;
}

export class Download_Backup_Data_Request {
    username: string | null = null;

    _property_name_to_its_type_dict = {
            username: "string",
    };

    _key_string_dict = {
        username: "username",
    };

    /*
    constructor(username: string | null = null) {
            this.username = username
    }
    */

    to_dict(): _Download_Backup_Data_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Download_Backup_Data_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Download_Backup_Data_Request): Download_Backup_Data_Request {
        let an_item = new Download_Backup_Data_Request()
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


export interface _Download_Backup_Data_Response {
    error: string | null;
    file_name: string | null;
    file_bytes_in_base64_format: string | null;
}

export class Download_Backup_Data_Response {
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

    to_dict(): _Download_Backup_Data_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Download_Backup_Data_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Download_Backup_Data_Response): Download_Backup_Data_Response {
        let an_item = new Download_Backup_Data_Response()
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


export interface _Admin_Download_Backup_Data_Request {
    token: string | null;
}

export class Admin_Download_Backup_Data_Request {
    token: string | null = null;

    _property_name_to_its_type_dict = {
            token: "string",
    };

    _key_string_dict = {
        token: "token",
    };

    /*
    constructor(token: string | null = null) {
            this.token = token
    }
    */

    to_dict(): _Admin_Download_Backup_Data_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Admin_Download_Backup_Data_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Admin_Download_Backup_Data_Request): Admin_Download_Backup_Data_Request {
        let an_item = new Admin_Download_Backup_Data_Request()
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


export interface _Admin_Download_Backup_Data_Response {
    error: string | null;
    file_name: string | null;
    file_bytes_in_base64_format: string | null;
}

export class Admin_Download_Backup_Data_Response {
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

    to_dict(): _Admin_Download_Backup_Data_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Admin_Download_Backup_Data_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Admin_Download_Backup_Data_Response): Admin_Download_Backup_Data_Response {
        let an_item = new Admin_Download_Backup_Data_Response()
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


export interface _Admin_Upload_Backup_Data_Request {
    token: string | null;
    file_bytes_in_base64_format: string | null;
}

export class Admin_Upload_Backup_Data_Request {
    token: string | null = null;
    file_bytes_in_base64_format: string | null = null;

    _property_name_to_its_type_dict = {
            token: "string",
            file_bytes_in_base64_format: "string",
    };

    _key_string_dict = {
        token: "token",
        file_bytes_in_base64_format: "file_bytes_in_base64_format",
    };

    /*
    constructor(token: string | null = null, file_bytes_in_base64_format: string | null = null) {
            this.token = token
            this.file_bytes_in_base64_format = file_bytes_in_base64_format
    }
    */

    to_dict(): _Admin_Upload_Backup_Data_Request {
        return _general_to_dict_function(this);
    }

    _clone(): Admin_Upload_Backup_Data_Request {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Admin_Upload_Backup_Data_Request): Admin_Upload_Backup_Data_Request {
        let an_item = new Admin_Upload_Backup_Data_Request()
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


export interface _Admin_Upload_Backup_Data_Response {
    error: string | null;
    success: boolean | null;
}

export class Admin_Upload_Backup_Data_Response {
    error: string | null = null;
    success: boolean | null = null;

    _property_name_to_its_type_dict = {
            error: "string",
            success: "boolean",
    };

    _key_string_dict = {
        error: "error",
        success: "success",
    };

    /*
    constructor(error: string | null = null, success: boolean | null = null) {
            this.error = error
            this.success = success
    }
    */

    to_dict(): _Admin_Upload_Backup_Data_Response {
        return _general_to_dict_function(this);
    }

    _clone(): Admin_Upload_Backup_Data_Response {
        let clone = Object.assign(Object.create(Object.getPrototypeOf(this)), this)
        return clone
    }

    from_dict(item: _Admin_Upload_Backup_Data_Response): Admin_Upload_Backup_Data_Response {
        let an_item = new Admin_Upload_Backup_Data_Response()
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