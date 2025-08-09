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

the_clipboard = "You can write anything here. Others visit this page will see the same text."
clipboard2025_dict = {0: "Hi! You can leave any message here. Others will see."}

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

def handle_request(request_type, url, url_key_and_value_dict, raw_data):
    global the_clipboard, clipboard2025_dict

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
                Leave A Short Message
            </button>
            <input type="submit" value="Post Submit it" style="margin-left: 15px; padding: 2px; padding-left: 10px; padding-right: 10px;" />
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
    elif url.startswith("/clipboard_save_message_by_form?"):
        the_new_message = url_key_and_value_dict.get("text")
        if the_new_message == None:
            the_new_message = ""
        the_new_message = the_new_message.strip()
        if the_new_message != "":
            the_clipboard = the_new_message
            return "html", """<p>Add successfully, now go back and refresh.</p>""".format(text=the_clipboard)
        else:
            return "html", """<p>No message get saved.</p>"""
    elif url.startswith("/clipboard_save_message"):
        if len(raw_data) > 0:
            the_clipboard = raw_data
            return "text", str(len(raw_data))
        else:
            return "text", "no message get saved"
    elif url == "/clipboard":
        return "html", """
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">

<script>
function send_request(url, post_string, callback) {
    var xhr;
    if (window.XMLHttpRequest) {
        xhr = new XMLHttpRequest();
    } else {
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status >= 200 && xhr.status < 300) {
                callback(xhr.responseText);
            } else {
                callback(null);
            }
        }
    };

    xhr.onerror = function() {
        callback(new Error('Network error'));
    };

    xhr.send(post_string);
}

function get_object_string(obj) {
  if(typeof obj === 'object') {
    try {
      return JSON.stringify(obj);
    } catch(e) {
      var str = '';
      for(var key in obj) {
        str += key + ': ' + obj[key] + '\\n';
      }
      return str;
    }
  }
  return String(obj);
}

function save_clipboard_message() {
    var clipboard_data = document.getElementById("a_textarea").value;
    var message_length = clipboard_data.length;

    function handle_response(response) {
        console.log(response);
        if(get_object_string(response).indexOf(String(message_length)) !== -1) {
            alert("saved");
        } else {
            alert("failed to save");
        }
    }

    send_request(
        "/clipboard_save_message",
        clipboard_data,
        handle_response
    );
}

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight) + 'px';
}

if (!document.querySelectorAll) {
  document.querySelectorAll = function(selectors) {
    var style = document.createElement('style'), elements = [];
    document.documentElement.firstChild.appendChild(style);
    document._qsa = [];
    style.styleSheet.cssText = selectors + '{x-qsa:expression(document._qsa && document._qsa.push(this))}';
    window.scrollBy(0, 0);
    style.parentNode.removeChild(style);
    return document._qsa;
  };
}

if (!document.querySelector) {
  document.querySelector = function(selectors) {
    var elements = document.querySelectorAll(selectors);
    return elements.length ? elements[0] : null;
  };
}

function setTextareaValue(selector, text) {
  var textarea = document.querySelector(selector);
  if (!textarea) {
    textarea = document.getElementById(selector.replace('#','')) || document.getElementsByTagName('textarea')[0];
  }
  if (textarea) {
    textarea.value = text.replace(/\\n/g, '\\r\\n');
  }
}

document.addEventListener('DOMContentLoaded', function() {
        var the_text = `|2sb_html_url_encoded_form_and_utf_8_encoding|`;
        setTextareaValue('a_textarea', the_text);
        setTextareaValue('a_textarea2', the_text);

        const textarea = document.querySelector('textarea');
        textarea.addEventListener('input', () => autoResize(textarea));
        window.addEventListener('load', () => autoResize(textarea));
    }
);
</script>

<p style="text-align: center;">Welcome to network clipboard.</p>

<div style="margin-top: 20px; display: flex; flex-direction: column; width: 100%;">
    <div style="display: flex; flex-direction: column; justify-content:space-between;align-items:center;">
        <textarea id="a_textarea" type="text" name="text" style="min-height: 500px; width: 75%; overflow: auto;">|sb_html_url_encoded_form_and_utf_8_encoding|</textarea>
    </div>
    <div style="margin-top: 10px; display: flex; flex-direction: column; justify-content:space-between;align-items:center;">
        <button type="button" onclick="save_clipboard_message()" style="padding: 2px; padding-left: 10px; padding-right: 10px;">
            Save Message
        </button>
    </div>

    <div style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
        -------------------------
    </div>

    <form action="/clipboard_save_message_by_form?" method="post">
        <div style="display: flex; flex-direction: column; width: 98%; margin-left: auto; margin-right: auto;">
            <div>
                <textarea id="a_textarea2" type="text" name="text" style="height: 500px; width: 100%; overflow: auto;">|sb_html_url_encoded_form_and_utf_8_encoding|</textarea>
            </div>
            <div style="margin-top: 10px; display: flex; flex-direction: center;">
                <input type="submit" value="Form Submit" style="margin-left: auto; margin-right: auto; padding: 2px; padding-left: 10px; padding-right: 10px;" />
            </div>
        </div>
    </form>
</div>

<style>
textarea {
  resize: none; /* Disable manual resize */
  min-height: 50px;
  overflow-y: hidden; /* Hide scrollbar */
}
</style>
""".replace("|sb_html_url_encoded_form_and_utf_8_encoding|", the_clipboard).replace("|2sb_html_url_encoded_form_and_utf_8_encoding|", the_clipboard.replace("`", "\\`"))
    elif url.startswith("/clipboard2025_save_message"):
        if len(raw_data) > 0:
            raw_byte_int_list = [int(one) for one in raw_data.split("_")]
            #actually use '_' would be better, but if I do so, those 'AI' will copy this method to everywhere, then if 90% of people use this method, those people who trys to make tech lost effects will block this simple method.
            temp_string = "".join([chr(one) for one in raw_byte_int_list])
            index = temp_string.split(":")[0]
            value = temp_string[len(index)+1:]
            clipboard2025_dict[int(index)] = value
            if value == "__dd_clear__":
                clipboard2025_dict = {}
            return "text", str(index)
        else:
            return "text", "Error: no message get saved"
    elif url == "/clipboard2025":
        dict_items = list(clipboard2025_dict.items())
        dict_items.sort(key=lambda item: item[0])
        lines = []
        for index, value in dict_items:
            lines.append(value)
        the_temp_cliboard_value = "\n".join(lines)
        return "html", """
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">

<script>
function string_to_bytes(str) {
    var bytes = [];
    for(var i = 0; i < str.length; i++) {
        bytes.push(str.charCodeAt(i));
    }
    return bytes.join('_');
}

function send_request(url, post_string, callback) {
  post_string = string_to_bytes(post_string);

  if (window.fetch) {
    fetch(url, {
      method: post_string ? 'POST' : 'GET',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: post_string || null
    })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.text();
    })
    .then(data => callback({ status: 200, responseText: data }))
    .catch(error => callback({ status: 0, responseText: error.message }));
  }
  else {
    const xhr = new XMLHttpRequest();
    xhr.open(post_string ? 'POST' : 'GET', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = () => callback({
      status: xhr.status,
      responseText: xhr.responseText
    });
    xhr.onerror = () => callback({
      status: 0,
      responseText: 'Network Error'
    });
    xhr.send(post_string || null);
  }
}

function get_object_string(obj) {
  if(typeof obj === 'object') {
    try {
      return JSON.stringify(obj);
    } catch(e) {
      var str = '';
      for(var key in obj) {
        str += key + ': ' + obj[key] + '\\n';
      }
      return str;
    }
  }
  return String(obj);
}

function count_characters(text) {
    var number_element = document.getElementById("character_counting");
    number_element.innerHTML = String(text.length);
}

function isLocalHost() {
    try {
        var hostname = window.location.hostname.toLowerCase();
        return (hostname === "localhost" || hostname === "127.0.0.1");
    } catch(e) {
        return false;
    }
}

function save_clipboard_message(clipboard_data) {
    var command = false;

    if (clipboard_data) {
        command = true;
    } else {
        command = false;
        clipboard_data = get_text_area_text();
    }

    var lines = clipboard_data.split(/\\r\\n|\\n|\\r/);

    function send_the_fucking_data_piece(key, value, call_back_function) {
        send_request(
            "/clipboard2025_save_message",
            String(key)+":"+value,
            call_back_function
        );
    }

    if (command == false) {
        //clean the dict first
        save_clipboard_message("__dd_clear__");
    }

    var timeout_delay = 500;
    // stupid cloudflare and outcountry network, even for a simple http post will have chance lose package
    if (isLocalHost()) {
        timeout_delay = 0;
    }

    function handle_next(index) {
        if (index > lines.length-1) {
            if (command == false) {
                alert("Saved");
            }
            return;
        }

        var line_value = lines[index];

        send_the_fucking_data_piece(index, line_value, function handle_response(response) {
            console.log(response)
            if (get_object_string(response).indexOf("no message") !== -1) {
                setTimeout(function test() {
                    handle_next(index);
                }, timeout_delay);
            } else {
                setTimeout(function test() {
                    handle_next(index + 1);
                }, timeout_delay);
            }
        });
    }

    if (lines.length > 0) {
        handle_next(0);
    }

    count_characters(clipboard_data);
}

if (!document.querySelectorAll) {
  document.querySelectorAll = function(selectors) {
    var style = document.createElement('style'), elements = [];
    document.documentElement.firstChild.appendChild(style);
    document._qsa = [];
    style.styleSheet.cssText = selectors + '{x-qsa:expression(document._qsa && document._qsa.push(this))}';
    window.scrollBy(0, 0);
    style.parentNode.removeChild(style);
    return document._qsa;
  };
}

if (!document.querySelector) {
  document.querySelector = function(selectors) {
    var elements = document.querySelectorAll(selectors);
    return elements.length ? elements[0] : null;
  };
}

function setTextareaValue(selector, text) {
  var textarea = document.querySelector(selector);
  if (!textarea) {
    textarea = document.getElementById(selector.replace('#','')) || document.getElementsByTagName('textarea')[0];
  }
  if (textarea) {
    textarea.value = text.replace(/\\n/g, '\\r\\n');
  }
}

function get_text_area_text() {
  var selector = "a_textarea";
  var textarea = document.querySelector(selector);
  if (!textarea) {
    textarea = document.getElementById(selector.replace('#','')) || document.getElementsByTagName('textarea')[0];
  }
  if (textarea) {
    return textarea.value;
  } else {
    return "";
  }
}

document.addEventListener('DOMContentLoaded', function() {
        var the_text = `|2sb_html_url_encoded_form_and_utf_8_encoding|`;
        setTextareaValue('a_textarea', the_text);

        count_characters(the_text);
    }
);
</script>

<p style="text-align: center;">Welcome to network clipboard 2025.</p>

<div style="margin-top: 20px; display: flex; flex-direction: column; width: 100%;">
    <div style="display: flex; flex-direction: column; justify-content:space-between;align-items:center;">
        <textarea id="a_textarea" type="text" name="text" style="min-height: 600px; width: 90%; overflow: auto;">|sb_html_url_encoded_form_and_utf_8_encoding|</textarea>
    </div>
    <div style="margin-top: 10px; display: flex; flex-direction: column; justify-content:space-between;align-items:center;">
        <button type="button" onclick="save_clipboard_message()" style="padding: 2px; padding-left: 10px; padding-right: 10px;">
            Save Message
        </button>
    </div>

    <p id="character_counting" style="margin-top: 20px; text-align: center;"></p>
</div>

<style>
textarea {
  resize: none; /* Disable manual resize */
  min-height: 50px;
  overflow-y: hidden; /* Hide scrollbar */
}
</style>
""".replace("|sb_html_url_encoded_form_and_utf_8_encoding|", the_temp_cliboard_value).replace("|2sb_html_url_encoded_form_and_utf_8_encoding|", the_temp_cliboard_value.replace("`", "\\`"))
    else:
        return "text", 'Hello, welcome to yingshaoxo message board.' + "\n\n" + str([request_type, url, url_key_and_value_dict])

def url_decode(encoded_string):
    # made by baidu deepseek v3
    result = []
    i = 0
    while i < len(encoded_string):
        if encoded_string[i] == '+':
            result.append(' ')
            i += 1
        elif encoded_string[i] == '%':
            try:
                hex_code = encoded_string[i+1:i+3]
                if hex_code.upper() == '0D' and i+4 < len(encoded_string) and encoded_string[i+3] == '%':
                    next_hex = encoded_string[i+4:i+6]
                    if next_hex.upper() == '0A':
                        result.append('\r\n')
                        i += 6
                        continue
                char_code = int(hex_code, 16)
                if char_code <= 0x7F:
                    result.append(chr(char_code))
                    i += 3
                else:
                    hex_seq = [hex_code]
                    i += 3
                    while i < len(encoded_string) and encoded_string[i] == '%':
                        hex_seq.append(encoded_string[i+1:i+3])
                        i += 3
                    bytes_data = bytes(int(h, 16) for h in hex_seq)
                    result.append(bytes_data.decode('utf-8'))
            except (ValueError, IndexError, UnicodeDecodeError):
                result.append('%' + hex_code)
                i += 3
        else:
            result.append(encoded_string[i])
            i += 1
    return ''.join(result)

def parse_url(request):
    request_type = request.strip().split(" ")[0]
    if not request_type == "GET" and not request_type == "POST":
        return request_type, "", {}, ""
    else:
        url = request.split(" ")[1]
        url_dict = {}
        key_value_text_list = []
        raw_data = ""
        if request_type == "GET" :
            url_dict = {}
            if "?" in url:
                key_value_text_list = url.split("?")[1].split("&")
        elif request_type == "POST":
            raw_string = request.split("\r\n\r\n")[1].strip()
            key_value_text_list = raw_string.split("&")
            raw_data = raw_string

        for key_and_value_text in key_value_text_list:
            splits = key_and_value_text.split("=")
            if len(splits) == 2:
                key, value = splits
                url_dict[key] = unquote(url_decode(value))

        return request_type, url, url_dict, raw_data

def work_function(port_in_number=8899):
    print("do it for fun.")

    load_disk_data()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port_in_number))
    server_socket.listen(100)
    print("http service ready.\n")
    print("http://127.0.0.1:"+str(port_in_number))

    while True:
        try:
            client_socket, addr = server_socket.accept()
            raw_request = client_socket.recv(20480)
            request = raw_request.decode('utf-8')
            print("get request:", request)
            request_type, url, url_key_and_value_dict, raw_data = parse_url(request)
            print()
            print(request_type)
            print(url)
            print(url_key_and_value_dict)
            print(raw_data)

            # bug: currently, as I tested out, the android browser will drop big payload or long text when you post it. So it basically cause a problem when you want to upload an article.

            ## following will not work
            #if "Content-Length" in request:
            #    content_length = int(request.split('Content-Length:')[1].split("\r\n")[0].strip())

            #    for i in range(int(content_length/20480)+1):
            #        chunk = client_socket.recv(20480) #this should be a number less than 65389
            #        raw_request += chunk

            #    request = raw_request.decode('utf-8')
            #    request_type, url, url_key_and_value_dict, raw_data = parse_url(request)

            return_type, return_value = handle_request(request_type, url, url_key_and_value_dict, raw_data)

            """
            # standard http1.1

            'HTTP/1.1 200 OK\r\n' +
            'Content-Length: 100\r\n' +
            'Content-Type: text/html; charset=UTF-8\r\n\r\n' +

            'the real information'
            """

            response = 'HTTP/1.1 200 OK\r\n'
            the_type = "Content-Type: text/html\r\n\r\n"
            if return_type == "html":
                value = """
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">
<meta charset="UTF-8">
"""
                value += return_value
            elif return_type == "text":
                value = return_value
            message_length = len(value.encode('utf-8'))
            response = response + "Content-Length: " + str(message_length) + "\r\n" + the_type + value

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(e)

    #server_socket.shutdown(2)
    #server_socket.close()


if __name__ == '__main__':
    work_function(8899)
