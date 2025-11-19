import re
import os
import random
#from complete import load_data, get_next_text_block
from super_completor import Yingshaoxo_Text_Completor
import yingshaoxo_txt_data.yingshaoxo_ai as yingshaoxo_ai

yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

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
                if "yingshaoxo_thinking_dataset.txt" in file:
                    continue
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
    temp_list1 = one.split("\n# ")
    temp_list2 = []
    for sub_one in temp_list1:
        if "\n第" in sub_one and "章 " in sub_one:
            temp_list2 += sub_one.split("\n\n\n")
        else:
            temp_list2 += [sub_one]
    new_text_list += temp_list2
the_text_list = new_text_list
new_text = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(the_text_list)

#load_data("", text_data=new_text, max_sequence_length=8)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def get_random_one(input_text, text_list):
    return random.choice(text_list) if (len(text_list) > 0) else 'Not found'

def get_sub_sentence_list_from_end_to_begin_and_begin_to_end(input_text, no_single_char=True):
    input_text = input_text.strip()
    full_length = len(input_text)
    result_list = []
    for i in range(full_length):
        end_to_begin_sub_string = input_text[i:]
        begin_to_end_sub_string = input_text[:-i]
        if no_single_char == True:
            if len(end_to_begin_sub_string) > 1:
                result_list.append(end_to_begin_sub_string)
            if len(begin_to_end_sub_string) > 1:
                result_list.append(begin_to_end_sub_string)
        else:
            result_list.append(end_to_begin_sub_string)
            result_list.append(begin_to_end_sub_string)
    result_list_2 = []
    for one in result_list:
        if one not in result_list_2:
            result_list_2.append(one)
    return result_list_2

def search_text_in_text_list(search_text, source_text_list):
    longest_first_sub_sentence_list = get_sub_sentence_list_from_end_to_begin_and_begin_to_end(search_text)
    useful_source_text_list = []
    for sub_sentence in longest_first_sub_sentence_list:
        for one in source_text_list:
            if sub_sentence in one:
                useful_source_text_list.append(one)
        if len(useful_source_text_list) != 0:
            return useful_source_text_list

    return []

def a_useful_search(search_text, source_text_list):
    try:
        # load yingshaoxo_ai
        result = yingshaoxo_ai.ask_yingshaoxo_ai(search_text).stirp()
        if len(result) == 0:
            result_list = search_text_in_text_list(search_text, source_text_list)
            result = random.choice(result_list) if (len(result_list) > 0) else 'Not found'
        return result
    except Exception as e:
        print(e)
        result_list = search_text_in_text_list(search_text, source_text_list)
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
        natural_next_text = yingshaoxo_text_completor.get_next_text_by_pure_text(new_text, input_text, how_many_character_you_want=2000, level=64)
        natural_next_text = natural_next_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
        response1 = input_text + " " + natural_next_text
        response2 = a_useful_search(input_text.strip(), the_text_list)
        response3 = get_random_one(input_text.strip(), the_text_list)
        return response3 + "\n\n\n----------------------------------\n\n\n" + response2 + "\n\n\n----------------------------------\n\n\n" + response1
    else:
        return "You said: " + input_text
