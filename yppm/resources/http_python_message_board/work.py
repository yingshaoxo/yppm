import time
import socket
import json
import os
from datetime import datetime

try:
    from urllib.parse import unquote
except Exception as e:
    print("error:", e)
    def unquote(text):
        return text

old_print = print
def fake_print(*object_list):
    for object in object_list:
        old_print(str(object).encode("utf-8"))
print = fake_print

absolute_current_folder_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(absolute_current_folder_path, "./data.txt")
a_list = ["Hi, you.\nYou can leave whatever message you want.", "For example, 'yingshaoxo: Long time no see.'\nHow to prove it is sent from yingshaoxo?\nAsk yingshaoxo yourself in other way."]

def get_current_time():
    now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    current_time = "{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return current_time

def load_disk_data():
    global a_list

    if not os.path.exists(data_file_path):
        with open(data_file_path, "w") as f:
            f.write(json.dumps(a_list))

    with open(data_file_path, "r") as f:
        all_data_as_text = f.read()
    a_list = json.loads(all_data_as_text)

def write_data_to_disk():
    global a_list

    with open(data_file_path, "w") as f:
        f.write(json.dumps(a_list, indent=4))

def handle_request(request_type, url, url_key_and_value_dict):
    if request_type == "GET" and (url == "/" or url.startswith("/?")):
        message_list_html = ""

        page_number = url_key_and_value_dict.get("page")
        if page_number == None:
            page_number = 0
        page_number = int(page_number)
        start_index = page_number * 10
        end_index = start_index + 10

        if start_index > len(a_list):
            return "html", """
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">

Error: No more message out there.
"""

        for a_message in a_list[start_index: end_index]:
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

function formEncode(str) {
    str = str.replace(/\\n/g, '\\r\\n');
    var encoded = '';
    for (var i = 0; i < str.length; i++) {
        var char = str.charAt(i);
        var code = char.charCodeAt(0);
        if (code > 127 || (char === '&' || char === '#')) {
            encoded += '&#' + code + ';';
        } else {
            encoded += char;
        }
    }
    return encodeURIComponent(encoded).replace(/%20/g, '+');
}

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

    //url = url.concat(encodeURIComponent(data_string));
    url = url.concat(data_string);

    xmlhttp.open("GET", url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

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

    xmlhttp.send();
}

function leave_a_new_message() {
    send_request("/new_message?", (new String('text=')).concat(formEncode(get_input_value())));
}

function refresh_page() {
    window.location = window.location.href;
}

function refresh_page_without_paramater() {
    location.href = location.href.split('?')[0];
}
</script>

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

""" + message_list_html + """
<div style="width: 100%; margin-top: 10px; margin-bottom: 30px; display: flex; flex-direction: row; justify-content: left;">
    <button type="button" onclick="window.location.href='{next_page_url}'" style="padding: 2px; padding-left: 10px; padding-right: 10px;">
        Next Page
    </button>
</div>
""".format(next_page_url="/?page="+str(page_number+1))
    elif url.startswith("/new_message?"):
        the_new_message = url_key_and_value_dict.get("text")
        if the_new_message == None:
            the_new_message = ""
        the_new_message = the_new_message.strip()
        if the_new_message != "":
            the_new_message = get_current_time() + "\n\n" + the_new_message
            a_list.insert(0, the_new_message)
            write_data_to_disk()
            return "html", """
<p>Add successfully.</p>
            """
        else:
            return "html", """
<p>You should input something.</p>
            """
    elif url.startswith("/message_list?"):
        return "text", json.dumps(a_list)
    else:
        return "text", 'Hello, welcome to yingshaoxo message board.' + "\n\n" + str([request_type, url, url_key_and_value_dict])

def url_decode(encoded_string):
    # do not support chinese yet, english should be fine.
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
        elif request_type == "POST":
            raw_string = request.split("\r\n\r\n")[1].strip()
            key_value_text_list = raw_string.split("&")

        for key_and_value_text in key_value_text_list:
            splits = key_and_value_text.split("=")
            if len(splits) == 2:
                key, value = splits
                url_dict[key] = unquote(url_decode(value))

        return request_type, url, url_dict

def work_function(port_in_number=8899):
    print("do it for fun.")

    load_disk_data()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port_in_number))
    server_socket.listen(100)
    print("http service ready.\n")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(2048).decode('utf-8')
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
                response += """
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">
"""
                response += return_value
            elif return_type == "text":
                response += "\n" + return_value

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(e)

    #server_socket.shutdown(2)
    #server_socket.close()


if __name__ == '__main__':
    work_function(8899)
