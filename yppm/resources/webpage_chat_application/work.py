import time
import socket
from chat import get_response

try:
    from urllib.parse import unquote
except Exception as e:
    print("error:", e)
    def unquote(encoded_str):
        if "%u" in encoded_str:
            parts = encoded_str.split('%u')[1:]
            decoded_str = ''.join(chr(int(code, 16)) for code in parts)
            return decoded_str
        else:
            return encoded_str

def handle_request(request_type, url, url_key_and_value_dict, raw_data):
    if request_type == "GET" and (url == "/" or url.startswith("/?")):
        return "html", """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!--[if !IE]>-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--<![endif]-->
    <title>Chat with yingshaoxo</title>
    <style type="text/css">
        /* Reset and base styles */
        html, body {
            width: 100%;
            height: 100%;
            margin: 0px;
            padding: 0px;
            overflow: hidden;
            background-color: #f0f2f5;
            font-family: Arial, sans-serif;
        }
        
        /* Container styles */
        #chat-container {
            position: absolute;
            left: 50%;
            top: 0px;
            width: 800px;
            margin-left: -400px;
            height: 100%;
            background-color: #ffffff;
            border-left: 1px solid #dddfe2;
            border-right: 1px solid #dddfe2;
        }
        
        /* Header styles */
        #chat-header {
            position: absolute;
            left: 0px;
            top: 0px;
            width: auto;
            right: 0px;
            height: 60px;
            background-color: #ffffff;
            border-bottom: 1px solid #dddfe2;
            box-sizing: border-box;
        }
        
        #chat-header h1 {
            margin: 0px;
            padding: 15px 20px;
            font-size: 24px;
            color: #1c1e21;
        }
        
        /* Chat history styles */
        #chat-history {
            position: absolute;
            left: 0px;
            top: 60px;
            width: auto;
            right: 0px;
            bottom: 120px;
            overflow: auto;
            background-color: #ffffff;
            padding: 20px;
        }
        
        /* Message styles */
        .message {
            margin: 10px 0px;
            padding: 10px 15px;
            max-width: 70%;
            clear: both;
            line-height: 1.4;
            word-wrap: break-word;
        }
        
        .user-message {
            float: right;
            background-color: #0084ff;
            color: #ffffff;
            margin-left: 20%;
        }
        
        .ai-message {
            float: left;
            background-color: #e9ecef;
            color: #1c1e21;
            margin-right: 20%;
        }
        
        /* Input container styles */
        #input-container {
            position: absolute;
            left: 0px;
            bottom: 0px;
            width: auto;
            right: 0px;
            height: 120px;
            background-color: #ffffff;
            border-top: 1px solid #dddfe2;
            padding: 20px;
            box-sizing: border-box;
        }
        
        #message-input {
            position: absolute;
            left: 20px;
            bottom: 20px;
            width: 75%;
            height: 80px;
            padding: 10px;
            border: 1px solid #dddfe2;
            background-color: #ffffff;
            font-size: 14px;
            font-family: Arial, sans-serif;
            resize: none;
            box-sizing: border-box;
        }
        
        #send-button {
            position: absolute;
            right: 20px;
            bottom: 20px;
            width: 15%;
            height: 80px;
            background-color: #0084ff;
            border: none;
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        
        /* Mobile styles */
        @media screen and (max-width: 800px) {
            body {
                padding: 0px 10px;
            }
            
            #chat-container {
                position: absolute;
                left: 0px;
                top: 0px;
                width: 100%;
                margin-left: 0px;
                border: none;
            }
            
            #chat-header h1 {
                font-size: 20px;
                padding: 18px 15px;
            }
            
            #chat-history {
                padding: 10px;
                width: auto;
                right: 0px;
            }
            
            #input-container {
                padding: 20px 10px;
                width: auto;
                right: 0px;
            }
            
            #message-input {
                width: 65%;
                left: 10px;
                padding: 8px;
            }
            
            #send-button {
                width: 28%;
                right: 10px;
            }
            
            .message {
                max-width: 85%;
                margin: 8px 0px;
                padding: 8px 12px;
            }
        }
        
        /* Extra small screens */
        @media screen and (max-width: 480px) {
            body {
                padding: 0px 15px;
            }
            
            #input-container {
                padding: 20px 5px;
            }
            
            #message-input {
                width: 62%;
                left: 5px;
            }
            
            #send-button {
                width: 32%;
                right: 5px;
            }
            
            .message {
                max-width: 90%;
                font-size: 14px;
            }
        }
        
        /* IE6 specific styles */
        * html body {
            padding: expression(document.body.clientWidth > 800 ? "0px" : document.body.clientWidth > 480 ? "0px 10px" : "0px 15px");
        }
        
        * html #chat-container {
            width: expression(document.body.clientWidth > 800 ? "800px" : "auto");
            margin-left: expression(document.body.clientWidth > 800 ? "-400px" : "0");
            left: expression(document.body.clientWidth > 800 ? "50%" : "0");
            right: expression(document.body.clientWidth <= 800 ? "10px" : "auto");
        }
        
        * html #message-input {
            width: expression(document.body.clientWidth > 800 ? "650px" : document.body.clientWidth > 480 ? "65%" : "62%");
            left: expression(document.body.clientWidth > 800 ? "20px" : document.body.clientWidth > 480 ? "10px" : "5px");
            padding: expression(document.body.clientWidth > 800 ? "10px" : "8px");
        }
        
        * html #send-button {
            width: expression(document.body.clientWidth > 800 ? "90px" : document.body.clientWidth > 480 ? "28%" : "32%");
            right: expression(document.body.clientWidth > 800 ? "20px" : document.body.clientWidth > 480 ? "10px" : "5px");
        }
        
        * html #chat-history {
            height: expression((document.documentElement.clientHeight || document.body.clientHeight) - 180 + "px");
            width: expression(document.body.clientWidth > 800 ? "760px" : (document.body.clientWidth - 40) + "px");
            overflow-y: auto;
            overflow-x: hidden;
            position: relative;
            margin-top: 60px;
            margin-bottom: 120px;
            padding-bottom: 0px;
        }
        
        * html #input-container {
            position: absolute;
            bottom: 0px;
            left: 0px;
            height: 120px;
            width: expression(document.body.clientWidth > 800 ? "800px" : "auto");
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chat-header">
            <h1>Chat with <a href="http://ask.ai-tools-online.xyz/chat_page" target="_blank" style="color: #4682B4; text-decoration: none;">yingshaoxo</a></h1>
        </div>
        <div id="chat-history"></div>
        <div id="input-container">
            <textarea id="message-input" cols="40" rows="4"></textarea>
            <input type="button" id="send-button" value="Send" onclick="window.sendMessage()" />
        </div>
    </div>

    <script type="text/javascript">
    //<![CDATA[
    window.sendMessage = function() {
        var input = document.getElementById('message-input');
        var message = input.value;
        if (!message) return;

        addMessage(message, true);
        input.value = '';

        var xhr;
        try {
            xhr = new ActiveXObject("Microsoft.XMLHTTP");
        } catch(e) {
            try {
                xhr = new XMLHttpRequest();
            } catch(e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }

        // Using a separate function for the callback to avoid scope issues in IE6
        function handleResponse() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    addMessage(xhr.responseText, false);
                }
            }
        }
        xhr.onreadystatechange = handleResponse;

        try {
            var url = "/chat?message=" + escape(message);
            xhr.open("GET", url, true);
            xhr.send(null);  // IE6 requires null parameter
        } catch(e) {
            alert("Error sending message");
            return false;
        }
    };

    function addMessage(text, isUser) {
        try {
            var chatHistory = document.getElementById('chat-history');
            var messageDiv = document.createElement('div');
            
            messageDiv.className = 'message';
            messageDiv.className += isUser ? ' user-message' : ' ai-message';
            
            var lines = text.split('\\n');
            for (var i = 0; i < lines.length; i++) {
                if (i > 0) {
                    var br = document.createElement('br');
                    messageDiv.appendChild(br);
                }
                var textNode = document.createTextNode(lines[i] || ' ');
                messageDiv.appendChild(textNode);
            }
            
            chatHistory.appendChild(messageDiv);
            
            // Add clearfix div after each message
            var clearfix = document.createElement('div');
            clearfix.className = 'clearfix';
            chatHistory.appendChild(clearfix);
            
            // Scroll to bottom
            var scrollHeight = chatHistory.scrollHeight;
            if (scrollHeight) {
                chatHistory.scrollTop = scrollHeight;
            }
        } catch(e) {
            alert("Error adding message");
        }
    }

    // Simple cross-browser event handler
    document.getElementById('message-input').onkeypress = function(e) {
        e = e || window.event;
        var keyCode = e.keyCode || e.which;
        return true;
    };
    //]]>
    </script>
</body>
</html>
"""
    elif url.startswith("/chat?"):
        message = url_key_and_value_dict.get("message", "")
        response = get_response(message)
        return "text", response
    else:
        return "text", 'Hello, welcome to AI chat.'

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
        return request_type, "", {}, ""
    else:
        url = request.split(" ")[1]
        url_dict = {}
        key_value_text_list = []
        raw_data = ""
        if request_type == "GET":
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
                url_dict[key] = url_decode(value)

        return request_type, url, url_dict, raw_data

def work_function(port_in_number=8899):
    print("Starting AI chat server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port_in_number))
    server_socket.listen(100)
    print("Chat server ready.\n")
    print("http://127.0.0.1:" + str(port_in_number))

    while True:
        try:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(20480).decode('utf-8')
            request_type, url, url_key_and_value_dict, raw_data = parse_url(request)

            return_type, return_value = handle_request(request_type, url, url_key_and_value_dict, raw_data)

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

if __name__ == '__main__':
    pass
