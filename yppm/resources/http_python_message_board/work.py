import time
import socket
import json
from urllib.parse import unquote

a_list = ["hi", "you"]

def handle_request(request_type, url, url_key_and_value_dict):
    if request_type == "GET" and url == "/":
        message_list_html = ""
        for a_message in reversed(a_list):
            message_list_html += """
<div style="margin-bottom: 20px; background-color: #E8E8E8; padding: 5px; overflow: scroll;"><pre>{message}</pre></div>
""".format(message=a_message)
        message_list_html = """
<div style="display: flex; flex-direction: column; margin-top: 30px;">
""" + message_list_html + """
</div>
"""
        return "html", """
<script>
/*
var dict = {};
dict.key1 = "value1";
dict.key2 = "value2";

var list = [];
list.push({ key: "key1", value: "value1" });
list.push({ key: "key2", value: "value2" });
*/

window.console = window.console || (function() {
    var c = {};
    c.log = c.warn = c.debug = c.info = c.error = c.time = c.dir = c.profile = c.clear = c.exception = c.trace = c.assert = function() {};
    return c;
})();

function get_input_value() {
    return document.getElementById("a_textarea").value;
    //.innerHTML = new Date();
}

function send_get_request(url) {
    window.location = url;
}

function send_request(url, data_string) {
    var is_ie = false;

    var xmlhttp;
    if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        is_ie = true;
    } else if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        alert("Your browser does not support XMLHTTP.");
        return;
    }

    if (is_ie) {
        url = url.concat(encodeURIComponent(data_string));
        xmlhttp.open("GET", url, true);
    } else {
        xmlhttp.open("POST", url, true);
    }
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    //application/json

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            //JSON.stringify({});
            //JSON.parse(xmlhttp.responseText);
            var response = xmlhttp.responseText;
            console.log(response);
        } else if (xmlhttp.readyState === 4) {
            console.error("Error: " + xmlhttp.statusText);
        }
        setTimeout(refresh_page, 200);
    };

    if (is_ie) {
        xmlhttp.send();
    } else {
        xmlhttp.send(encodeURIComponent(data_string));
    }
}

function leave_a_new_message() {
    send_request("/new_message?", (new String('text=')).concat(get_input_value()));
}

function refresh_page() {
    window.location = window.location.href;
}

function refresh_page_without_paramater() {
    location.href = location.href.split('?')[0];
}
</script>

<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">

<div style="margin-top: 30px;">Hello, welcome to yingshaoxo message board.</div>

<div style="margin-top: 30px;"></div>

<form action="/new_message?" method="post">
    <div style="display: flex; flex-direction: column; width: 100%;">
        <div>
            <textarea id="a_textarea" type="text" name="text" style="height: 200px; width: 100%;"></textarea>
            <!--input name="name"></input-->
        </div>
        <div style="margin-top: 5px; display: flex; flex-direction: row;">
            <button type="button" onclick="leave_a_new_message()" style="padding: 2px; padding-left: 10px; padding-right: 10px;">
                Leave A Message
            </button>
            <input type="submit" value="Submit it" style="margin-left: 15px; padding: 2px; padding-left: 10px; padding-right: 10px;" />
        </div>
    </div>
</form>
""" + message_list_html
    elif url.startswith("/new_message?"):
        a_list.append(url_key_and_value_dict.get("text"))
        return "text", "Add successfully."
    elif url.startswith("/message_list?"):
        return "text", json.dumps(a_list)
    else:
        return "text", 'Hello, welcome to yingshaoxo message board.' + "\n\n" + str([request_type, url, url_key_and_value_dict])

def url_decode(encoded_string):
    result = ""
    i = 0
    while i < len(encoded_string):
        if encoded_string[i] == '+':
            result += ' '
            i += 1
        elif encoded_string[i] == '%':
            try:
                hex_code = encoded_string[i + 1:i + 3]
                char = chr(int(hex_code, 16))
                result += char
                i += 3
            except (ValueError, IndexError):
                result += encoded_string[i]
                i += 1
        else:
            result += encoded_string[i]
            i += 1
    return result

def parse_url(request):
    request_type = request.strip().split(" ")[0]
    if not request_type == "GET" and not request_type == "POST":
        return request_type, "", {}
    else:
        url = request.split(" ")[1]
        url_dict = {}
        key_value_text_list = []
        if request_type == "GET" :
            url_dict = {}
            if "?" in url:
                key_value_text_list = url.split("?")[1].split("&")
                key_value_text_list = [url_decode(unquote(one)) for one in key_value_text_list]
        elif request_type == "POST":
            raw_string = request.split("\r\n\r\n")[1].strip()
            key_value_text_list = url_decode(unquote(raw_string)).split("&")

        for key_and_value_text in key_value_text_list:
            splits = key_and_value_text.split("=")
            if len(splits) == 2:
                key, value = splits
                url_dict[key] = value

        return request_type, url, url_dict

def work_function(port_in_number=8899):
    print("do it for fun.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port_in_number))
    server_socket.listen(100)
    print("http service ready.\n")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            print("get request:", request)
            request_type, url, url_key_and_value_dict = parse_url(request)
            print()
            print(request_type)
            print(url)
            print(url_key_and_value_dict)

            return_type, return_value = handle_request(request_type, url, url_key_and_value_dict)

            response = 'HTTP/1.1 200 OK\n'
            if return_type == "html":
                response += "Content-Type: text/html\n\n"
                response += return_value
            elif return_type == "text":
                response += "\n" + return_value

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(e)

    #server_socket.shutdown(2)
    #server_socket.close()
