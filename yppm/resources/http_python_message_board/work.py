import time
import socket
import json

a_list = ["hi", "you"]

def handle_request(url, url_key_and_value_dict):
    if url == "/" or url == "":
        message_list_html = ""
        for a_message in reversed(a_list):
            message_list_html += """<div style="margin-bottom: 20px; background-color: #E8E8E8; padding: 5px;"><pre>{message}</pre></div>\n""".format(message=a_message)
        message_list_html = '\n<div style="display: flex; flex-direction: column; margin-top: 30px;">\n' + message_list_html + '</div>'
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

function get_input_value() {
    return document.getElementById("a_textarea").value;
    //.innerHTML = new Date();
}

function send_get_request(url) {
    var xmlhttp;
    if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        alert("Your browser does not support XMLHTTP.");
        return;
    }

    xmlhttp.open("GET", url, true); // true means async

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            //var response = JSON.parse(xmlhttp.responseText);
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
    var url = (new String('new_message?text=')).concat(get_input_value());
    send_get_request(url);
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

<div style="display: flex; flex-direction: column; width: 100%;">
    <div>
        <textarea id="a_textarea" style="height: 300px; width: 100%;"></textarea>
    </div>
    <div style="margin-top: 5px;">
        <button onclick="leave_a_new_message()" style="padding: 2px; padding-left: 10px; padding-right: 10px;">
            Leave A Message
        </button>
    </div>
</div>
""" + message_list_html
    elif url.startswith("/new_message?"):
        a_list.append(url_key_and_value_dict.get("text"))
        return "text", "Add successfully."
    elif url.startswith("/message_list?"):
        return "text", json.dumps(a_list)
    else:
        return "text", 'Hello, welcome to yingshaoxo message board.'

def parse_url_and_url_key_value_dict(request):
    if not request.startswith("GET"):
        return "", {}
    else:
        url = request[4:].split(" HTTP/")[0]
        url_dict = {}
        if "?" in url:
            key_value_text_list = url.split("?")[1].split("&")
            for key_and_value_text in key_value_text_list:
                splits = key_and_value_text.split("=")
                if len(splits) == 2:
                    key, value = splits
                    url_dict[key] = value
        return url, url_dict

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
            #print("get request:", request)
            url, url_key_and_value_dict = parse_url_and_url_key_value_dict(request)
            print()
            print(url)
            print(url_key_and_value_dict)

            return_type, return_value = handle_request(url, url_key_and_value_dict)

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
