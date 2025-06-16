import re
import os
import random
from complete import load_data, get_next_text_block

resource_basic_folder_path = os.path.dirname(os.path.abspath(__file__))
offline_question_and_answer_bot_dataset_path = os.path.join(resource_basic_folder_path, "./yingshaoxo_txt_data")

Has_Data = True
if not os.path.exists(offline_question_and_answer_bot_dataset_path):
    print("Run following command before anything:")
    print("git clone https://gitlab.com/yingshaoxo/yingshaoxo_txt_data.git")
    Has_Data = False

def read_text_files(folder_path):
    new_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.txt', '.md')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        new_text += f.read() + "\n\n\n\n"
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            new_text += f.read() + "\n\n\n\n"
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
    return new_text

new_text = read_text_files(offline_question_and_answer_bot_dataset_path)
the_text_list = [one.strip() for one in new_text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]
new_text_list = []
for one in the_text_list:
    temp_list1 = one.split("\n#")
    temp_list2 = []
    for sub_one in temp_list1:
        if "第" in sub_one and "章" in sub_one:
            temp_list2 += sub_one.split("\n\n\n")
        else:
            temp_list2 += [sub_one]
    new_text_list += temp_list2
the_text_list = new_text_list
new_text = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(the_text_list)

load_data("", text_data=new_text, max_sequence_length=11)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def super_search_bot(input_text, text_list, use_character=False):
    if use_character == True:
        return random.choice(text_list) if (len(text_list) > 0) else 'Not found'

    words = input_text.split(" ")
    new_words = []
    for word in words:
        if not is_ascii(word):
            if use_character == True:
                new_words += list(word)
            else:
                new_words += [word]
        else:
            new_words.append(word)

    result_list = []
    for index, target_text in enumerate(text_list):
        ok = True
        for word in new_words:
            if word not in target_text:
                ok = False
                break
        if ok == True:
            result_list.append(target_text)

    return random.choice(result_list) if (len(result_list) > 0) else 'Not found'

#def my_unquote(encoded_str):
#    if "%u" in encoded_str:
#        parts = encoded_str.split('%u')[1:]
#        decoded_str = ''.join(chr(int(code, 16)) for code in parts)
#        return decoded_str
#    else:
#        return encoded_str

def my_unquote(encoded_str):
    def replace_unicode(match):
        hex_code = match.group(1)
        try:
            code_point = int(hex_code, 16)
            if 0xD800 <= code_point <= 0xDFFF:
                return match.group(0)
            return chr(code_point)
        except (ValueError, OverflowError):
            return match.group(0)
    pattern = r'%u([0-9a-fA-F]{4})'
    return re.sub(pattern, replace_unicode, encoded_str)

def get_response(input_text):
    if not input_text:
        return "Please say something!"

    if Has_Data == True:
        input_text = my_unquote(input_text)
        natural_next_text = get_next_text_block(input_text)
        response1 = input_text + " " + natural_next_text
        response2 = super_search_bot(input_text.strip(), the_text_list)
        response3 = super_search_bot(input_text.strip(), the_text_list, use_character=True)
        return response3 + "\n\n\n-----------------\n\n\n" + response2 + "\n\n\n-----------------\n\n\n" + response1
    else:
        return "You said: " + input_text
